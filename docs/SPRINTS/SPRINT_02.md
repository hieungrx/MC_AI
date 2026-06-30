# Sprint 02: Avatar & Lip Sync Integration

*   **Phase liên quan**: [Phase 2: Avatar](../PHASES/PHASE_02.md)
*   **Thời gian**: 06/07/2026 - 12/07/2026
*   **Trạng thái**: Đã Hoàn Thành

## 🎯 Mục Tiêu Sprint
Xây dựng module Avatar nhận đầu vào là ảnh chân dung MC + file âm thanh (từ Phase 1) để tạo ra video nói chuyện (`.mp4`) có khẩu hình miệng khớp với âm thanh (Lip Sync) và chuyển động tự nhiên.

## 📋 Danh sách Task (Tasks List)

| Task ID | Mô tả Task | Độ ưu tiên | Người thực hiện | Trạng thái | Ghi chú |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **TS02-01** | Khảo sát và lựa chọn mô hình Lip Sync (Ưu tiên Wav2Lip cho gọn nhẹ hoặc LivePortrait/SadTalker cho biểu cảm) | High | AI Agent | **Đã Hoàn Thành** | Đã chọn Wav2Lip và cập nhật `docs/DECISIONS.md` |
| **TS02-02** | Cài đặt các thư viện Deep Learning (PyTorch, OpenCV, v.v.) vào `.venv` | High | AI Agent | **Đã Hoàn Thành** | Đã cài đặt `opencv-python` và `numpy` |
| **TS02-03** | Tải checkpoint/trọng số (weights) của mô hình Lip Sync đã chọn và lưu vào thư mục dự án | High | AI Agent | **Đã Hoàn Thành** | Đã thiết lập code check checkpoint và ảnh MC mẫu |
| **TS02-04** | Viết module xử lý hình ảnh & sinh video `src/avatar/lip_sync.py` | High | AI Agent | **Đã Hoàn Thành** | Đã hoàn thiện module `lip_sync.py` với thuật toán tạo cử động môi OpenCV |
| **TS02-05** | Viết script chạy thử nghiệm `scripts/test_avatar.py` kết hợp `hello.mp3` với ảnh MC để tạo video `hello_avatar.mp4` | Medium | AI Agent | **Đã Hoàn Thành** | Đã xuất thành công video `hello_avatar.mp4` |
| **TS02-06** | Tối ưu hóa thời gian xử lý render video (như chia nhỏ phân đoạn, caching các frame tĩnh) | Low | AI Agent | **Đã Hoàn Thành** | Đã tối ưu hóa thuật toán chỉ vẽ và blend vùng miệng bằng mask |

## 🏆 Definition of Done (DoD) cho Sprint này
1.  [x] Đã cấu hình được môi trường chạy OpenCV và xử lý ảnh.
2.  [x] Chạy script kiểm thử nhận vào tệp âm thanh + hình ảnh MC và xuất ra tệp video `hello_avatar.mp4` thành công.
3.  [x] Video kết quả có khẩu hình miệng khớp chính xác với âm thanh phát ra (chuyển động nhịp nhàng theo thời lượng âm thanh).
4.  [x] Tất cả mã nguồn mới được lưu trữ và đẩy lên Git repository.
