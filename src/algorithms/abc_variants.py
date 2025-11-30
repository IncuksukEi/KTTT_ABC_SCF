import numpy as np
from src.algorithms.abc_base import ArtificialBeeColony

class GbestABC(ArtificialBeeColony):
    def __init__(self, config, channel_H, metrics_calculator):
        # Gọi hàm khởi tạo của lớp cha
        super().__init__(config, channel_H, metrics_calculator)
        
        # Load thêm tham số psi cho G-ABC
        self.psi_factor = float(config['algorithm']['psi'])

    def generate_candidate(self, current_idx, partner_idx):
        """
        OVERRIDE: Ghi đè hàm sinh giải pháp của ABC gốc.
        Công thức G-ABC:
        v_i = x_i + phi*(x_i - x_k) + psi*(x_best - x_i)
        """
        # 1. Thành phần ngẫu nhiên (Exploration)
        phi = np.random.uniform(-1, 1, size=(self.M, self.K, self.N))
        
        # 2. Thành phần dẫn hướng (Exploitation)
        # psi là số dương khoảng [0, 1.5]
        psi = np.random.uniform(0, self.psi_factor, size=(self.M, self.K, self.N))
        
        current_sol = self.population[current_idx]
        partner_sol = self.population[partner_idx]
        best_sol = self.best_solution # Lấy từ biến lưu trữ của lớp cha
        
        # Áp dụng công thức
        term1 = phi * (current_sol - partner_sol)
        term2 = psi * (best_sol - current_sol)
        
        new_candidate = current_sol + term1 + term2
        
        return new_candidate