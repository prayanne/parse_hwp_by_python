from hwp5 import hwp5txt

def extract_hwp_text(hwp_path: str) -> str:
    # hwp5txt는 HWP 문서의 텍스트를 최대한 자연스럽게 뽑아줍니다.
    # (머리말/꼬리말/표 내부 텍스트 등도 상당 부분 포함)
    return hwp5txt.text(hwp_path)

if __name__ == "__main__":
    path = "/mnt/data/2025.11.23.hwp"
    text = extract_hwp_text(path)
    print(text[:2000])          # 앞부분 미리보기
    print("\n--- total chars:", len(text))
