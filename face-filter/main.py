from camera_manager import CameraManager
from face_processor import FaceProcessor
from interface_manager import InterfaceManager
import cv2


class FaceFilterApp:
    def __init__(self):
        self.camera_manager = CameraManager()
        self.face_processor = FaceProcessor()
        self.interface = InterfaceManager()
        self.running = False
        
    def run(self):
        if not self.camera_manager.initialize(): return
            
        self.camera_manager.print_camera_info()
        self.interface.print_instructions()
        
        self.running = True
        self.main_loop()
        
    def main_loop(self):
        while self.running:
            frame = self.camera_manager.capture_frame()
            if frame is None: break
                
            processed_frame = self.face_processor.process_frame(frame)
            display_frame = self.interface.add_overlay(processed_frame, self.face_processor)
            
            self.interface.display_frame(display_frame)
            self.handle_keys()
            
    def handle_keys(self):
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'): self.running = False
        elif key == ord('s'): self.interface.save_screenshot(self.face_processor)
        elif key == ord('+'): self.face_processor.increase_pixel_size()
        elif key == ord('-'): self.face_processor.decrease_pixel_size()
        elif key == ord('m'): self.face_processor.toggle_mode()
        elif key == ord('i'): self.camera_manager.toggle_flip()
            
    def cleanup(self):
        self.camera_manager.release()
        self.interface.cleanup()

if __name__ == "__main__":
    app = FaceFilterApp()
    try: app.run()
    finally: app.cleanup()