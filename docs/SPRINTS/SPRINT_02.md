# Sprint 02: Avatar & Lip Sync Integration

*   **Phase liên quan**: [Phase 2: Avatar](../PHASES/PHASE_02.md)
*   **Thời gian**: 06/07/2026 - 12/07/2026
*   **Trạng thái**: Chuẩn Bị

## 🎯 Mục Tiêu Sprint
Xây dựng module Avatar nhận đầu vào là ảnh chân dung MC + file âm thanh (từ Phase 1) để tạo ra video nói chuyện (`.mp4`) có khẩu hình miệng khớp với âm thanh (Lip Sync) và chuyển động tự nhiên.

## 📋 Danh sách Task (Tasks List)

| Task ID | Mô tả Task | Độ ưu tiên | Người thực hiện | Trạng thái | Ghi chú |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TS02-01** | Khảo sát và lựa chọn mô hình Lip Sync (Ưu tiên Wav2Lip cho gọn nhẹ hoặc LivePortrait/SadTalker cho biểu cảm) | High | AI Agent | *To-Do* | Cập nhật quyết định vào `docs/DECISIONS.md` |
| **TS02-02** | Cài đặt các thư viện Deep Learning (PyTorch, OpenCV, v.v.) vào `.venv` | High | AI Agent | *To-Do* | Cần kiểm tra cấu hình GPU / CUDA nếu có |
| **TS02-03** | Tải checkpoint/trọng số (weights) của mô hình Lip Sync đã chọn và lưu vào thư mục dự án | High | AI Agent | *To-Do* | Cần thiết lập thư mục lưu checkpoint |
| **TS02-04** | Viết module xử lý hình ảnh & sinh video `src/avatar/lip_sync.py` | High | AI Agent | *To-Do* | Module xử lý chính của Phase 2 |
| **TS02-05** | Viết script chạy thử nghiệm `scripts/test_avatar.py` kết hợp `hello.mp3` với ảnh MC để tạo video `hello_avatar.mp4` | Medium | AI Agent | *To-Do* | Dùng làm file test kiểm tra kết quả |
| **TS02-06** | Tối ưu hóa thời gian xử lý render video (như chia nhỏ phân đoạn, caching các frame tĩnh) | Low | AI Agent | *To-Do* | Tối ưu hóa hiệu năng |

## 🏆 Definition of Done (DoD) cho Sprint này
1.  Đã cấu hình được môi trường chạy PyTorch (sử dụng CUDA nếu có GPU).
2.  Chạy script kiểm thử nhận vào tệp âm thanh + hình ảnh MC và xuất ra tệp video `hello_avatar.mp4` thành công.
3.  Video kết quả có khẩu hình miệng khớp chính xác với âm thanh phát ra, không bị lệch hoặc đơ.
4.  Tất cả mã nguồn mới được lưu trữ và đẩy lên Git repository.
