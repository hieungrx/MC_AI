# Phase 3: Streaming

## 🎯 Mục Tiêu
Truyền tải video sinh ra từ Phase 2 trực tiếp lên các nền tảng mạng xã hội (TikTok, Facebook, YouTube) bằng cách cấu hình OBS Studio hoặc phát trực tiếp thông qua luồng FFmpeg/RTMP.

## 📋 Phạm Vi Công Việc (Scope)
1.  **Tích hợp OBS Studio**:
    *   Tự động hóa OBS thông qua WebSocket (`obs-websocket-py`).
    *   Tự động tạo các Scene (cảnh livestream), thiết lập nguồn (Media Source, Window Capture, v.v.).
2.  **Cấu hình luồng truyền tải (RTMP)**:
    *   Sử dụng giao thức RTMP để đẩy luồng video/audio lên máy chủ livestream.
    *   Quản lý Stream Key linh hoạt thông qua file cấu hình.
3.  **Hỗ trợ Multistream (Đa kênh)**:
    *   Nghiên cứu cơ chế đẩy luồng lên nhiều nền tảng cùng lúc (YouTube + Facebook + TikTok).
    *   Sử dụng giải pháp phần mềm trung gian hoặc chạy nhiều tiến trình đẩy luồng song song.

## 🏆 Definition of Done (DoD)
*   [ ] Hệ thống có khả năng tự động mở OBS, cấu hình đúng Scene chứa luồng phát của MC ảo.
*   [ ] Livestream phát sóng thành công lên ít nhất một nền tảng thử nghiệm (ví dụ: YouTube Sandbox hoặc tài khoản cá nhân).
*   [ ] Thử nghiệm phát sóng liên tục trong **30 phút** không có hiện tượng mất kết nối, giật lag hay crash hệ thống.
