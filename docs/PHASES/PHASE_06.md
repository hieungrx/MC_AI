# Phase 6: Optimization

## 🎯 Mục Tiêu
Tối ưu hóa toàn diện hiệu năng của hệ thống nhằm đảm bảo khả năng chạy liên tục 24/7 (hoặc nhiều ngày liền) mà không gặp sự cố crash, tràn bộ nhớ (memory leak) hay sụt giảm khung hình (drop frames).

## 📋 Phạm Vi Công Việc (Scope)
1.  **Tối ưu tài nguyên hệ thống (Resource Optimization)**:
    *   Tối ưu sử dụng CPU/GPU/RAM của các tiến trình render video và sinh âm thanh.
    *   Tìm và khắc phục các hiện tượng rò rỉ bộ nhớ (Memory Leak) trong mã nguồn Python hoặc thư viện đồ họa.
2.  **Tối ưu luồng Stream (Bitrate & FPS)**:
    *   Điều chỉnh cấu hình mã hóa (Encoder) để giữ khung hình ổn định ở mức 30/60 FPS.
    *   Cân bằng giữa băng thông (Bitrate) và chất lượng hình ảnh để không bị nghẽn mạng.
3.  **Tự động khôi phục lỗi (Error Recovery & Auto-Restart)**:
    *   Xây dựng cơ chế giám sát (Watchdog) phát hiện nếu tiến trình stream hoặc tiến trình sinh nội dung bị đơ/treo.
    *   Tự động khởi động lại (Auto Restart) tiến trình bị lỗi và tiếp tục stream từ phân đoạn gần nhất mà không làm ngắt quãng livestream quá lâu.

## 🏆 Definition of Done (DoD)
*   [ ] Hệ thống hoàn thành bài kiểm thử chạy liên tục **24 giờ** không crash, không bị sụt giảm chất lượng stream rõ rệt.
*   [ ] Có cơ chế tự động reconnect và tự động restart khi gặp sự cố mạng hoặc lỗi runtime.
*   [ ] Tài nguyên sử dụng (RAM, VRAM) duy trì ở mức ổn định, không tăng tiến theo thời gian.
