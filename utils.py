from typing import Dict
import json

def read_json(path: str) -> Dict[str, object]:
    with open(path, 'r', encoding = 'utf-8') as f:
        config: Dict[str, object] = json.load(f)
    return config