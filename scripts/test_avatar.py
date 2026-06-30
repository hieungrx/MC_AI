import os
import sys

# Add project root to sys.path to allow imports from src
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.utils.logger import logger
from src.avatar.lip_sync import avatar_generator

def run_test():
    logger.info("Starting Avatar test script...")
    
    audio_path = "assets/audio/hello.mp3"
    face_path = "assets/avatar/mc_default.png"
    output_path = "assets/video/hello_avatar.mp4"
    
    # Check if input audio exists, if not, generate a quick one
    if not os.path.exists(audio_path):
        logger.info(f"Audio file {audio_path} not found. Generating default speech first...")
        from src.voice.tts import tts_provider
        tts_provider.generate(
            "Xin chào, đây là kiểm thử đồng bộ hình ảnh đại diện với giọng nói.",
            audio_path
        )
    
    try:
        # Generate avatar video
        result_path = avatar_generator.generate_video(
            audio_path=audio_path,
            face_image_path=face_path,
            output_path=output_path
        )
        
        # Verify file creation
        if os.path.exists(result_path):
            file_size = os.path.getsize(result_path)
            logger.info(f"Avatar test SUCCESSFUL! Video generated at: {result_path} ({file_size} bytes)")
            return 0
        else:
            logger.error("Avatar test FAILED! Video was not created.")
            return 1
    except Exception as e:
        logger.error(f"Avatar test FAILED with exception: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(run_test())
