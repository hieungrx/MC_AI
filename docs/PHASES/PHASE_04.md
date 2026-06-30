# Phase 4: Automation

## 🎯 Mục Tiêu
Loại bỏ hoàn toàn các thao tác thủ công bằng tay. Hệ thống tự động đọc thông tin sản phẩm (Product JSON), tạo kịch bản (Script), chuyển thành giọng nói (Voice), dựng hình (Avatar) và phát sóng (OBS) theo một lịch trình định sẵn hoặc vòng lặp vô tận.

## 📋 Phạm Vi Công Việc (Scope)
1.  **Cơ sở dữ liệu sản phẩm & Kịch bản (Product & Script System)**:
    *   Tải thông tin sản phẩm từ file cấu hình JSON hoặc API cửa hàng.
    *   Sử dụng AI/LLM để tự động sinh kịch bản giới thiệu sản phẩm ngẫu nhiên hoặc theo template.
2.  **Bộ lập lịch & Hàng đợi (Scheduler & Playlist Manager)**:
    *   Xây dựng danh sách phát (Playlist) các phân đoạn livestream.
    *   Lập lịch phát sóng, chèn quảng cáo, đổi sản phẩm theo thời gian (Timer).
3.  **Vòng lặp tự động (Loop System)**:
    *   Cho phép luồng chạy liên tục bằng cách tự động sinh nội dung mới trước khi phân đoạn cũ kết thúc.
    *   Tự động giải phóng các tệp tạm (file audio, video cũ) để tránh đầy ổ đĩa.

## 🏆 Definition of Done (DoD)
*   [ ] Chỉ cần chạy 1 lệnh khởi chạy duy nhất để khởi động toàn bộ dây chuyền (từ gen script -> gen voice -> gen video -> stream).
*   [ ] Hệ thống tự chuyển cảnh, chuyển sản phẩm và giới thiệu sản phẩm liên tục theo danh sách cấu hình sẵn.
*   [ ] Hoạt động liên tục 2 giờ ở môi trường kiểm thử cục bộ mà không cần can thiệp thủ công.
