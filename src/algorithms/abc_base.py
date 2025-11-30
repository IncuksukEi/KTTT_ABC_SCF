import numpy as np
import copy
from src.system_model.constraints import enforce_power_constraint

class ArtificialBeeColony:
    def __init__(self, config, channel_H, metrics_calculator):
        # 1. Load tham số từ config
        self.pop_size = int(config['algorithm']['pop_size']) # SN
        self.max_cycle = int(config['algorithm']['max_cycle'])
        self.limit = int(config['algorithm']['limit'])
        self.p_max_dbm = float(config['system']['p_max_dbm'])
        
        # 2. Lưu môi trường (Kênh và Hàm tính điểm)
        self.H = channel_H
        self.metrics = metrics_calculator
        
        # Kích thước bài toán: (M, K, N)
        self.M = int(config['system']['M'])
        self.K = int(config['system']['K'])
        self.N = int(config['system']['N'])
        
        # 3. Khởi tạo quần thể
        # self.population là mảng 4 chiều: (SN, M, K, N)
        # Mỗi phần tử population[i] là một giải pháp Beamforming hoàn chỉnh
        self.population = None 
        self.fitness = np.zeros(self.pop_size)
        self.trial_counters = np.zeros(self.pop_size) # Đếm số lần không cải thiện (cho Scout bee)
        
        # Lưu kết quả tốt nhất toàn cục
        self.best_solution = None
        self.best_fitness = -np.inf
        self.convergence_curve = [] # Để vẽ biểu đồ

    def initialize_population(self):
        """Khởi tạo ngẫu nhiên quần thể ban đầu"""
        # Tạo số phức ngẫu nhiên: Thực + Ảo
        X_real = np.random.randn(self.pop_size, self.M, self.K, self.N)
        X_imag = np.random.randn(self.pop_size, self.M, self.K, self.N)
        self.population = X_real + 1j * X_imag
        
        # Quan trọng: Chuẩn hóa công suất ngay từ đầu
        for i in range(self.pop_size):
            self.population[i] = enforce_power_constraint(self.population[i], self.p_max_dbm)
            self.fitness[i] = self.metrics.calculate_sum_rate(self.population[i], self.H)
            
        # Cập nhật Best Global
        best_idx = np.argmax(self.fitness)
        self.best_fitness = self.fitness[best_idx]
        self.best_solution = copy.deepcopy(self.population[best_idx])

    def generate_candidate(self, current_idx, partner_idx):
        """
        Hàm sinh giải pháp mới (Logic cốt lõi của ABC gốc).
        v_i = x_i + phi * (x_i - x_k)
        """
        phi = np.random.uniform(-1, 1, size=(self.M, self.K, self.N))
        
        current_sol = self.population[current_idx]
        partner_sol = self.population[partner_idx]
        
        # Công thức ABC gốc
        new_candidate = current_sol + phi * (current_sol - partner_sol)
        return new_candidate

    def employed_bees_phase(self):
        """Giai đoạn Ong thợ"""
        for i in range(self.pop_size):
            # 1. Chọn đối tác ngẫu nhiên k khác i
            candidates = list(range(self.pop_size))
            candidates.remove(i)
            k = np.random.choice(candidates)
            
            # 2. Sinh giải pháp mới
            new_sol = self.generate_candidate(i, k)
            
            # 3. Xử lý ràng buộc công suất (Cực quan trọng)
            new_sol = enforce_power_constraint(new_sol, self.p_max_dbm)
            
            # 4. Đánh giá và Tham lam (Greedy Selection)
            new_fitness = self.metrics.calculate_sum_rate(new_sol, self.H)
            
            if new_fitness > self.fitness[i]:
                self.population[i] = new_sol
                self.fitness[i] = new_fitness
                self.trial_counters[i] = 0 # Reset bộ đếm
            else:
                self.trial_counters[i] += 1 # Tăng bộ đếm thất bại

    def onlooker_bees_phase(self):
        """Giai đoạn Ong quan sát (Roulette Wheel Selection)"""
        # Tính xác suất chọn lọc
        # Để tránh chia cho 0 hoặc số âm, ta dùng hàm exp hoặc shift dương
        # Ở đây Sum-rate luôn dương nên tính trực tiếp tỉ lệ
        prob = self.fitness / np.sum(self.fitness)
        
        # Ong quan sát chọn nguồn thức ăn để khai thác
        for _ in range(self.pop_size):
            # Chọn i dựa trên xác suất prob
            i = np.random.choice(self.pop_size, p=prob)
            
            # Thực hiện tìm kiếm giống hệt Ong thợ
            candidates = list(range(self.pop_size))
            candidates.remove(i)
            k = np.random.choice(candidates)
            
            new_sol = self.generate_candidate(i, k)
            new_sol = enforce_power_constraint(new_sol, self.p_max_dbm)
            new_fitness = self.metrics.calculate_sum_rate(new_sol, self.H)
            
            if new_fitness > self.fitness[i]:
                self.population[i] = new_sol
                self.fitness[i] = new_fitness
                self.trial_counters[i] = 0
            else:
                self.trial_counters[i] += 1

    def scout_bees_phase(self):
        """Giai đoạn Ong trinh sát"""
        for i in range(self.pop_size):
            if self.trial_counters[i] > self.limit:
                # Reset hoàn toàn giải pháp này (Random search)
                X_real = np.random.randn(self.M, self.K, self.N)
                X_imag = np.random.randn(self.M, self.K, self.N)
                new_sol = X_real + 1j * X_imag
                
                self.population[i] = enforce_power_constraint(new_sol, self.p_max_dbm)
                self.fitness[i] = self.metrics.calculate_sum_rate(self.population[i], self.H)
                self.trial_counters[i] = 0

    def memorize_best_solution(self):
        """Lưu lại kết quả tốt nhất vòng lặp này"""
        current_best_idx = np.argmax(self.fitness)
        if self.fitness[current_best_idx] > self.best_fitness:
            self.best_fitness = self.fitness[current_best_idx]
            self.best_solution = copy.deepcopy(self.population[current_best_idx])

    def solve(self):
        """Hàm chạy chính"""
        self.initialize_population()
        
        for cycle in range(self.max_cycle):
            self.employed_bees_phase()
            self.onlooker_bees_phase()
            self.scout_bees_phase()
            self.memorize_best_solution()
            
            # Lưu lịch sử hội tụ
            self.convergence_curve.append(self.best_fitness)
            
            # (Tùy chọn) In log mỗi 10 vòng
            if (cycle+1) % 10 == 0:
                print(f"Cycle {cycle+1}/{self.max_cycle}: Best Rate = {self.best_fitness:.4f} bps/Hz")
                
        return self.best_fitness, self.convergence_curve