from ultralytics import YOLO

class PPEYOLODetector:
    def __init__(self, model_path: str, device: str = "mps", imgsz: int = 640, conf: float = 0.25):
        # device: "mps" (Apple Silicon), "cpu"
        self.model = YOLO(model_path)
        self.device = device
        self.imgsz = imgsz
        self.conf = conf

    def infer(self, frame):
        # Run inference on a single frame
        results = self.model.predict(
            source=frame,
            imgsz=self.imgsz,
            conf=self.conf,
            device=self.device,
            verbose=False,
        )
        return results[0]