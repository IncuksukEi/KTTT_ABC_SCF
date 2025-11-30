import numpy as np
import matplotlib.pyplot as plt
import os

def plot_convergence(curve1, curve2):
    """Vẽ so sánh tốc độ hội tụ"""
    plt.figure(figsize=(10, 6))
    plt.plot(curve1, 'b--o', markevery=10, label='Original ABC', linewidth=2)
    plt.plot(curve2, 'r-s', markevery=10, label='Gbest-guided ABC', linewidth=2)
    
    plt.title('Convergence Comparison: ABC vs G-ABC', fontsize=14)
    plt.xlabel('Iterations (Cycles)', fontsize=12)
    plt.ylabel('Sum Rate (bps/Hz)', fontsize=12)
    plt.legend(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Tạo thư mục nếu chưa có
    os.makedirs('results/figures', exist_ok=True)
    save_path = 'results/figures/convergence_comparison.png'
    plt.savefig(save_path, dpi=300)
    print(f"\n[1/2] Đã lưu biểu đồ hội tụ tại: {save_path}")
    # plt.show() # Bỏ comment nếu muốn hiện cửa sổ

def plot_beampattern(W, N, save_name="beampattern.png"):
    """
    Vẽ hình dạng búp sóng (Beam Pattern) của AP đầu tiên.
    W: Ma trận Beamforming tốt nhất (M, K, N)
    N: Số lượng anten
    """
    M, K, _ = W.shape
    
    # Tạo không gian góc từ -180 đến 180 độ
    theta = np.linspace(-np.pi, np.pi, 360)
    
    plt.figure(figsize=(10, 8))
    ax = plt.subplot(111, projection='polar')
    
    # Vẽ pattern cho từng User (tại AP đầu tiên m=0)
    for k in range(K):
        w_k = W[0, k, :] # Vector beamforming của AP 0 dành cho User k
        
        # Tính Array Factor: Gain(theta) = |w^H * a(theta)|
        pattern = []
        for ang in theta:
            # Vector dẫn hướng (Steering vector) cho mảng anten thẳng (ULA)
            # Giả sử khoảng cách d = lambda/2 -> phase shift = pi * sin(theta)
            a_theta = np.exp(-1j * np.pi * np.arange(N) * np.sin(ang))
            
            # Tính độ lợi
            gain = np.abs(np.vdot(w_k, a_theta))**2
            pattern.append(gain)
            
        ax.plot(theta, pattern, label=f'Beam to User {k+1}', linewidth=2)

    plt.title(f"Visualizing Beam Pattern at AP #1 (N={N})", y=1.08, fontsize=14)
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    
    save_path = f'results/figures/{save_name}'
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"[2/2] Đã lưu biểu đồ búp sóng tại: {save_path}")