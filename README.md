# 📡 Tối ưu hóa Beamforming trong mạng Scalable Cell-free ISAC sử dụng thuật toán G-ABC

![Language](https://img.shields.io/badge/Language-Python%203.8%2B-blue)
![Library](https://img.shields.io/badge/Library-NumPy%20%7C%20Matplotlib-orange)
![Subject](https://img.shields.io/badge/Subject-Communication%20Engineering-green)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

> **Đồ án môn học:** Kỹ thuật Truyền tin (Communication Engineering)  
> **Học kỳ:** 2024-2025  
> **Giảng viên hướng dẫn:** [Tên Giảng Viên]

---

## 📖 Mục lục
1. [Giới thiệu đề tài](#-giới-thiệu-đề-tài)
2. [Mô hình hệ thống & Thuật toán](#-mô-hình-hệ-thống--thuật-toán)
3. [Cấu trúc dự án](#-cấu-trúc-dự-án)
4. [Cài đặt môi trường](#-cài-đặt-môi-trường)
5. [Hướng dẫn sử dụng](#-hướng-dẫn-sử-dụng)
6. [Kết quả mô phỏng](#-kết-quả-mô-phỏng)
7. [Tác giả](#-tác-giả)

---

## 📝 Giới thiệu đề tài

Dự án này tập trung giải quyết bài toán tối ưu hóa tài nguyên vô tuyến trong mạng **Scalable Cell-free Massive MIMO** tích hợp Cảm biến và Truyền thông (ISAC). Mục tiêu chính là tối đa hóa **Tổng tốc độ dữ liệu (Sum-Rate)** của người dùng dưới các ràng buộc vật lý về công suất phát.

Thách thức chính của bài toán là tìm ra ma trận trọng số Beamforming (Precoding Matrix) tối ưu trong không gian tìm kiếm phức hợp nhiều chiều. Chúng tôi đề xuất sử dụng thuật toán **Gbest-guided Artificial Bee Colony (G-ABC)** để giải quyết vấn đề hội tụ chậm của thuật toán ABC truyền thống.

---

## 📐 Mô hình hệ thống & Thuật toán

### 1. Thông số kỹ thuật
* **Kiến trúc mạng:** Scalable Cell-free Massive MIMO.
* **Mô hình kênh truyền:** Rayleigh Fading (Small-scale) kết hợp Pathloss (Large-scale).
* **Số lượng Access Points (AP):** $M = 16$.
* **Số lượng User (UE):** $K = 4$.
* **Số lượng Anten/AP:** $N = 2$.
* **Công suất phát tối đa ($P_{max}$):** 23 dBm (200 mW).

### 2. Thuật toán tối ưu (G-ABC)
So với ABC gốc, biến thể G-ABC cải tiến phương trình tìm kiếm của Ong thợ bằng cách tích hợp thông tin từ cá thể tốt nhất toàn cục ($x_{best}$):

$$v_{ij} = x_{ij} + \phi_{ij}(x_{ij} - x_{kj}) + \psi_{ij}(x_{best,j} - x_{ij})$$

* **Thành phần $\phi$:** Duy trì sự đa dạng (Exploration).
* **Thành phần $\psi$:** Tăng tốc độ hội tụ về cực trị (Exploitation).

---

## 📂 Cấu trúc dự án

Mã nguồn được tổ chức theo mô hình **Modular Design**, tách biệt giữa Lõi thuật toán và Mô hình vật lý.

```text
KTTT_ABC_SCF/
├── config.yaml                 # ⚙️ FILE CẤU HÌNH (Chỉnh sửa tham số hệ thống tại đây)
├── main.py                     # 🚀 SCRIPT CHÍNH (Chạy Monte Carlo & Vẽ đồ thị)
├── compare_algorithms.py       # 📊 SCRIPT SO SÁNH (Benchmark ABC vs G-ABC)
├── live_simulation.py          # 🎬 SCRIPT DEMO (Chạy mô phỏng thời gian thực)
├── simple_test.py              # 🧪 SCRIPT TEST (Kiểm thử trên hàm toán học)
├── requirements.txt            # 📦 THƯ VIỆN (Danh sách dependencies)
│
├── src/                        # SOURCE CODE
│   ├── system_model/           # [Physical Layer Module]
│   │   ├── channel.py          # Tạo kênh truyền (H Matrix generation)
│   │   ├── metrics.py          # Tính toán Sum-Rate, SINR
│   │   └── constraints.py      # Xử lý ràng buộc công suất (Power Normalization)
│   │
│   ├── algorithms/             # [Optimization Module]
│   │   ├── abc_base.py         # Class ABC gốc
│   │   └── abc_variants.py     # Class G-ABC (Kế thừa và cải tiến)
│   │
│   └── utils/                  # [Utility Module]
│       └── visualization.py    # Các hàm vẽ đồ thị (Convergence, Polar Plot)
│
└── results/                    # KẾT QUẢ ĐẦU RA
    └── figures/                # Chứa ảnh đồ thị (.png)
