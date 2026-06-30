# Phase 1: AI Voice

## 🎯 Mục Tiêu
Phát triển module **AI Voice** có nhiệm vụ chuyển đổi các kịch bản văn bản (Text) thành các tệp âm thanh (Audio) chất lượng cao sử dụng công nghệ Text-to-Speech (TTS), hỗ trợ lưu trữ tệp và truyền phát (streaming) âm thanh.

## 📋 Phạm Vi Công Việc (Scope)
1.  **Nghiên cứu & Chọn lựa TTS**:
    *   Thử nghiệm các dịch vụ Cloud TTS (Google Cloud TTS, Edge TTS, ElevenLabs, FPT.AI, v.v.).
    *   Đánh giá các giải pháp offline/open-source (coqui-tts, XTTS, v.v.) nếu cần chạy nội bộ.
2.  **Thử nghiệm giọng đọc**:
    *   Lọc chọn các giọng đọc tiếng Việt tự nhiên, phù hợp với vai trò MC livestream.
    *   Điều chỉnh các thông số: tốc độ (speed), cao độ (pitch), ngữ điệu.
3.  **Lưu trữ Output**:
    *   Module xuất ra tệp định dạng âm thanh tiêu chuẩn (`.mp3`, `.wav`).
    *   Tự động đặt tên và quản lý tệp âm thanh sinh ra trong thư mục lưu trữ đệm (buffer/cache).
4.  **Streaming Audio (Nâng cao)**:
    *   Hỗ trợ stream luồng âm thanh trực tiếp (byte stream) để giảm độ trễ chuẩn bị cho các bước tiếp theo.

## 🏆 Definition of Done (DoD)
*   [ ] Đã tích hợp thành công ít nhất một thư viện/API TTS vào mã nguồn dự án.
*   [ ] Có công cụ/script kiểm thử tự động nhận đầu vào là văn bản tiếng Việt và xuất ra tệp âm thanh nghe rõ ràng, tự nhiên.
*   [ ] Hỗ trợ cấu hình lựa chọn giọng đọc từ file config.
*   [ ] Có tài liệu đánh giá và lựa chọn giải pháp TTS tối ưu nhất trong file `docs/DECISIONS.md`.
