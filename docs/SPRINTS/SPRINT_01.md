# Sprint 01: AI Voice Development

*   **Phase liên quan**: [Phase 1: AI Voice](../PHASES/PHASE_01.md)
*   **Thời gian**: 01/07/2026 - 05/07/2026
*   **Trạng thái**: Chuẩn Bị

## 🎯 Mục Tiêu Sprint
Xây dựng thành công module phát sinh giọng nói từ văn bản (TTS), xuất ra tệp âm thanh định dạng `.mp3`/`.wav` chất lượng cao, tự nhiên và sẵn sàng tích hợp với avatar.

## 📋 Danh sách Task (Tasks List)

| Task ID | Mô tả Task | Độ ưu tiên | Người thực hiện | Trạng thái | Ghi chú |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TS01-01** | Khảo sát và lựa chọn thư viện/API TTS (Ưu tiên Edge-TTS hoặc Google Cloud TTS) | High | AI Agent | *To-Do* | Cần tạo tài liệu quyết định trong `DECISIONS.md` |
| **TS01-02** | Cài đặt các thư viện Python bổ trợ cho âm thanh và TTS vào `.venv` | High | AI Agent | *To-Do* | Thêm vào `requirements.txt` |
| **TS01-03** | Viết module sinh giọng đọc `src/voice/tts.py` hỗ trợ cấu hình giọng đọc, tốc độ, cao độ | High | AI Agent | *To-Do* | Module xử lý chính |
| **TS01-04** | Viết script chạy thử nghiệm `scripts/test_tts.py` để sinh ra file `hello.mp3` | Medium | AI Agent | *To-Do* | Dùng làm tệp kiểm tra |
| **TS01-05** | Thiết lập cấu hình chuyên biệt cho TTS trong `configs/default.yaml` | Medium | AI Agent | *To-Do* | Đồng bộ hóa tham số cấu hình |
| **TS01-06** | Nghiên cứu và hiện thực phương án phát luồng âm thanh (audio streaming) dạng chunks | Low | AI Agent | *To-Do* | Chuẩn bị cho tích hợp realtime |

## 🏆 Definition of Done (DoD) cho Sprint này
1.  Đã cài đặt đầy đủ các package cần thiết trong `.venv`.
2.  Chạy script kiểm thử tạo ra được tệp âm thanh phát tiếng Việt rõ ràng, tự nhiên từ một đoạn văn bản đầu vào.
3.  Thông tin cấu hình (giọng đọc, tốc độ) được nạp trực tiếp từ `configs/default.yaml`.
4.  Tất cả mã nguồn mới được đẩy lên Git repository.
