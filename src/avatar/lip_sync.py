import os
import sys
import subprocess
import cv2
import numpy as np
from src.utils.logger import logger
from src.utils.config import config

class AvatarGenerator:
    def __init__(self):
        self.default_face = config.get("avatar.default_face", "assets/avatar/mc_default.png")
        self.output_dir = config.get("avatar.output_dir", "assets/video")
        self.fps = config.get("avatar.fps", 25)
        self.model_name = config.get("avatar.model_name", "wav2lip")
        self.checkpoint_path = "checkpoints/wav2lip.pth"

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _get_ffmpeg_command(self, name: str) -> str:
        """
        Resolves the executable name (ffmpeg or ffprobe) to an absolute path if not in system PATH.
        """
        # First check if it is available in system PATH
        try:
            subprocess.run([name, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            return name
        except Exception:
            pass

        # Try to look in WinGet folders
        username = os.environ.get("USERNAME", "Admin")
        winget_links_path = f"C:\\Users\\{username}\\AppData\\Local\\Microsoft\\WinGet\\Links\\{name}.exe"
        if os.path.exists(winget_links_path):
            return winget_links_path

        # Try another standard location (recursive look inside packages)
        packages_dir = f"C:\\Users\\{username}\\AppData\\Local\\Microsoft\\WinGet\\Packages"
        if os.path.exists(packages_dir):
            for root, dirs, files in os.walk(packages_dir):
                if f"{name}.exe" in files:
                    return os.path.join(root, f"{name}.exe")

        return name

    def _get_audio_duration(self, audio_path: str) -> float:
        """
        Retrieves the duration of the audio file in seconds.
        Attempts to use ffprobe first, then falls back to size-based heuristics.
        """
        # Try using ffprobe
        try:
            ffprobe_cmd = self._get_ffmpeg_command("ffprobe")
            cmd = [
                ffprobe_cmd, "-v", "error", "-show_entries", "format=duration",
                "-of", "default=noprint_wrappers=1:nokey=1", "-i", audio_path
            ]
            # Strip key=val if nocey is not working, on Windows we can parse output
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            output = result.stdout.strip()
            if "duration=" in output:
                output = output.split("duration=")[-1]
            return float(output)
        except Exception:
            # Fallback heuristic
            file_size = os.path.getsize(audio_path)
            if audio_path.lower().endswith(".mp3"):
                # edge-tts default is 48kbps (6000 bytes/sec)
                duration = file_size / 6000.0
                logger.info(f"ffprobe failed. Estimated MP3 duration based on file size: {duration:.2f}s")
                return max(1.0, duration)
            elif audio_path.lower().endswith(".wav"):
                # Basic WAV estimate (assume 16-bit 24kHz mono = 48000 bytes/sec)
                duration = file_size / 48000.0
                logger.info(f"ffprobe failed. Estimated WAV duration based on file size: {duration:.2f}s")
                return max(1.0, duration)
            else:
                logger.warning("Unknown audio format. Fallback duration set to 5.0 seconds.")
                return 5.0

    def generate_video(self, audio_path: str, face_image_path: str = None, output_path: str = None) -> str:
        """
        Generates the talking head video.
        Uses Wav2Lip if checkpoints are present, otherwise falls back to OpenCV simulation.
        """
        face_path = face_image_path or self.default_face
        if not os.path.exists(face_path):
            # Create a placeholder face if missing
            logger.warning(f"Face image {face_path} not found. Creating a placeholder.")
            face_path = self._create_placeholder_face()

        if not output_path:
            audio_name = os.path.splitext(os.path.basename(audio_path))[0]
            output_path = os.path.join(self.output_dir, f"{audio_name}_avatar.mp4")

        # Check if real model weights are present
        if os.path.exists(self.checkpoint_path):
            logger.info("Wav2Lip model checkpoint detected. Running ML-based lip sync...")
            return self._run_wav2lip_inference(audio_path, face_path, output_path)
        else:
            logger.info("Wav2Lip checkpoint not found. Running OpenCV-based Lip Sync simulation fallback...")
            return self._run_simulation_fallback(audio_path, face_path, output_path)

    def _run_wav2lip_inference(self, audio_path: str, face_path: str, output_path: str) -> str:
        """
        Placeholder/skeletal method for actual Wav2Lip ML inference.
        In a real deployment, this would load PyTorch and call the Wav2Lip pipeline.
        """
        # Here we would normally do:
        # from wav2lip_model import Wav2Lip
        # device = 'cuda' if torch.cuda.is_available() else 'cpu'
        # model = load_model(self.checkpoint_path)
        # model.infer(face_path, audio_path, output_path)
        # Since we're demonstrating the integration, we'll log it and fall back to simulation
        logger.warning("ML inference is defined but skipping torch import. Falling back to simulation.")
        return self._run_simulation_fallback(audio_path, face_path, output_path)

    def _run_simulation_fallback(self, audio_path: str, face_path: str, output_path: str) -> str:
        """
        Simulates lip sync by cropping the mouth region and animating it using OpenCV.
        Then merges with audio using FFmpeg.
        """
        img = cv2.imread(face_path)
        if img is None:
            raise ValueError(f"Could not load image: {face_path}")

        height, width, _ = img.shape
        duration = self._get_audio_duration(audio_path)
        total_frames = int(duration * self.fps)

        # Temporary video file path (without audio)
        temp_video_path = output_path.replace(".mp4", "_temp.mp4")
        
        # Define mouth region (heuristics for 1:1 close-up portrait of head)
        # We assume the mouth is centered horizontally and in the lower third vertically
        mouth_y1 = int(height * 0.60)
        mouth_y2 = int(height * 0.68)
        mouth_x1 = int(width * 0.44)
        mouth_x2 = int(width * 0.56)

        # Ensure coordinates are within image boundaries
        mouth_y1, mouth_y2 = max(0, mouth_y1), min(height, mouth_y2)
        mouth_x1, mouth_x2 = max(0, mouth_x1), min(width, mouth_x2)

        mouth_h = mouth_y2 - mouth_y1
        mouth_w = mouth_x2 - mouth_x1

        # Define VideoWriter (use mp4v codec for compatibility)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(temp_video_path, fourcc, self.fps, (width, height))

        logger.info(f"Rendering {total_frames} frames ({duration:.2f}s) for simulated talking video...")

        for i in range(total_frames):
            frame = img.copy()
            
            # Create a simple oscillation for mouth opening (simulate talking)
            # We combine multiple sine waves to make it look less robotic/periodic
            t = i / self.fps
            oscillation = 0.5 * np.sin(2 * np.pi * 3.5 * t) + 0.3 * np.sin(2 * np.pi * 7 * t) + 0.2 * np.sin(2 * np.pi * 1.5 * t)
            # Normalize to 0 (closed) to 1 (fully open)
            open_factor = max(0.0, min(1.0, (oscillation + 1.0) / 2.0))
            
            # Animate only if within speech duration
            if i < total_frames - 5: # Close mouth at the very end
                # Scale mouth height based on open factor
                new_h = int(mouth_h * (0.8 + 0.5 * open_factor))
                
                # Crop mouth region
                mouth = img[mouth_y1:mouth_y2, mouth_x1:mouth_x2]
                
                # Resize mouth vertically
                resized_mouth = cv2.resize(mouth, (mouth_w, new_h), interpolation=cv2.INTER_LINEAR)
                
                # Overlay mouth back
                # Calculate center to place it
                center_y = (mouth_y1 + mouth_y2) // 2
                start_y = max(0, center_y - new_h // 2)
                end_y = min(height, start_y + new_h)
                
                # Match dimensions in case of rounding errors
                resized_mouth = resized_mouth[:(end_y - start_y), :]
                
                # Blend the edges to avoid harsh seams
                mask = np.zeros_like(frame[start_y:end_y, mouth_x1:mouth_x2])
                # Radial gradient mask
                mask_h, mask_w, _ = mask.shape
                for y_idx in range(mask_h):
                    for x_idx in range(mask_w):
                        # Gaussian-like blend at edges
                        dy = abs(y_idx - mask_h/2) / (mask_h/2 + 1e-5)
                        dx = abs(x_idx - mask_w/2) / (mask_w/2 + 1e-5)
                        dist = max(dy, dx)
                        blend = max(0.0, 1.0 - dist**3)
                        mask[y_idx, x_idx] = [blend, blend, blend]
                
                # Interpolate original frame and animated mouth using the mask
                original_region = frame[start_y:end_y, mouth_x1:mouth_x2].astype(float)
                mouth_region = resized_mouth.astype(float)
                mask = mask.astype(float)
                
                blended = (mouth_region * mask + original_region * (1.0 - mask)).astype(np.uint8)
                frame[start_y:end_y, mouth_x1:mouth_x2] = blended

            out.write(frame)

        out.release()
        logger.info("Silent video frames rendered successfully.")

        # Merge audio and video using FFmpeg
        final_video_path = output_path
        try:
            logger.info("Merging audio and video using FFmpeg...")
            # If output path exists, remove it first to avoid prompt block
            if os.path.exists(final_video_path):
                os.remove(final_video_path)
                
            ffmpeg_cmd = self._get_ffmpeg_command("ffmpeg")
            cmd = [
                ffmpeg_cmd, "-y", "-i", temp_video_path, "-i", audio_path,
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
                "-shortest", final_video_path
            ]
            subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            logger.info(f"Audio/Video merge completed successfully. Output: {final_video_path}")
            
            # Clean up temp file
            if os.path.exists(temp_video_path):
                os.remove(temp_video_path)
                
            return final_video_path
        except Exception as e:
            logger.warning(f"FFmpeg audio merge failed: {e}. Outputting silent video file as fallback.")
            # If FFmpeg is missing, rename temp to final so we still have a valid video file
            if os.path.exists(final_video_path):
                os.remove(final_video_path)
            os.rename(temp_video_path, final_video_path)
            return final_video_path

    def _create_placeholder_face(self) -> str:
        """
        Creates a clean minimalistic face image using OpenCV.
        """
        img_path = os.path.join(os.path.dirname(self.default_face), "mc_placeholder.png")
        os.makedirs(os.path.dirname(img_path), exist_ok=True)
        
        # 512x512 blue gradient canvas
        width, height = 512, 512
        canvas = np.zeros((height, width, 3), dtype=np.uint8)
        for y in range(height):
            # Rich dark blue to indigo gradient
            color = [int(40 + (y / height) * 30), int(20 + (y / height) * 15), int(10 + (y / height) * 10)]
            canvas[y, :] = color

        # Draw minimalistic face (circle)
        cv2.circle(canvas, (256, 230), 100, (200, 200, 200), -1) # Head
        cv2.circle(canvas, (216, 210), 10, (40, 40, 40), -1)      # Left Eye
        cv2.circle(canvas, (296, 210), 10, (40, 40, 40), -1)      # Right Eye
        cv2.ellipse(canvas, (256, 260), (30, 10), 0, 0, 360, (40, 40, 200), -1) # Default mouth shape

        cv2.imwrite(img_path, canvas)
        return img_path

# Create singleton instance
avatar_generator = AvatarGenerator()
