import re
import json
from typing import List
from hwp5 import hwp5txt


def extract_text(hwp_path: str) -> str:
    """
    Extract text content from HWP file.

    Args:
        hwp_path: Path to the .hwp file

    Returns:
        Raw text content from the HWP document
    """
    return hwp5txt.text(hwp_path)


def extract_text_to_stdout(hwp_path: str) -> None:
    """
    Extract text from HWP file and print to stdout.

    Args:
        hwp_path: Path to the .hwp file
    """
    text = extract_text(hwp_path)
    print(text)


def normalize_text(text: str) -> str:
    """
    Normalize text by removing non-breaking spaces and trailing whitespace.

    Args:
        text: Raw text to normalize

    Returns:
        Normalized text
    """
    text = text.replace("\u00a0", " ")  # NBSP
    return "\n".join(line.rstrip() for line in text.splitlines())


def parse_pipe_tables(text: str) -> List[List[List[str]]]:
    """
    Parse pipe-delimited tables from text (format: | col1 | col2 |).

    Args:
        text: Text containing pipe-delimited tables

    Returns:
        List of tables, where each table is a list of rows,
        and each row is a list of cell values.
        Example: [table1, table2, ...] where table = [row1, row2, ...]
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


def export_to_json(hwp_path: str, output_path: str) -> None:
    """
    Extract text from HWP and export to JSON file.

    Args:
        hwp_path: Path to the .hwp file
        output_path: Path to the output JSON file
    """
    raw = extract_text(hwp_path)
    norm = normalize_text(raw)

    doc = {
        "source": hwp_path,
        "length_chars": len(norm),
        "text": norm,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
