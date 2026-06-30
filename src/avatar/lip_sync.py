import os
import shutil
import subprocess
from pathlib import Path
from functools import lru_cache
import cv2
import numpy as np
from src.utils.logger import logger
from src.utils.config import config

# --- Named Constants ---
# Face anatomy ratios (relative to Haar Cascade face bounding box)
MOUTH_VERTICAL_RATIO = 0.73       # Mouth center is ~73% down the face height
MOUTH_WIDTH_RATIO = 0.12          # Mouth width is ~12% of face width
MOUTH_HEIGHT_RATIO = 0.06         # Mouth max opening is ~6% of face height

# Fallback portrait heuristics (when no face is detected)
FALLBACK_MOUTH_X_RATIO = 0.50     # Centered horizontally
FALLBACK_MOUTH_Y_RATIO = 0.65     # 65% down image height
FALLBACK_MOUTH_RX_RATIO = 0.035   # ~3.5% of image width
FALLBACK_MOUTH_RY_RATIO = 0.022   # ~2.2% of image height

# Audio duration estimation (when ffprobe is unavailable)
MP3_APPROX_BYTES_PER_SEC = 6000.0   # edge-tts default is ~48kbps
WAV_APPROX_BYTES_PER_SEC = 48000.0  # 16-bit 24kHz mono
FALLBACK_DURATION_SEC = 5.0

# Mouth oscillation frequencies (Hz) — combined for natural speech rhythm
OSCILLATION_FREQ_PRIMARY = 3.5
OSCILLATION_FREQ_SECONDARY = 7.0
OSCILLATION_FREQ_TERTIARY = 1.5

# Drawing parameters
MOUTH_CAVITY_COLOR = (20, 20, 50)
TEETH_COLOR = (250, 250, 250)
LIPS_COLOR = (50, 50, 190)
OVERLAY_ALPHA = 0.90


