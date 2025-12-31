import re
from typing import List

def parse_pipe_tables(text: str) -> List[List[List[str]]]:
    """
    텍스트 안에서 | a | b | 형태 블록을 찾아 테이블 목록으로 반환
    return: [table1, table2, ...]
            table = [row1, row2, ...]
            row = [cell1, cell2, ...]
    """
    lines = [ln.rstrip() for ln in text.splitlines()]
    tables = []
    current = []

    pipe_row = re.compile(r"^\s*\|.*\|\s*$")
    for ln in lines:
        if pipe_row.match(ln):
            row = [c.strip() for c in ln.strip().strip("|").split("|")]
            current.append(row)
        else:
            if current:
                tables.append(current)
                current = []

    if current:
        tables.append(current)

    return tables

if __name__ == "__main__":
    from hwp5 import hwp5txt
    path = "./2025.12.31.hwp"
    text = hwp5txt.text(path)
    tables = parse_pipe_tables(text)
    print("tables found:", len(tables))
    if tables:
        print("first table rows:", len(tables[0]))
        for r in tables[0][:10]:
            print(r)
