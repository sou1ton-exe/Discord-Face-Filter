import cv2


class CameraManager:
    def __init__(self):
        self.cap = None
        self.camera_index = 0
        self.flip_enabled = True
        
    def find_available_cameras(self):
        available = []
        for i in range(5):
            temp_cap = cv2.VideoCapture(i)
            if temp_cap.isOpened():
                available.append(i)
                temp_cap.release()
                
        return available
        
    def initialize(self):
        cameras = self.find_available_cameras()
        if not cameras:
            print("ERROR: No cameras available!")
            return False
            
        self.camera_index = cameras[0]
        self.cap = cv2.VideoCapture(self.camera_index)
        
        if not self.cap.isOpened(): self.cap = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
            
        if not self.cap.isOpened():
            print("ERROR: Cannot open camera!")
            return False
            
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        return True
        
    def capture_frame(self):
        ret, frame = self.cap.read()
        if not ret: return None
            
        if self.flip_enabled: frame = cv2.flip(frame, 1)
        return frame
        
    def toggle_flip(self):
        self.flip_enabled = not self.flip_enabled
        return self.flip_enabled
        
    def print_camera_info(self):
        print(f"Using camera: {self.camera_index}")
        print(f"Flip mode: {'ON' if self.flip_enabled else 'OFF'}")
        
    def release(self):
        if self.cap: self.cap.release()