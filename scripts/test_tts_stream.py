import os
import sys
import asyncio

# Add project root to sys.path to allow imports from src
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.utils.logger import logger
from src.voice.tts import tts_provider

async def run_stream_test():
    logger.info("Starting TTS streaming test script...")
    
    test_text = "Thử nghiệm truyền phát âm thanh trực tiếp theo luồng."
    chunk_count = 0
    total_bytes = 0
    
    try:
        async for chunk in tts_provider.stream_async(test_text):
            chunk_count += 1
            total_bytes += len(chunk)
            if chunk_count <= 3:
                logger.info(f"Received chunk {chunk_count}: {len(chunk)} bytes")
        
        logger.info(f"Stream test completed. Received {chunk_count} chunks, total {total_bytes} bytes.")
        if total_bytes > 0:
            logger.info("Streaming test SUCCESSFUL!")
            return 0
        else:
            logger.error("Streaming test FAILED! No bytes received.")
            return 1
    except Exception as e:
        logger.error(f"Streaming test FAILED with exception: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(run_stream_test()))
