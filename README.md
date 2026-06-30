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

**Cấu hình bảo mật (Secrets):** Mật khẩu OBS và Stream Key được đọc từ biến môi trường, không lưu trực tiếp trong file config:
```powershell
# Thiết lập biến môi trường trước khi chạy
$env:OBS_PASSWORD = "your_obs_password"
$env:STREAM_KEY = "your_stream_key"
```

### 3. Chạy Demo (Text → Voice → Avatar Video)

Đây là pipeline chính để tạo video MC ảo nói chuyện từ kịch bản text:

```powershell
python demo.py
```

Bạn có thể:
- Nhấn **Enter** để dùng kịch bản mặc định.
- Nhập **đường dẫn file** chứa kịch bản (ví dụ: `configs/script_quan_tay.txt`).
- Nhập **trực tiếp** kịch bản trên một dòng.

Video đầu ra sẽ được lưu tại `assets/video/demo_avatar.mp4`.

### 4. Chạy xác minh Phase 0 (Foundation)

Kiểm tra hệ thống log và cấu hình:

```powershell
python -m src.main
```

### 5. Chạy Test Scripts

```powershell
# Test Text-to-Speech
python scripts/test_tts.py

# Test TTS Streaming
python scripts/test_tts_stream.py

# Test Avatar Generation
python scripts/test_avatar.py
```

---

## 📋 Yêu Cầu Hệ Thống

- **Python**: 3.10+
- **FFmpeg**: Cần cài đặt để merge audio/video. Cài qua `winget install ffmpeg` trên Windows.
- **OS**: Windows 10/11 (đã kiểm thử). Có thể chạy trên macOS/Linux.

---

## 📁 Cấu Trúc Thư Mục

```
AI_MC/
├── assets/            # Tài nguyên (audio, video, avatar)
├── configs/           # File cấu hình YAML và kịch bản
├── docs/              # Tài liệu dự án
├── logs/              # File log ứng dụng
├── scripts/           # Script kiểm thử thủ công
├── src/               # Mã nguồn chính
│   ├── avatar/        # Module đồng bộ khẩu hình (lip sync)
│   ├── automation/    # Module tự động hóa (coming soon)
│   ├── streaming/     # Module phát trực tiếp (coming soon)
│   ├── utils/         # Tiện ích (config, logger)
│   └── voice/         # Module Text-to-Speech
├── tests/             # Unit tests
├── demo.py            # Pipeline demo chính
├── pyproject.toml     # Cấu hình package Python
└── requirements.txt   # Danh sách thư viện phụ thuộc
```
