import cv2
import os

def draw_debug_mouth():
    img_path = "assets/avatar/mc_default.png"
    if not os.path.exists(img_path):
        print("Error: mc_default.png not found")
        return
        
    img = cv2.imread(img_path)
    height, width, _ = img.shape
    
    # Same coordinates as in lip_sync.py
    mouth_y1 = int(height * 0.60)
    mouth_y2 = int(height * 0.68)
    mouth_x1 = int(width * 0.44)
    mouth_x2 = int(width * 0.56)
    
    # Draw red rectangle around the mouth
    debug_img = img.copy()
    cv2.rectangle(debug_img, (mouth_x1, mouth_y1), (mouth_x2, mouth_y2), (0, 0, 255), 3)
    
    output_path = "assets/avatar/debug_mouth.png"
    cv2.imwrite(output_path, debug_img)
    print(f"Debug image saved at: {os.path.abspath(output_path)}")
    print(f"Image shape: {width}x{height}")
    print(f"Mouth bounding box: x={mouth_x1}-{mouth_x2}, y={mouth_y1}-{mouth_y2}")

if __name__ == "__main__":
    draw_debug_mouth()
