import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

# Import các module từ dự án của bạn
from main import load_config
from src.system_model.channel import ChannelModel
from src.system_model.metrics import SystemMetrics
from src.algorithms.abc_base import ArtificialBeeColony
from src.algorithms.abc_variants import GbestABC

def run_comparison():
    # 1. Cấu hình hệ thống
    config = load_config()
    M = config['system']['M']
    K = config['system']['K']
    N = config['system']['N']
    
    print("--- BẮT ĐẦU SO SÁNH TRỰC QUAN ---")
    
    # 2. Tạo môi trường (QUAN TRỌNG: Cả 2 thuật toán phải chạy trên cùng 1 kênh H)
    print("1. Khởi tạo kênh truyền ngẫu nhiên...")
    channel_model = ChannelModel(M, K, N)
    H = channel_model.generate_rayleigh_channel()
    metrics = SystemMetrics(config)
    
    # 3. Chạy thuật toán 1: ABC Gốc
    print("2. Đang chạy ABC Gốc (Original)...")
    abc_solver = ArtificialBeeColony(config, H, metrics)
    fit_abc, curve_abc = abc_solver.solve()
    
    # 4. Chạy thuật toán 2: G-ABC (Biến thể)
    print("3. Đang chạy G-ABC (Gbest-guided)...")
    gabc_solver = GbestABC(config, H, metrics)
    fit_gabc, curve_gabc = gabc_solver.solve()
    
    # 5. Vẽ đồ thị so sánh trực quan
    print("4. Đang vẽ đồ thị...")
    visualize_comparison(curve_abc, fit_abc, curve_gabc, fit_gabc)

def visualize_comparison(curve1, final1, curve2, final2):
    plt.figure(figsize=(14, 6))
    
    # --- Biểu đồ 1: Đường hội tụ (Line Chart) ---
    ax1 = plt.subplot(1, 2, 1)
    ax1.plot(curve1, 'b--o', markevery=10, label='ABC Gốc', linewidth=2, alpha=0.7)
    ax1.plot(curve2, 'r-s', markevery=10, label='G-ABC (Cải tiến)', linewidth=2)
    
    ax1.set_title('So sánh tốc độ hội tụ', fontsize=14, fontweight='bold')
    ax1.set_xlabel('Vòng lặp (Iterations)')
    ax1.set_ylabel('Tổng tốc độ (Sum Rate) [bps/Hz]')
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.6)
    
    # Đánh dấu điểm kết thúc
    ax1.plot(len(curve1)-1, final1, 'b*', markersize=15)
    ax1.plot(len(curve2)-1, final2, 'r*', markersize=15)
    
    # --- Biểu đồ 2: Cột so sánh kết quả cuối (Bar Chart) ---
    ax2 = plt.subplot(1, 2, 2)
    algorithms = ['ABC Gốc', 'G-ABC']
    scores = [final1, final2]
    colors = ['blue', 'red']
    
    bars = ax2.bar(algorithms, scores, color=colors, alpha=0.8, width=0.5)
    
    # Thêm số liệu lên đầu cột
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.2f}',
                 ha='center', va='bottom', fontsize=12, fontweight='bold')
        
    # Tính phần trăm cải thiện
    improvement = ((final2 - final1) / final1) * 100
    
    ax2.set_title(f'Kết quả cuối cùng (Cải thiện: +{improvement:.1f}%)', fontsize=14, fontweight='bold')
    ax2.set_ylabel('Sum Rate tối đa đạt được')
    ax2.set_ylim(0, max(scores)*1.2) # Tăng chiều cao trục Y để số không bị che
    
    plt.tight_layout()
    
    # Lưu và hiển thị
    plt.savefig('results/figures/comparison_visual.png', dpi=300)
    print("Đã lưu ảnh so sánh tại: results/figures/comparison_visual.png")
    plt.show()

if __name__ == "__main__":
    run_comparison()