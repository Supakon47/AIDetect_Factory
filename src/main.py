import os
import cv2
from detector import PPEYOLODetector
from utils import yolo_to_detections
from rules import build_compliance
from logger import ensure_logs_dir, append_log_csv, now_iso

def main():
    # Model: start with your current yolov8n.pt (person only)
    # For PPE, replace with a PPE-trained .pt later
    model_path = "models/best.pt"

    # If you are on Intel Mac, set device="cpu"
    detector = PPEYOLODetector(model_path=model_path, device="mps", imgsz=640, conf=0.25)

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    log_dir = "logs"
    ensure_logs_dir(log_dir)
    log_path = os.path.join(log_dir, "events.csv")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        result = detector.infer(frame)
        detections = yolo_to_detections(result)

        # NOTE: With yolov8n.pt you only get "person" by default
        # PPE compliance will work after you switch to a PPE model
        compliance = build_compliance(detections)

        annotated = result.plot()

        status_text = "PASS" if compliance["compliant"] else "FAIL"
        missing_text = ",".join(compliance["missing"]) if compliance["missing"] else "-"

        cv2.putText(annotated, f"Compliance: {status_text}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0) if compliance["compliant"] else (0, 0, 255), 2)
        cv2.putText(annotated, f"Missing: {missing_text}", (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        # Log (you can choose to log only FAIL events later)
        append_log_csv(log_path, {
            "timestamp": now_iso(),
            "compliant": compliance["compliant"],
            "missing": missing_text,
            "present": ",".join(compliance["present"]),
        })

        cv2.imshow("PPE Compliance AI", annotated)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()