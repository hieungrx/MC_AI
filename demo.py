import os
import sys
from src.utils.logger import logger
from src.utils.config import config
from src.voice.tts import tts_provider
from src.avatar.lip_sync import avatar_generator

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
    print(f"Nhấn Enter để dùng kịch bản mặc định:\n> '{default_script}'")
    user_input = input("\nHoặc nhập kịch bản của riêng bạn: ").strip()
    
    script_text = user_input if user_input else default_script

    # Step 2: Define Output paths
    audio_output = "assets/audio/demo_voice.mp3"
    video_output = "assets/video/demo_avatar.mp4"
    face_image = "assets/avatar/mc_default.png"

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
