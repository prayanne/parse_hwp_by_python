import argparse
import json
from src.hwp_parser import (
    extract_text,
    extract_text_to_stdout,
    export_to_json,
    parse_pipe_tables,
    normalize_text
)


def main():
    parser = argparse.ArgumentParser(
        description="HWP Parser - Extract text and tables from HWP files"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to .hwp file inside container"
    )
    parser.add_argument(
        "--output",
        help="Output file path (for json/tables mode)"
    )
    parser.add_argument(
        "--mode",
        choices=["text", "json", "tables"],
        default="text",
        help="Output mode: text (stdout), json (export to JSON), tables (extract tables)"
    )
    parser.add_argument(
        "--normalize",
        action="store_true",
        help="Normalize text output (remove NBSP, trim whitespace)"
    )

    args = parser.parse_args()

    if args.mode == "text":
        if args.normalize:
            text = extract_text(args.input)
            text = normalize_text(text)
            print(text)
        else:
            extract_text_to_stdout(args.input)

    elif args.mode == "json":
        if not args.output:
            print("Error: --output is required for json mode")
            return 1
        export_to_json(args.input, args.output)
        print(f"Exported to: {args.output}")

    elif args.mode == "tables":
        text = extract_text(args.input)
        tables = parse_pipe_tables(text)

        result = {
            "source": args.input,
            "table_count": len(tables),
            "tables": tables
        }

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"Found {len(tables)} tables, exported to: {args.output}")
        else:
            print(json.dumps(result, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    exit(main())
