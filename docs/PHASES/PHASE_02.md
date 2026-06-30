# Phase 2: Avatar

## 🎯 Mục Tiêu
Kết hợp luồng âm thanh từ Phase 1 với nhân vật ảo để tạo ra video MC ảo nói chuyện (Talking Head) với chuyển động môi đồng bộ chuẩn xác (Lip Sync) và cử chỉ tự nhiên.

## 📋 Phạm Vi Công Việc (Scope)
1.  **Thiết lập Nhân vật (Avatar)**:
    *   Sử dụng hình ảnh tĩnh (2D) hoặc mô hình 3D đại diện cho MC.
    *   Tích hợp công nghệ sinh chuyển động từ ảnh gốc (như SadTalker, LivePortrait, Wav2Lip, v.v.).
2.  **Đồng bộ khẩu hình (Lip Sync)**:
    *   Áp dụng các mô hình học máy để khớp khẩu hình của Avatar theo tần số âm thanh đầu vào.
3.  **Tạo cử chỉ & Biểu cảm (Animation)**:
    *   Tự động chèn các cử chỉ nhỏ như chớp mắt, gật đầu nhẹ để Avatar trông giống người thật nhất.
4.  **kết xuất Video (Video Render)**:
    *   Tối ưu hóa thời gian xử lý render video. Hỗ trợ sinh video realtime hoặc lưu trữ dạng phân đoạn ngắn.

## 🏆 Definition of Done (DoD)
*   [ ] Module nhận đầu vào là tệp âm thanh + ảnh nền/Avatar và xuất ra tệp video (`.mp4`).
*   [ ] Khẩu hình miệng của Avatar khớp chuẩn xác với nội dung âm thanh phát ra (Lip Sync hoạt động tốt).
*   [ ] Video xuất ra đạt độ phân giải tối thiểu 720p với tốc độ khung hình ổn định (từ 25-30 FPS).
