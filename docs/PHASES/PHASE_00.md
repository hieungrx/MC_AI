# Phase 0: Project Foundation

## 🎯 Mục Tiêu
Thiết lập nền móng kỹ thuật vững chắc cho dự án AI MC, đảm bảo môi trường phát triển nhất quán, hệ thống cấu hình linh hoạt, ghi log chuẩn mực và cấu trúc thư mục rõ ràng.

## 📋 Phạm Vi Công Việc (Scope)
1.  **Khởi tạo Git**: Thiết lập repository cục bộ, cấu hình tệp `.gitignore` chuẩn cho Python.
2.  **Cấu trúc thư mục**: Thiết lập các thư mục chức năng chính (`src`, `tests`, `configs`, `docs`, `scripts`, `assets`).
3.  **Python Environment**: Khởi tạo Virtual Environment (`.venv`), cấu hình trình quản lý dependency.
4.  **Logging**: Viết module quản lý log chuẩn, ghi log ra console và lưu tệp xoay vòng (rotating file logs).
5.  **Config System**: Xây dựng cơ chế tải cấu hình linh hoạt (YAML/JSON) hỗ trợ nhiều môi trường (development, production).
6.  **Tài liệu cơ bản**: Cập nhật `README.md` hướng dẫn cài đặt ban đầu, thiết lập hệ thống tài liệu quản lý dự án (`docs/`).

## 🏆 Definition of Done (DoD)
*   [ ] Cấu trúc thư mục được tạo đầy đủ.
*   [ ] Virtual Environment hoạt động ổn định và các thư viện nền tảng được cài đặt.
*   [ ] Khởi chạy được dự án thông qua script/lệnh chính mà không gặp lỗi (`python -m src.main` hoặc tương tự).
*   [ ] Hệ thống Log ghi nhận đúng định dạng và ghi ra file.
*   [ ] Config load chính xác cấu hình từ tệp cấu hình mẫu.
*   [ ] Repository Git sạch sẽ, `.gitignore` không bị sót các file rác hay file môi trường ảo.
