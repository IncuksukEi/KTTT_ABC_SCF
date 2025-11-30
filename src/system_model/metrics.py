import numpy as np

class SystemMetrics:
    def __init__(self, config):
        self.bandwidth = float(config['system']['bandwidth'])
        # Chuyển đổi công suất nhiễu từ dBm sang Watts
        # P_watt = 10^((P_dbm - 30) / 10)
        noise_dbm = float(config['system']['noise_power_dbm'])
        self.noise_power = 10**((noise_dbm - 30) / 10)

    def calculate_sum_rate(self, W, H):
        """
        Tính tổng tốc độ dữ liệu (Sum Rate).
        
        Args:
            W: Ma trận Beamforming (M, K, N) - Biến cần tối ưu
            H: Ma trận kênh truyền (M, K, N)
            
        Returns:
            sum_rate: Tổng dung lượng (bps/Hz) hoặc (bps) tùy config
            individual_rates: List tốc độ của từng user
        """
        M, K, N = W.shape
        sinr_list = []
        
        # Duyệt qua từng User k để tính SINR
        for k in range(K):
            # --- 1. Tính công suất tín hiệu mong muốn (Signal Power) ---
            # Tín hiệu user k nhận được là tổng hợp từ tất cả AP m
            # S_k = | sum_m (h_mk^H * w_mk) |^2
            signal_amplitude = 0
            for m in range(M):
                h_mk = H[m, k, :]     # Vector kênh (N,)
                w_mk = W[m, k, :]     # Vector trọng số (N,)
                # np.vdot(a, b) tương đương a.H * b (conjugate transpose)
                signal_amplitude += np.vdot(h_mk, w_mk) 
            
            signal_power = np.abs(signal_amplitude)**2
            
            # --- 2. Tính công suất nhiễu giao thoa (Interference) ---
            # Nhiễu do tín hiệu gửi cho user j (j != k) gây ra
            interference_power = 0
            for j in range(K):
                if j == k: continue # Không tính chính mình
                
                inter_amplitude = 0
                for m in range(M):
                    h_mk = H[m, k, :] # Kênh của user k (nạn nhân)
                    w_mj = W[m, j, :] # Trọng số phát cho user j (kẻ gây nhiễu)
                    inter_amplitude += np.vdot(h_mk, w_mj)
                
                interference_power += np.abs(inter_amplitude)**2
                
            # --- 3. Tính SINR ---
            sinr = signal_power / (interference_power + self.noise_power)
            sinr_list.append(sinr)
            
        # Tính Rate theo công thức Shannon: Rate = log2(1 + SINR)
        # Kết quả trả về là Spectral Efficiency (bps/Hz)
        individual_rates = np.log2(1 + np.array(sinr_list))
        sum_rate = np.sum(individual_rates)
        
        return sum_rate