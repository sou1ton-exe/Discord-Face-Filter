import cv2
import numpy as np


class FaceDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        
    def detect(self, gray_frame):
        if self.face_cascade.empty(): return []
        faces = self.face_cascade.detectMultiScale(
            gray_frame,
            scaleFactor=1.1,
            minNeighbors=12,
            minSize=(30, 30)
        )
        
        return faces

class FaceProcessor:
    def __init__(self):
        self.detector = FaceDetector()
        self.pixel_size = 15
        self.mode = "pixelate"
        
    def increase_pixel_size(self): self.pixel_size = min(50, self.pixel_size + 2)
        
    def decrease_pixel_size(self): self.pixel_size = max(2, self.pixel_size - 2)
        
    def toggle_mode(self): self.mode = "blur" if self.mode == "pixelate" else "pixelate"
        
    def pixelate_face(self, face_region, pixel_size):
        if face_region.size == 0: return face_region
        
        (h, w) = face_region.shape[:2]
        
        temp = cv2.resize(face_region, (w // pixel_size, h // pixel_size), interpolation=cv2.INTER_LINEAR)
        
        pixelated = cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)
        
        return pixelated
        
    def process_face(self, frame, x, y, w, h):
        y_expanded = max(0, y - h // 4)
        h_expanded = min(frame.shape[0] - y_expanded, int(h * 1.3))
        x_expanded = max(0, x - w // 4)
        w_expanded = min(frame.shape[1] - x_expanded, int(w * 1.2))
        
        face_roi = frame[y_expanded:y_expanded+h_expanded, 
                        x_expanded:x_expanded+w_expanded]
        
        if face_roi.size > 0:
            if self.mode == "pixelate": pixelated_face = self.pixelate_face(face_roi, self.pixel_size)
            else: pixelated_face = cv2.GaussianBlur(face_roi, (51, 51), 0)
            
            frame[y_expanded:y_expanded+h_expanded, 
                  x_expanded:x_expanded+w_expanded] = pixelated_face
        
    def process_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.detector.detect(gray)
        
        for (x, y, w, h) in faces: self.process_face(frame, x, y, w, h)
            
        return frame