class AvatarGenerator:
    def __init__(self):
        self.default_face = config.get("avatar.default_face", "assets/avatar/mc_default.png")
        self.output_dir = config.get("avatar.output_dir", "assets/video")
        self.fps = config.get("avatar.fps", 25)
        self.model_name = config.get("avatar.model_name", "wav2lip")
        self.checkpoint_path = config.get("avatar.checkpoint_path", "checkpoints/wav2lip.pth")

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    @staticmethod
    @lru_cache(maxsize=4)
    def _get_ffmpeg_command(name: str) -> str:
        """
        Resolves the executable name (ffmpeg or ffprobe) to an absolute path.
        Uses shutil.which() for cross-platform discovery, with WinGet fallback on Windows.
        Results are cached to avoid repeated filesystem lookups.
        """
        # 1. Cross-platform lookup via shutil.which (uses system PATH)
        which_path = shutil.which(name)
        if which_path:
            return which_path

        # 2. Windows-specific fallback: WinGet Links directory
        if os.name == "nt":
            local_app_data = os.environ.get("LOCALAPPDATA", "")
            if local_app_data:
                winget_links = os.path.join(local_app_data, "Microsoft", "WinGet", "Links", f"{name}.exe")
                if os.path.exists(winget_links):
                    return winget_links

                # 3. Last resort: search WinGet Packages (cached, so only runs once)
                packages_dir = os.path.join(local_app_data, "Microsoft", "WinGet", "Packages")
                if os.path.exists(packages_dir):
                    for root, dirs, files in os.walk(packages_dir):
                        if f"{name}.exe" in files:
                            return os.path.join(root, f"{name}.exe")

        # Fallback: return the bare name and let subprocess handle it
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
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            output = result.stdout.strip()
            if "duration=" in output:
                output = output.split("duration=")[-1]
            return float(output)
        except Exception:
            # Fallback heuristic based on file size
            file_size = os.path.getsize(audio_path)
            if audio_path.lower().endswith(".mp3"):
                duration = file_size / MP3_APPROX_BYTES_PER_SEC
                logger.info(f"ffprobe failed. Estimated MP3 duration based on file size: {duration:.2f}s")
                return max(1.0, duration)
            elif audio_path.lower().endswith(".wav"):
                duration = file_size / WAV_APPROX_BYTES_PER_SEC
                logger.info(f"ffprobe failed. Estimated WAV duration based on file size: {duration:.2f}s")
                return max(1.0, duration)
            else:
                logger.warning(f"Unknown audio format. Fallback duration set to {FALLBACK_DURATION_SEC}s.")
                return FALLBACK_DURATION_SEC

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
        Simulates lip sync by animating the mouth region using OpenCV.
        Then merges with audio using FFmpeg.
        """
        img = cv2.imread(face_path)
        if img is None:
            raise ValueError(f"Could not load image: {face_path}")

        height, width, _ = img.shape
        duration = self._get_audio_duration(audio_path)
        total_frames = int(duration * self.fps)

        # Temporary video file path (without audio) — use pathlib to avoid string replace bugs
        output_p = Path(output_path)
        temp_video_path = str(output_p.with_stem(output_p.stem + "_temp"))
        
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
                mouth_y = fy + int(fh * MOUTH_VERTICAL_RATIO)
                rx = int(fw * MOUTH_WIDTH_RATIO)
                ry_max = int(fh * MOUTH_HEIGHT_RATIO)
                has_face = True
                logger.info(f"Face detected for lip sync: x={fx}, y={fy}, w={fw}, h={fh}. Mouth centered at ({mouth_x}, {mouth_y})")

        if not has_face:
            logger.warning("No face detected by Haar Cascade. Using default portrait heuristics.")
            mouth_x = int(width * FALLBACK_MOUTH_X_RATIO)
            mouth_y = int(height * FALLBACK_MOUTH_Y_RATIO)
            rx = int(width * FALLBACK_MOUTH_RX_RATIO)
            ry_max = int(height * FALLBACK_MOUTH_RY_RATIO)

        # Define VideoWriter (use mp4v codec for compatibility)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(temp_video_path, fourcc, self.fps, (width, height))

        logger.info(f"Rendering {total_frames} frames ({duration:.2f}s) for simulated talking video...")

        try:
            for i in range(total_frames):
                frame = img.copy()
                
                # Create a simple oscillation for mouth opening (simulate talking)
                # We combine multiple sine waves to make it look less robotic/periodic
                t = i / self.fps
                oscillation = (
                    0.5 * np.sin(2 * np.pi * OSCILLATION_FREQ_PRIMARY * t)
                    + 0.3 * np.sin(2 * np.pi * OSCILLATION_FREQ_SECONDARY * t)
                    + 0.2 * np.sin(2 * np.pi * OSCILLATION_FREQ_TERTIARY * t)
                )
                # Normalize to 0 (closed) to 1 (fully open)
                open_factor = max(0.0, min(1.0, (oscillation + 1.0) / 2.0))
                
                # Animate only if within speech duration
                if i < total_frames - 5:  # Close mouth at the very end
                    cx = mouth_x
                    cy = mouth_y
                    
                    # Draw mouth cavity (dark oval)
                    ry = int(ry_max * open_factor)  # vertical opening
                    
                    if ry > 2:
                        overlay = frame.copy()
                        # 1. Dark mouth cavity
                        cv2.ellipse(overlay, (cx, cy), (rx, ry), 0, 0, 360, MOUTH_CAVITY_COLOR, -1)
                        
                        # 2. Teeth (white lines)
                        # Upper teeth
                        cv2.line(overlay, (cx - rx + 8, cy - ry + 3), (cx + rx - 8, cy - ry + 3), TEETH_COLOR, 3)
                        # Lower teeth (show if open wide)
                        if ry > 8:
                            cv2.line(overlay, (cx - rx + 12, cy + ry - 3), (cx + rx - 12, cy + ry - 3), TEETH_COLOR, 2)
                            
                        # 3. Red lips outline
                        cv2.ellipse(overlay, (cx, cy), (rx + 2, ry + 2), 0, 0, 360, LIPS_COLOR, 2)
                        
                        # Alpha blend overlay with frame to soften the edges
                        cv2.addWeighted(overlay, OVERLAY_ALPHA, frame, 1.0 - OVERLAY_ALPHA, 0, frame)

                out.write(frame)
        finally:
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
        Returns the path to the created image, or raises IOError on failure.
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

        success = cv2.imwrite(img_path, canvas)
        if not success:
            raise IOError(f"Failed to write placeholder face image to: {img_path}")
        return img_path

# Create singleton instance
avatar_generator = AvatarGenerator()
