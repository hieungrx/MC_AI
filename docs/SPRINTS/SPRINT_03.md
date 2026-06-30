# Sprint 03: Live Streaming Integration

*   **Phase liên quan**: [Phase 3: Streaming](../PHASES/PHASE_03.md)
*   **Thời gian**: 13/07/2026 - 19/07/2026
*   **Trạng thái**: Chuẩn Bị

## 🎯 Mục Tiêu Sprint
Tích hợp thành công module Live Streaming, cho phép hệ thống tự động đẩy luồng video nói chuyện của MC ảo (đã tạo ở Phase 2) lên các nền tảng Livestream (như YouTube, TikTok, Facebook) thông qua giao thức RTMP (bằng OBS Studio hoặc FFmpeg).

## 📋 Danh sách Task (Tasks List)

| Task ID | Mô tả Task | Độ ưu tiên | Người thực hiện | Trạng thái | Ghi chú |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TS03-01** | Cài đặt OBS Studio (người dùng làm trên máy) và cấu hình WebSocket server | High | USER | *To-Do* | Cần OBS bản 28.0+ tích hợp sẵn WebSocket |
| **TS03-02** | Cài đặt thư viện điều khiển OBS `obs-websocket-py` vào `.venv` | High | AI Agent | *To-Do* | Cập nhật `requirements.txt` |
| **TS03-03** | Viết module kết nối và điều khiển OBS `src/streaming/obs_client.py` | High | AI Agent | *To-Do* | Module điều phối OBS Scene |
| **TS03-04** | Nghiên cứu và hiện thực giải pháp đẩy luồng trực tiếp bằng FFmpeg (RTMP Push) không cần qua OBS | Medium | AI Agent | *To-Do* | Giải pháp thay thế nhẹ hơn, phù hợp cho cloud |
| **TS03-05** | Viết script chạy livestream thử nghiệm `scripts/test_stream.py` đẩy luồng lên YouTube Sandbox hoặc Custom RTMP | High | AI Agent | *To-Do* | Kịch bản phát thử nghiệm |
| **TS03-06** | Đo đạc hiệu năng và duy trì luồng phát trong vòng 30 phút liên tục không lỗi | Medium | AI/USER | *To-Do* | Đánh giá tính ổn định |

## 🏆 Definition of Done (DoD) cho Sprint này
1.  Đã cài đặt và kết nối được với OBS Studio qua WebSocket từ code Python.
2.  Chạy script đẩy luồng livestream thành công lên nền tảng RTMP thử nghiệm (ví dụ: YouTube, Facebook ở chế độ riêng tư).
3.  Stream hoạt động liên tục trong **30 phút** ổn định, không drop frames, không lệch tiếng (audio-video sync tốt).
4.  Tất cả mã nguồn mới được lưu trữ và đẩy lên Git repository.
