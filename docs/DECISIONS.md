# Technical Decisions Log (DECISIONS.md)

Tài liệu này lưu trữ các quyết định kỹ thuật quan trọng của dự án AI MC, kèm theo bối cảnh và lý do lựa chọn.

---

## 📅 [30/06/2026] DEC-001: Lựa chọn cấu trúc quản lý tài liệu dự án bằng Antigravity CLI

*   **Trạng thái**: Đã Quyết Định
*   **Người đề xuất**: USER / AI Agent
*   **Bối cảnh**: Dự án cần một cách thức theo dõi roadmap, các phase phát triển, sprints và các quyết định kỹ thuật một cách tường minh để AI Agent có thể đọc hiểu và thực hiện đúng tiến độ.
*   **Quyết định**: Sử dụng thư mục `docs/` chứa:
    *   `ROADMAP.md` quản lý bức tranh lớn.
    *   Thư mục `PHASES/` quản lý mục tiêu từng phase.
    *   Thư mục `SPRINTS/` quản lý chi tiết task từng sprint.
    *   `DECISIONS.md`, `ARCHITECTURE.md`, `TASKS.md`, `CHANGELOG.md` để theo dõi tiến độ và thiết kế.
*   **Hậu quả / Tác động**: Tài liệu sẽ được cập nhật liên tục qua mỗi sprint, đảm bảo tính nhất quán cao.

---

## 📅 [30/06/2026] DEC-002: Lựa chọn trình quản lý môi trường ảo mặc định (venv + pip)

*   **Trạng thái**: Đã Quyết Định
*   **Người đề xuất**: AI Agent (tuân thủ Skill `managing-python-dependencies`)
*   **Bối cảnh**: Khởi chạy dự án Python từ đầu cần chọn trình quản lý dependencies. Do dự án trống, chúng ta áp dụng quy tắc mặc định để tối giản và tương thích tốt trên môi trường Windows của người dùng.
*   **Quyết định**: Sử dụng module `venv` tích hợp sẵn của Python tạo thư mục `.venv` và quản lý gói qua `.venv\Scripts\pip`. Ghi nhận các package đã cài đặt vào `requirements.txt`.
*   **Hậu quả / Tác động**: Tránh xung đột thư viện với môi trường global của hệ thống.

---

## 📅 [01/07/2026] DEC-003: Lựa chọn Edge-TTS làm giải pháp Text-to-Speech (TTS) cho MVP

*   **Trạng thái**: Đã Quyết Định
*   **Người đề xuất**: AI Agent
*   **Bối cảnh**: Cần một giải pháp TTS chuyển đổi kịch bản văn bản thành giọng đọc tiếng Việt tự nhiên, nhanh chóng và dễ triển khai, không yêu cầu thủ tục đăng ký API Key phức tạp hoặc chi phí cao trong giai đoạn phát triển ban đầu.
*   **Quyết định**: Lựa chọn thư viện `edge-tts` (sử dụng dịch vụ TTS của Microsoft Edge qua giao thức websocket).
*   **Lý do lựa chọn**:
    *   **Miễn phí & Không cần API Key**: Rất tiện lợi cho việc phát triển và thử nghiệm cục bộ.
    *   **Giọng nói tự nhiên**: Hỗ trợ các giọng đọc Neural chất lượng cao của Microsoft như `vi-VN-HoaiMyNeural` (nữ) và `vi-VN-NamMinhNeural` (nam).
    *   **Hiệu năng tốt**: Phản hồi nhanh và hỗ trợ xuất dạng tệp âm thanh hoặc stream byte chunks trực tiếp.
*   **Hậu quả / Tác động**: Hệ thống sẽ phụ thuộc vào kết nối mạng internet để gọi dịch vụ Edge-TTS. Sau này, nếu cần hoạt động offline hoàn toàn, ta có thể bổ sung provider TTS local (như XTTS, Coqui-TTS) hoặc các Cloud API cao cấp hơn (ElevenLabs, Google TTS) nhờ thiết kế trừu tượng (Factory Pattern).

