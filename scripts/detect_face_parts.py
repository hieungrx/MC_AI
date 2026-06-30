import cv2
import os

def detect_mouth_relative():
    """Debug script to verify Haar Cascade face + mouth detection on the default avatar."""
    img_path = "assets/avatar/mc_default.png"
    if not os.path.exists(img_path):
        print("Error: mc_default.png not found")
        return
        
    img = cv2.imread(img_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Load face cascade classifier
    face_cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    face_cascade = cv2.CascadeClassifier(face_cascade_path)
    
    if face_cascade.empty():
        print("Error: Could not load Haar cascade classifier.")
        return
        
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))
    
    # Use same constants as lip_sync.py
    MOUTH_VERTICAL_RATIO = 0.73
    MOUTH_WIDTH_RATIO = 0.12
    MOUTH_HEIGHT_RATIO = 0.06

    debug_img = img.copy()

    if len(faces) == 0:
        print("Warning: No faces detected. Using fallback heuristics.")
        height, width, _ = img.shape
        mouth_x = int(width * 0.50)
        mouth_y = int(height * 0.65)
        rx = int(width * 0.035)
        ry = int(height * 0.022)
    else:
        faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
        fx, fy, fw, fh = faces[0]
        print(f"Face detected: x={fx}, y={fy}, w={fw}, h={fh}")
        
        mouth_x = fx + fw // 2
        mouth_y = fy + int(fh * MOUTH_VERTICAL_RATIO)
        rx = int(fw * MOUTH_WIDTH_RATIO)
        ry = int(fh * MOUTH_HEIGHT_RATIO)
        
        # Draw face box in green
        cv2.rectangle(debug_img, (fx, fy), (fx + fw, fy + fh), (0, 255, 0), 2)
    
    # Draw mouth box in red
    cv2.rectangle(debug_img, (mouth_x - rx, mouth_y - ry), (mouth_x + rx, mouth_y + ry), (0, 0, 255), 3)
    
    output_path = "assets/avatar/debug_mouth_detected.png"
    cv2.imwrite(output_path, debug_img)
    print(f"Debug image saved at: {os.path.abspath(output_path)}")
    print(f"Mouth center: ({mouth_x}, {mouth_y}), rx={rx}, ry={ry}")

if __name__ == "__main__":
    detect_mouth_relative()
