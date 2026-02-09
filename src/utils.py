from typing import List, Dict, Any

def yolo_to_detections(result) -> List[Dict[str, Any]]:
    """
    result: ultralytics.engine.results.Results
    """
    detections = []
    names = result.names

    if result.boxes is None:
        return detections

    for b in result.boxes:
        cls_id = int(b.cls[0].item())
        conf = float(b.conf[0].item())
        x1, y1, x2, y2 = [float(v) for v in b.xyxy[0].tolist()]

        detections.append({
            "cls_id": cls_id,
            "cls_name": names.get(cls_id, str(cls_id)),
            "conf": conf,
            "xyxy": [x1, y1, x2, y2],
        })

    return detections