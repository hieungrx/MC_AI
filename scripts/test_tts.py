import os
import sys

# Add project root to sys.path to allow imports from src
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.utils.logger import logger
from src.voice.tts import tts_provider

def run_test():
    """
    Test script to verify edge-tts integrations.
    Generates a default 'hello.mp3' file in the assets/audio/ directory.
    """
    logger.info("Starting TTS test script...")
    
    test_text = "Xin chào, tôi là MC ảo của hệ thống tự động livestream. Rất vui được gặp các bạn!"
    output_file = "assets/audio/hello.mp3"
    
    try:
        # Generate audio using synchronous wrapper
        result_path = tts_provider.generate(test_text, output_file)
        
        # Verify file creation
        if os.path.exists(result_path):
            file_size = os.path.getsize(result_path)
            logger.info(f"Test SUCCESSFUL! File generated at: {result_path} ({file_size} bytes)")
            return 0
        else:
            logger.error("Test FAILED! File was not created.")
            return 1
    except Exception as e:
        logger.error(f"Test FAILED with exception: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(run_test())
