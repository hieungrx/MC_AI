# Phase 5: Cloud Deployment

## 🎯 Mục Tiêu
Đưa hệ thống lên máy chủ đám mây (GPU Cloud), giải phóng tài nguyên máy tính cá nhân. Đảm bảo hệ thống có thể chạy ổn định, tự động phát trực tiếp 24/7 mà không phụ thuộc vào trạng thái bật/tắt của laptop cá nhân.

## 📋 Phạm Vi Công Việc (Scope)
1.  **Lựa chọn hạ tầng Cloud**:
    *   Đánh giá các nhà cung cấp GPU Cloud (RunPod, Vast.ai, Google Cloud Platform, AWS, v.v.).
    *   Chọn hệ điều hành phù hợp: Windows Server (dễ tích hợp OBS GUI) hoặc Ubuntu (tiết kiệm tài nguyên, phù hợp cho headless FFmpeg/Docker).
2.  **Cài đặt & Cấu hình môi trường trên Cloud**:
    *   Cài đặt driver GPU NVIDIA, CUDA Toolkit.
    *   Cài đặt OBS Studio (Headless/Virtual Framebuffer nếu dùng Linux) hoặc FFmpeg.
    *   Cài đặt Python environment và các thư viện học máy cần thiết.
3.  **Điều khiển từ xa (Remote Control)**:
    *   Thiết lập SSH, RDP hoặc giao diện Web UI đơn giản để giám sát trạng thái stream từ xa.

## 🏆 Definition of Done (DoD)
*   [ ] Toàn bộ mã nguồn và mô hình AI được triển khai và cấu hình thành công trên Cloud Server.
*   [ ] Hệ thống thực hiện phát livestream thành công từ máy chủ Cloud.
*   [ ] Đóng kết nối máy tính cá nhân (tắt laptop), phiên livestream vẫn tiếp tục chạy bình thường trên Cloud Server.
