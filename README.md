# AI Live Stream MC (AI_MC)

MC AI trực tiếp bằng giọng nói và khuôn mặt. Hệ thống tự sinh kịch bản giới thiệu sản phẩm, đồng bộ khẩu hình và phát trực tiếp lên các nền tảng mạng xã hội.

---

## 📂 Tài Liệu Dự Án (Documentation)

Hệ thống tài liệu quản lý dự án nằm trong thư mục `docs/`:

*   [ROADMAP.md](docs/ROADMAP.md) - Tổng quan 7 Phase phát triển.
*   [PHASES/](docs/PHASES/) - Chi tiết yêu cầu và tiêu chí hoàn thành (DoD) của từng giai đoạn.
*   [SPRINTS/](docs/SPRINTS/) - Công việc cụ thể đang và sẽ thực hiện theo từng đợt chạy nước rút.
*   [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Thiết kế kiến trúc và mô tả luồng dữ liệu.
*   [DECISIONS.md](docs/DECISIONS.md) - Ghi nhận các quyết định kỹ thuật quan trọng.
*   [TASKS.md](docs/TASKS.md) - Bảng quản trị nhiệm vụ (To-Do, In Progress, Done).
*   [CHANGELOG.md](docs/CHANGELOG.md) - Lịch sử thay đổi hệ thống.

---

## 🚀 Hướng Dẫn Khởi Đầu (Quick Start)

### 1. Chuẩn bị môi trường Python
Yêu cầu Python 3.10 trở lên. Khởi tạo môi trường ảo và kích hoạt:

```powershell
# Khởi tạo virtual environment
python -m venv .venv

# Kích hoạt venv (trên Windows PowerShell)
.venv\Scripts\Activate.ps1

# Nâng cấp pip và cài đặt thư viện cần thiết
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Cấu hình dự án
Tất cả các tham số cấu hình được đặt tại `configs/default.yaml`. Bạn có thể sao chép cấu hình và điều chỉnh cho phù hợp.

### 3. Chạy thử nghiệm
Khi hoàn tất thiết lập Phase 0, khởi chạy dự án để xác minh log và cấu hình:

```powershell
python -m src.main
```
