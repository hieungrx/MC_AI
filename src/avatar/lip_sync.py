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
        
        # Detect face using Haar Cascade to position mouth dynamically
        face_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        face_cascade = cv2.CascadeClassifier(face_cascade_path)
        
        has_face = False
        if not face_cascade.empty():
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))
            if len(faces) > 0:
                faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
                fx, fy, fw, fh = faces[0]
                mouth_x = fx + fw // 2
                # Mouth is typically around 73% down the face box
                mouth_y = fy + int(fh * 0.73)
                rx = int(fw * 0.12)
                ry_max = int(fh * 0.06)
                has_face = True
                logger.info(f"Face detected for lip sync: x={fx}, y={fy}, w={fw}, h={fh}. Mouth centered at ({mouth_x}, {mouth_y})")

        if not has_face:
            logger.warning("No face detected by Haar Cascade. Using default portrait heuristics.")
            mouth_x = int(width * 0.50)
            mouth_y = int(height * 0.65)
            rx = int(width * 0.035)
            ry_max = int(height * 0.022)

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
                cx = mouth_x
                cy = mouth_y
                
                # Draw mouth cavity (dark oval)
                ry = int(ry_max * open_factor)  # vertical opening
                
                if ry > 2:
                    overlay = frame.copy()
                    # 1. Dark mouth cavity
                    cv2.ellipse(overlay, (cx, cy), (rx, ry), 0, 0, 360, (20, 20, 50), -1)
                    
                    # 2. Teeth (white lines)
                    # Upper teeth
                    cv2.line(overlay, (cx - rx + 8, cy - ry + 3), (cx + rx - 8, cy - ry + 3), (250, 250, 250), 3)
                    # Lower teeth (show if open wide)
                    if ry > 8:
                        cv2.line(overlay, (cx - rx + 12, cy + ry - 3), (cx + rx - 12, cy + ry - 3), (250, 250, 250), 2)
                        
                    # 3. Red lips outline
                    cv2.ellipse(overlay, (cx, cy), (rx + 2, ry + 2), 0, 0, 360, (50, 50, 190), 2)
                    
                    # Alpha blend overlay with frame to soften the edges
                    alpha = 0.90
                    cv2.addWeighted(overlay, alpha, frame, 1.0 - alpha, 0, frame)

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
