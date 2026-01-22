import cv2
import time


class InterfaceManager:
    def __init__(self):
        self.window_name = "Face Filter"
        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        
    def print_instructions(self):
        print("\n" + "="*40)
        print("FACE PIXELATION FILTER")
        print("="*40)
        print("Q - Quit")
        print("S - Save screenshot")
        print("+/- - Change pixel size")
        print("M - Toggle mode (pixelate/blur)")
        print("I - Toggle mirror effect")
        print("="*40)
        
    def add_overlay(self, frame, face_processor):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_processor.detector.detect(gray)
        
        status_text = f"Faces: {len(faces)} | Mode: {face_processor.mode} | "
        status_text += f"Pixel: {face_processor.pixel_size}"
        
        cv2.putText(frame, status_text, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        return frame
        
    def display_frame(self, frame): cv2.imshow(self.window_name, frame)
        
    def save_screenshot(self, face_processor):
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}_{face_processor.mode}_{face_processor.pixel_size}.jpg"
        cv2.imwrite(filename, cv2.imread('current_frame'))
        print(f"Screenshot saved: {filename}")
        
    def cleanup(self): cv2.destroyAllWindows()