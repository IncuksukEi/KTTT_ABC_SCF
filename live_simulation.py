import matplotlib.pyplot as plt
import numpy as np
import time

# Import các module đã viết
from src.system_model.channel import ChannelModel
from src.system_model.metrics import SystemMetrics
from src.algorithms.abc_variants import GbestABC
from main import load_config

def run_live_demo():
    # 1. Load cấu hình
    config = load_config()
    
    # Giảm số vòng lặp xuống một chút nếu muốn demo nhanh (VD: 50)
    # config['algorithm']['max_cycle'] = 50 
    max_cycle = config['algorithm']['max_cycle']
    
    # 2. Tạo môi trường
    M = config['system']['M']
    K = config['system']['K']
    N = config['system']['N']
    
    print("--- KHỞI TẠO MÔ PHỎNG TRỰC TIẾP (LIVE DEMO) ---")
    channel_model = ChannelModel(M, K, N)
    H = channel_model.generate_rayleigh_channel()
    metrics = SystemMetrics(config)
    
    # Khởi tạo thuật toán G-ABC
    optimizer = GbestABC(config, H, metrics)
    optimizer.initialize_population() # Bước 1: Khởi tạo bầy ong
    
    # --- THIẾT LẬP ĐỒ THỊ LIVE ---
    plt.ion() # Bật chế độ Interactive (vẽ động)
    fig = plt.figure(figsize=(14, 6))
    
    # Subplot 1: Biểu đồ hội tụ (Sum Rate tăng dần)
    ax1 = fig.add_subplot(1, 2, 1)
    line, = ax1.plot([], [], 'b-o', linewidth=2, label='Current Best SumRate')
    ax1.set_xlim(0, max_cycle)
    # Dự đoán y_lim khoảng 0 đến 50 (tùy tham số, có thể chỉnh sau)
    ax1.set_ylim(0, 30) 
    ax1.set_title("Tốc độ hội tụ theo thời gian thực")
    ax1.set_xlabel("Vòng lặp (Cycle)")
    ax1.set_ylabel("Sum Rate (bps/Hz)")
    ax1.grid(True)
    ax1.legend()
    
    # Subplot 2: Búp sóng (Beam Pattern) thay đổi hình dạng
    ax2 = fig.add_subplot(1, 2, 2, projection='polar')
    theta = np.linspace(-np.pi, np.pi, 360)
    
    # Lưu dữ liệu để vẽ
    history_fitness = []
    
    print(">>> Đang chạy vòng lặp tối ưu...")
    
    # 3. VÒNG LẶP THỦ CÔNG (Thay vì gọi .solve(), ta gọi từng bước)
    for cycle in range(max_cycle):
        # --- A. Các bước của thuật toán ABC ---
        optimizer.employed_bees_phase()
        optimizer.onlooker_bees_phase()
        optimizer.scout_bees_phase()
        optimizer.memorize_best_solution()
        
        # --- B. Lấy dữ liệu cập nhật ---
        current_best = optimizer.best_fitness
        history_fitness.append(current_best)
        
        # --- C. Cập nhật đồ thị (Cứ mỗi 2 vòng lặp vẽ 1 lần cho đỡ lag) ---
        if cycle % 2 == 0 or cycle == max_cycle - 1:
            # 1. Update biểu đồ đường
            line.set_xdata(range(len(history_fitness)))
            line.set_ydata(history_fitness)
            
            # Tự động scale trục Y nếu giá trị vượt quá khung
            if current_best > ax1.get_ylim()[1]:
                ax1.set_ylim(0, current_best * 1.2)
            
            ax1.set_title(f"Cycle {cycle}/{max_cycle} - Rate: {current_best:.2f} bps/Hz")
            
            # 2. Update biểu đồ cực (Polar)
            ax2.clear() # Xóa hình cũ
            # Lấy vector beamforming tốt nhất hiện tại của AP đầu tiên
            W_best = optimizer.best_solution
            
            # Giả lập vị trí user để vẽ (đánh dấu bằng đường kẻ đứt)
            # Lưu ý: Trong code metrics mình không cố định góc user, 
            # nên ở đây vẽ minh họa hình dạng búp sóng thay đổi là chính.
            
            # Vẽ pattern cho User 1 (để minh họa sự tập trung năng lượng)
            w_k = W_best[0, 0, :] # User đầu tiên
            pattern = []
            for ang in theta:
                a_theta = np.exp(-1j * np.pi * np.arange(N) * np.sin(ang))
                gain = np.abs(np.vdot(w_k, a_theta))**2
                pattern.append(gain)
            
            ax2.plot(theta, pattern, 'r-', linewidth=2)
            ax2.set_title(f"Hình dạng Búp sóng (Beam Pattern)\nUser 1 @ AP 1", va='bottom')
            
            # Dừng 0.1s để mắt người kịp nhìn thấy thay đổi
            plt.draw()
            plt.pause(0.1)

    print("✅ Hoàn tất mô phỏng!")
    plt.ioff() # Tắt chế độ interactive
    plt.show() # Giữ hình cuối cùng lại

if __name__ == "__main__":
    run_live_demo()