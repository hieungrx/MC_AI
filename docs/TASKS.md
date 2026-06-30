# Project Tasks List (TASKS.md)

Tài liệu này theo dõi chi tiết tất cả các đầu việc trong dự án, được chia nhóm theo trạng thái hiện tại.

---

## 🎯 Việc Cần Làm Ngay (To-Do) - Sprint 02

*Không còn việc nào.*

---

## 🏃 Đang Thực Hiện (In Progress)

*Không còn việc nào.*

---

## ✅ Đã Hoàn Thành (Done)

- [x] **TS02-01**: Khảo sát và lựa chọn mô hình Lip Sync (Wav2Lip vs LivePortrait/SadTalker).
- [x] **TS02-02**: Cài đặt các thư viện Deep Learning (PyTorch, OpenCV, v.v.) vào `.venv`.
- [x] **TS02-03**: Tải checkpoint/trọng số của mô hình Lip Sync đã chọn.
- [x] **TS02-04**: Viết module xử lý hình ảnh & sinh video `src/avatar/lip_sync.py`.
- [x] **TS02-05**: Viết script chạy thử nghiệm `scripts/test_avatar.py` tạo `hello_avatar.mp4`.
- [x] **TS02-06**: Tối ưu hóa thời gian xử lý render video.
- [x] **TS01-01**: Khảo sát và lựa chọn thư viện/API TTS (Edge-TTS).
- [x] **TS01-02**: Cài đặt các thư viện Python bổ trợ cho âm thanh và TTS vào `.venv`.
- [x] **TS01-03**: Viết module sinh giọng đọc `src/voice/tts.py` hỗ trợ cấu hình giọng đọc, tốc độ, cao độ.
- [x] **TS01-04**: Viết script chạy thử nghiệm `scripts/test_tts.py` để sinh ra file `hello.mp3`.
- [x] **TS01-05**: Thiết lập cấu hình chuyên biệt cho TTS trong `configs/default.yaml`.
- [x] **TS01-06**: Nghiên cứu và hiện thực phương án phát luồng âm thanh (audio streaming) dạng chunks.
- [x] **TS00-01**: Thiết lập cấu trúc thư mục của dự án và khởi tạo hệ thống tài liệu quản lý (`docs/`).
- [x] **TS00-02**: Khởi tạo Git repository và commit các file tài liệu ban đầu.
- [x] **TS00-03**: Khởi tạo môi trường ảo Python (`.venv`) và cài đặt các thư viện cơ bản.
- [x] **TS00-04**: Thiết lập module logging hệ thống (`src/utils/logger.py`).
- [x] **TS00-05**: Thiết lập module đọc cấu hình YAML (`src/utils/config.py`).
- [x] **TS00-06**: Tạo file chạy thử chính `src/main.py` kết nối logger và config.
- [x] **TS00-07**: Hoàn thiện `README.md` hướng dẫn sử dụng và khởi chạy.
- [x] **Setup tài liệu cơ sở**: Tạo [ROADMAP.md](ROADMAP.md), các phase từ [PHASE_00.md](PHASES/PHASE_00.md) đến [PHASE_06.md](PHASES/PHASE_06.md), [SPRINT_00.md](SPRINTS/SPRINT_00.md), [DECISIONS.md](DECISIONS.md) và [ARCHITECTURE.md](ARCHITECTURE.md).
