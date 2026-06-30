import os
import asyncio
from src.utils.logger import logger
from src.utils.config import config

class TTSProvider:
    def __init__(self):
        # Default config settings
        self.default_voice = config.get("voice.voice_name", "vi-VN-HoaiMyNeural")
        self.default_rate = config.get("voice.speed", "+0%")
        self.default_pitch = config.get("voice.pitch", "+0Hz")
        self.default_output_dir = config.get("voice.output_dir", "assets/audio")

        # Create output directory
        if not os.path.exists(self.default_output_dir):
            os.makedirs(self.default_output_dir)

    async def generate_async(self, text: str, output_path: str = None, voice_name: str = None, rate: str = None, pitch: str = None) -> str:
        """
        Asynchronously generates speech from text using edge-tts.
        """
        import edge_tts

        voice = voice_name or self.default_voice
        rate_str = rate or self.default_rate
        pitch_str = pitch or self.default_pitch

        if not output_path:
            # Generate a default filename if not provided
            safe_text = "".join([c if c.isalnum() else "_" for c in text[:15]])
            output_path = os.path.join(self.default_output_dir, f"tts_{safe_text}.mp3")

        # Ensure directory of output path exists
        out_dir = os.path.dirname(output_path)
        if out_dir and not os.path.exists(out_dir):
            os.makedirs(out_dir)

        log_preview = f"'{text[:30]}...'" if len(text) > 30 else f"'{text}'"
        logger.info(f"Generating TTS for text: {log_preview} using voice: {voice}, rate: {rate_str}, pitch: {pitch_str}")
        
        try:
            communicate = edge_tts.Communicate(text, voice, rate=rate_str, pitch=pitch_str)
            await communicate.save(output_path)
            logger.info(f"Speech audio successfully generated at: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error generating speech audio via edge-tts: {e}")
            raise  # Bare raise to preserve original traceback

    def generate(self, text: str, output_path: str = None, voice_name: str = None, rate: str = None, pitch: str = None) -> str:
        """
        Synchronous wrapper to generate speech from text.
        Uses asyncio.run() for clean event loop management (Python 3.10+ compatible).
        """
        return asyncio.run(
            self.generate_async(text, output_path, voice_name, rate, pitch)
        )

    async def stream_async(self, text: str, voice_name: str = None, rate: str = None, pitch: str = None):
        """
        Asynchronously streams audio chunks.
        """
        import edge_tts
        voice = voice_name or self.default_voice
        rate_str = rate or self.default_rate
        pitch_str = pitch or self.default_pitch

        communicate = edge_tts.Communicate(text, voice, rate=rate_str, pitch=pitch_str)
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                yield chunk["data"]

# Create a singleton instance
tts_provider = TTSProvider()
