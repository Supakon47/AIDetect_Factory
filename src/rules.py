from typing import Dict, List, Any

# Adjust these class names to match your PPE model classes
REQUIRED_ITEMS = ["helmet", "vest"]

def build_compliance(detections: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    detections: list of {"cls_name": str, "conf": float, "xyxy": [x1,y1,x2,y2]}
    """
    present = set([d["cls_name"] for d in detections])

    missing = [item for item in REQUIRED_ITEMS if item not in present]
    compliant = (len(missing) == 0)

    return {
        "compliant": compliant,
        "missing": missing,
        "present": sorted(list(present)),
    }