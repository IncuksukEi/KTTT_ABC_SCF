import os

def create_project_structure():
    # Tên thư mục gốc
    root_dir = "."

    # Các thư mục con cần tạo
    folders = [
        "src",
        "src/algorithms",
        "src/system_model",
        "src/utils",
        "notebooks",
        "results",
        "results/figures",
        "results/logs"
    ]

    # Các file rỗng cần tạo
    files = [
        "config.yaml",
        "main.py",
        "requirements.txt",
        "README.md",
        "src/__init__.py",
        "src/algorithms/__init__.py",
        "src/algorithms/abc_base.py",
        "src/algorithms/abc_variants.py",
        "src/system_model/__init__.py",
        "src/system_model/channel.py",
        "src/system_model/metrics.py",
        "src/system_model/constraints.py",
        "src/utils/__init__.py",
        "src/utils/config_loader.py",
        "src/utils/visualization.py"
    ]

    print(f"🚀 Đang khởi tạo cấu trúc dự án...")

    # 1. Tạo thư mục
    for folder in folders:
        path = os.path.join(root_dir, folder)
        os.makedirs(path, exist_ok=True)
        print(f"   [DIR]  Đã tạo: {path}")

    # 2. Tạo file
    for file in files:
        path = os.path.join(root_dir, file)
        if not os.path.exists(path):
            with open(path, 'w', encoding='utf-8') as f:
                pass # Tạo file rỗng
            print(f"   [FILE] Đã tạo: {path}")
        else:
            print(f"   [SKIP] File đã tồn tại: {path}")

    print("\n✅ Hoàn tất! Bạn có thể bắt đầu code.")

if __name__ == "__main__":
    create_project_structure()