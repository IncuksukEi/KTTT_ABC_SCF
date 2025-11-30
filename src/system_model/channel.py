import numpy as np

class ChannelModel:
    def __init__(self, M, K, N):
        """
        Khởi tạo mô hình kênh.
        :param M: Số lượng AP
        :param K: Số lượng User
        :param N: Số lượng anten mỗi AP
        """
        self.M = M
        self.K = K
        self.N = N

    def generate_rayleigh_channel(self):
        """
        Tạo kênh Rayleigh Fading chuẩn (Small-scale fading).
        Mô phỏng môi trường phân tán mạnh, không có tầm nhìn thẳng (NLOS).
        
        Returns:
            H: Ma trận phức kích thước (M, K, N)
               H[m, k, :] là vector kênh từ AP m đến User k.
        """
        # Tạo phần thực và ảo theo phân phối chuẩn N(0, 1)
        H_real = np.random.randn(self.M, self.K, self.N)
        H_imag = np.random.randn(self.M, self.K, self.N)
        
        # Kết hợp thành số phức và chuẩn hóa công suất trung bình về 1
        H = (H_real + 1j * H_imag) / np.sqrt(2)
        
        return H

    def generate_channel_with_pathloss(self, area_size=1000):
        """
        (Nâng cao) Tạo kênh có cả Large-scale fading (Pathloss).
        Để đơn giản hóa cho bài tập lớn, hàm này giữ cấu trúc beta ngẫu nhiên.
        """
        # Small-scale fading
        g = self.generate_rayleigh_channel()
        
        # Large-scale fading (Beta): Mô phỏng user ở xa/gần AP
        # Log-normal distribution để mô phỏng shadowing
        beta_db = np.random.uniform(-10, 10, (self.M, self.K)) # Giả lập ngẫu nhiên
        beta = 10**(beta_db / 10)
        
        H = np.zeros((self.M, self.K, self.N), dtype=complex)
        for m in range(self.M):
            for k in range(self.K):
                H[m, k, :] = np.sqrt(beta[m, k]) * g[m, k, :]
                
        return H