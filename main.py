import yaml
import numpy as np
from tqdm import tqdm

from src.system_model.channel import ChannelModel
from src.system_model.metrics import SystemMetrics
from src.algorithms.abc_base import ArtificialBeeColony
from src.algorithms.abc_variants import GbestABC
from src.utils.visualization import plot_convergence, plot_beampattern

def load_config(path='config.yaml'):
    # SỬA LỖI: Thêm encoding='utf-8' để đọc tiếng Việt trong config
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def run_simulation():
    # 1. Load Cấu hình
    config = load_config()
    n_realizations = config['simulation']['n_realizations']
    print(f"--- Bắt đầu mô phỏng Cell-free ISAC (Chạy {n_realizations} lần) ---")
    
    # Lưu trữ kết quả trung bình
    avg_curve_abc = np.zeros(config['algorithm']['max_cycle'])
    avg_curve_gabc = np.zeros(config['algorithm']['max_cycle'])
    
    # Biến lưu lại giải pháp tốt nhất cuối cùng để vẽ búp sóng
    final_best_W = None 
    
    # 2. Vòng lặp Monte Carlo
    for i in range(n_realizations):
        print(f"\nRunning Realization {i+1}/{n_realizations}...")
        
        # a. Tạo môi trường
        M = config['system']['M']
        K = config['system']['K']
        N = config['system']['N']
        
        channel_model = ChannelModel(M, K, N)
        H = channel_model.generate_rayleigh_channel()
        
        metrics = SystemMetrics(config)
        
        # b. Chạy ABC gốc
        print("  > [1] Running ABC Original...")
        abc = ArtificialBeeColony(config, H, metrics)
        _, curve_abc = abc.solve()
        avg_curve_abc += np.array(curve_abc)
        
        # c. Chạy G-ABC
        print("  > [2] Running G-ABC...")
        gabc = GbestABC(config, H, metrics)
        _, curve_gabc = gabc.solve()
        avg_curve_gabc += np.array(curve_gabc)
        
        # Lưu lại giải pháp G-ABC của lần chạy cuối cùng
        if i == n_realizations - 1:
            final_best_W = gabc.best_solution

    # 3. Tính trung bình
    avg_curve_abc /= n_realizations
    avg_curve_gabc /= n_realizations
    
    # 4. Vẽ và Lưu đồ thị
    print("\n--- Đang vẽ đồ thị ---")
    # Biểu đồ 1: So sánh hội tụ
    plot_convergence(avg_curve_abc, avg_curve_gabc)
    
    # Biểu đồ 2: Búp sóng (Beam Pattern) của giải pháp tốt nhất
    if final_best_W is not None:
        plot_beampattern(final_best_W, N=config['system']['N'])
        
    print("\nMô phỏng hoàn tất! Kiểm tra thư mục 'results/figures'.")

if __name__ == "__main__":
    run_simulation()