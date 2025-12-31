import json
from hwp5 import hwp5txt

def normalize_text(text: str) -> str:
    # 기본 정규화 (원하면 규칙을 더 강화)
    text = text.replace("\u00a0", " ")  # NBSP
    return "\n".join(line.rstrip() for line in text.splitlines())

def hwp_to_json(hwp_path: str, out_path: str) -> None:
    raw = hwp5txt.text(hwp_path)
    norm = normalize_text(raw)

    doc = {
        "source": hwp_path,
        "length_chars": len(norm),
        "text": norm,
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    hwp_to_json("/mnt/data/2025.11.23.hwp", "/mnt/data/2025.11.23.json")
    print("written:", "/mnt/data/2025.11.23.json")
