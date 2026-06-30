import os
import sys
from pathlib import Path

# Add project root to sys.path to allow imports from src
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.utils.logger import logger
from src.utils.config import config
from src.voice.tts import tts_provider
from src.avatar.lip_sync import avatar_generator


def _read_script_file(file_path: str) -> str:
    """
    Reads script text from a file. Returns the text content or None on failure.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read().strip()
        logger.info(f"Đã đọc kịch bản thành công từ file: {file_path}")
        return text
    except Exception as e:
        logger.error(f"Không thể đọc file {file_path}: {e}")
        return None


def run_pipeline_demo():
    banner = """
    ==================================================
    *                                                *
    *          AI MC LIVE STREAM - DEMO PIPELINE     *
    *            Phase 1 (Voice) & Phase 2 (Avatar)  *
    *                                                *
    ==================================================
    """
    print(banner)
    logger.info("Starting AI MC Pipeline Demo...")

    # Step 1: Input Script Text
    default_script = (
        "Xin chào mọi người! Chào mừng các bạn đã đến với chương trình Livestream tự động của tôi. "
        "Hôm nay chúng ta sẽ khám phá những sản phẩm công nghệ mới nhất. Hãy nhấn tim và chia sẻ buổi live nhé!"
    )
    
    print("\n--- NHẬP KỊCH BẢN CHO MC ---")
    print(f"1. Nhấn Enter để dùng kịch bản mặc định.")
    print(f"2. Nhập đường dẫn file chứa kịch bản (ví dụ: configs/script_quan_tay.txt).")
    print(f"3. Nhập trực tiếp kịch bản trên một dòng.")
    user_input = input("\nNhập lựa chọn của bạn: ").strip()
    
    script_text = default_script
    if user_input:
        # Check if user input is a file path
        if os.path.exists(user_input):
            result = _read_script_file(user_input)
            script_text = result if result else user_input
        else:
            # Check if it exists in configs directory
            config_try = os.path.join("configs", user_input)
            if os.path.exists(config_try):
                result = _read_script_file(config_try)
                script_text = result if result else user_input
            else:
                script_text = user_input

    # Step 2: Define Output paths
    audio_output = config.get("voice.output_dir", "assets/audio") + "/demo_voice.mp3"
    video_output = config.get("avatar.output_dir", "assets/video") + "/demo_avatar.mp4"
    face_image = config.get("avatar.default_face", "assets/avatar/mc_default.png")

    # Step 3: Run TTS (Text -> Audio)
    print("\n[Bước 1/2] Đang chuyển đổi kịch bản thành giọng nói MC (Text-to-Speech)...")
    try:
        audio_path = tts_provider.generate(script_text, audio_output)
        logger.info(f"Đã tạo file âm thanh: {audio_path}")
    except Exception as e:
        logger.error(f"Lỗi khi tạo giọng nói: {e}")
        return 1

    # Step 4: Run Lip Sync (Audio + Image -> Video)
    print("\n[Bước 2/2] Đang đồng bộ khẩu hình và dựng video MC ảo nói chuyện...")
    try:
        video_path = avatar_generator.generate_video(
            audio_path=audio_path,
            face_image_path=face_image,
            output_path=video_output
        )
        logger.info(f"Đã tạo video MC ảo: {video_path}")
    except Exception as e:
        logger.error(f"Lỗi khi dựng video Avatar: {e}")
        return 1

    print("\n==================================================")
    print(" 🎉 HỆ THỐNG ĐÃ TẠO DEMO THÀNH CÔNG!")
    print("==================================================")
    print(f" 🔊 File âm thanh: {os.path.abspath(audio_path)}")
    print(f" 🎬 Video MC nói chuyện: {os.path.abspath(video_path)}")
    print("\n Bạn có thể mở video trên để kiểm tra khẩu hình và giọng đọc của MC ảo.")
    print("==================================================")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(run_pipeline_demo())
    except KeyboardInterrupt:
        print("\nDemo đã bị dừng bởi người dùng.")
        sys.exit(0)
