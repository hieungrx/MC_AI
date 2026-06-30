# Sprint 00: Project Foundation

*   **Phase liên quan**: [Phase 0: Project Foundation](../PHASES/PHASE_00.md)
*   **Thời gian**: 30/06/2026 - 02/07/2026
*   **Trạng thái**: Đã Hoàn Thành

## 🎯 Mục Tiêu Sprint
Xây dựng nền móng dự án ổn định bao gồm: môi trường ảo Python, hệ thống log, hệ thống nạp cấu hình và cấu trúc thư mục tiêu chuẩn của dự án AI MC.

## 📋 Danh sách Task (Tasks List)

| Task ID | Mô tả Task | Độ ưu tiên | Người thực hiện | Trạng thái | Ghi chú |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TS00-01** | Tạo cấu trúc thư mục dự án và tệp `.gitignore` | High | AI Agent | **Đã Hoàn Thành** | Đã tạo thư mục và docs |
| **TS00-02** | Khởi tạo Git repository | High | AI Agent | **Đã Hoàn Thành** | Đã khởi tạo và commit |
| **TS00-03** | Tạo Virtual Environment (`.venv`) và cấu hình pip | High | AI Agent | **Đã Hoàn Thành** | Đã cấu hình `.venv` |
| **TS00-04** | Thiết lập Module Logging (`src/utils/logger.py`) | High | AI Agent | **Đã Hoàn Thành** | Logging hoạt động tốt |
| **TS00-05** | Thiết lập Module Config System (`src/utils/config.py`) | High | AI Agent | **Đã Hoàn Thành** | Config load YAML và fallback ok |
| **TS00-06** | Tạo tệp khởi chạy chính `src/main.py` | High | AI Agent | **Đã Hoàn Thành** | Tệp main khởi chạy thành công |
| **TS00-07** | Hoàn thiện tài liệu `README.md` và `docs/` | Medium | AI Agent | **Đã Hoàn Thành** | Hướng dẫn cài đặt & sitemap hoàn tất |

## 🏆 Definition of Done (DoD) cho Sprint này
1.  [x] Chạy lệnh `python -m src.main` in ra dòng log chào mừng dự án và hiển thị các giá trị cấu hình được nạp thành công từ `configs/default.yaml`.
2.  [x] File log được tạo tự động tại thư mục `logs/` dạng rotating file (ví dụ `logs/app.log`).
3.  [x] Git repository sạch sẽ và bỏ qua đúng các tệp môi trường ảo, tệp log, cache.
