# HWP Parser Module Documentation

## Overview

The HWP Parser is a Docker-based Python module for extracting text and tables from HWP (Hangul Word Processor) files. It provides a simple command-line interface and can export data in multiple formats including plain text, JSON, and structured table data.

## Features

- Extract plain text from HWP files
- Parse pipe-delimited tables from HWP documents
- Export to JSON format with normalized text
- Docker containerization for consistent execution environment
- Multiple output modes (text, JSON, tables)
- Text normalization options

## Architecture

### Project Structure

```
hwp_parse/
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
├── .dockerignore          # Docker build ignore patterns
├── src/
│   ├── __init__.py        # Module initialization
│   ├── main.py            # CLI entry point
│   ├── hwp_parser.py      # Core parser functionality
│   ├── app.py             # Legacy table parser (deprecated)
│   ├── parse_hwp.py       # Legacy parser (deprecated)
│   ├── export_json.py     # Legacy JSON exporter (deprecated)
│   └── export_str.py      # Legacy text extractor (deprecated)
└── docs.md                # This documentation
```

### Core Components

#### `hwp_parser.py`

The main parser module containing all extraction and parsing functionality:

- `extract_text(hwp_path: str) -> str`: Extract raw text from HWP file
- `extract_text_to_stdout(hwp_path: str) -> None`: Extract and print text to stdout
- `normalize_text(text: str) -> str`: Normalize text (remove NBSP, trim whitespace)
- `parse_pipe_tables(text: str) -> List[List[List[str]]]`: Parse pipe-delimited tables
- `export_to_json(hwp_path: str, output_path: str) -> None`: Export to JSON file

#### `main.py`

Command-line interface providing multiple modes of operation:

- `text` mode: Extract and print text to stdout
- `json` mode: Export text to JSON file with metadata
- `tables` mode: Extract and export table structures

## Installation

### Prerequisites

- Docker (20.10 or higher)
- Docker Compose (optional, for easier management)

### Building the Docker Image

```bash
# Build using Docker
docker build -t hwp-parser .

# Or using Docker Compose
docker-compose build
```

## Usage

### Basic Usage with Docker

#### Extract Text to Stdout

```bash
docker run --rm -v "$(pwd)/data:/app/data" hwp-parser \
  --input /app/data/sample.hwp --mode text
```

#### Extract Normalized Text

```bash
docker run --rm -v "$(pwd)/data:/app/data" hwp-parser \
  --input /app/data/sample.hwp --mode text --normalize
```

#### Export to JSON

```bash
docker run --rm \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/output:/app/output" \
  hwp-parser \
  --input /app/data/sample.hwp \
  --mode json \
  --output /app/output/result.json
```

#### Extract Tables

```bash
# Print tables to stdout
docker run --rm -v "$(pwd)/data:/app/data" hwp-parser \
  --input /app/data/sample.hwp --mode tables

# Export tables to JSON file
docker run --rm \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/output:/app/output" \
  hwp-parser \
  --input /app/data/sample.hwp \
  --mode tables \
  --output /app/output/tables.json
```

### Using Docker Compose

Docker Compose simplifies volume mounting and container management.

```bash
# Extract text
docker-compose run --rm hwp-parser \
  --input /app/data/sample.hwp --mode text

# Export to JSON
docker-compose run --rm hwp-parser \
  --input /app/data/sample.hwp \
  --mode json \
  --output /app/output/result.json

# Extract tables
docker-compose run --rm hwp-parser \
  --input /app/data/sample.hwp \
  --mode tables \
  --output /app/output/tables.json
```

### Windows Usage

For Windows users, adjust the volume mounting syntax:

```powershell
# PowerShell
docker run --rm -v "${PWD}/data:/app/data" hwp-parser `
  --input /app/data/sample.hwp --mode text

# CMD
docker run --rm -v "%cd%/data:/app/data" hwp-parser ^
  --input /app/data/sample.hwp --mode text
```

## Command-Line Options

### Required Arguments

- `--input PATH`: Path to the .hwp file inside the container

### Optional Arguments

- `--output PATH`: Output file path (required for json mode, optional for tables mode)
- `--mode {text|json|tables}`: Output mode (default: text)
  - `text`: Extract and print text to stdout
  - `json`: Export text to JSON file with metadata
  - `tables`: Extract pipe-delimited tables
- `--normalize`: Normalize text output (remove non-breaking spaces, trim whitespace)

## Output Formats

### Text Mode

Plain text output to stdout:

```
[Extracted text content from HWP file...]
```

### JSON Mode

Structured JSON with metadata:

```json
{
  "source": "/app/data/sample.hwp",
  "length_chars": 1234,
  "text": "[Normalized text content...]"
}
```

### Tables Mode

Structured JSON with table data:

```json
{
  "source": "/app/data/sample.hwp",
  "table_count": 2,
  "tables": [
    [
      ["Header1", "Header2", "Header3"],
      ["Row1Col1", "Row1Col2", "Row1Col3"],
      ["Row2Col1", "Row2Col2", "Row2Col3"]
    ],
    [
      ["Table2Header1", "Table2Header2"],
      ["Table2Row1Col1", "Table2Row1Col2"]
    ]
  ]
}
```

## API Reference

### `hwp_parser.extract_text(hwp_path: str) -> str`

Extract raw text content from an HWP file.

**Parameters:**
- `hwp_path` (str): Path to the .hwp file

**Returns:**
- str: Raw text content

**Example:**
```python
from src.hwp_parser import extract_text

text = extract_text("/app/data/sample.hwp")
print(text)
```

### `hwp_parser.normalize_text(text: str) -> str`

Normalize text by removing non-breaking spaces and trailing whitespace.

**Parameters:**
- `text` (str): Raw text to normalize

**Returns:**
- str: Normalized text

**Example:**
```python
from src.hwp_parser import extract_text, normalize_text

raw_text = extract_text("/app/data/sample.hwp")
normalized = normalize_text(raw_text)
```

### `hwp_parser.parse_pipe_tables(text: str) -> List[List[List[str]]]`

Parse pipe-delimited tables from text content.

**Parameters:**
- `text` (str): Text containing pipe-delimited tables (format: `| col1 | col2 |`)

**Returns:**
- List[List[List[str]]]: List of tables, where each table is a list of rows, and each row is a list of cells

**Example:**
```python
from src.hwp_parser import extract_text, parse_pipe_tables

text = extract_text("/app/data/sample.hwp")
tables = parse_pipe_tables(text)

print(f"Found {len(tables)} tables")
for i, table in enumerate(tables):
    print(f"Table {i+1}: {len(table)} rows")
```

### `hwp_parser.export_to_json(hwp_path: str, output_path: str) -> None`

Extract text from HWP and export to JSON file with metadata.

**Parameters:**
- `hwp_path` (str): Path to the .hwp file
- `output_path` (str): Path to the output JSON file

**Example:**
```python
from src.hwp_parser import export_to_json

export_to_json("/app/data/sample.hwp", "/app/output/result.json")
```

## Docker Configuration

### Dockerfile

The Dockerfile uses Python 3.10-slim base image and includes:

- System dependencies: libxml2, libxslt1.1, zlib1g (required by pyhwp)
- Python dependencies from requirements.txt
- Application source code in /app/src/
- Entry point: `python -m src.main`

### Environment Variables

- `PYTHONDONTWRITEBYTECODE=1`: Prevents Python from writing .pyc files
- `PYTHONUNBUFFERED=1`: Enables unbuffered output for real-time logging
- `PIP_NO_CACHE_DIR=1`: Disables pip cache to reduce image size

### Volume Mounting

Recommended volume mounts:

- `/app/data`: Mount your HWP files directory
- `/app/output`: Mount output directory for JSON exports

## Troubleshooting

### Issue: "No such file or directory"

**Cause:** File path is incorrect or volume not mounted properly

**Solution:** Ensure you're using the correct container path (e.g., `/app/data/sample.hwp`) and that the volume is mounted correctly:

```bash
docker run --rm -v "$(pwd)/data:/app/data" hwp-parser --input /app/data/sample.hwp
```

### Issue: "Error: --output is required for json mode"

**Cause:** JSON mode requires an output file path

**Solution:** Provide the `--output` argument:

```bash
docker run --rm \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/output:/app/output" \
  hwp-parser \
  --input /app/data/sample.hwp \
  --mode json \
  --output /app/output/result.json
```

### Issue: "Permission denied" when writing output

**Cause:** Container doesn't have write permissions to the output directory

**Solution:** Ensure the output directory exists and has proper permissions:

```bash
mkdir -p output
chmod 777 output  # Or appropriate permissions for your environment
```

### Issue: Garbled text or encoding errors

**Cause:** HWP file encoding issues

**Solution:** The parser uses UTF-8 encoding by default. If you encounter issues:

1. Verify the HWP file is not corrupted
2. Try using the `--normalize` flag for text mode
3. Check if the HWP file version is supported by pyhwp

## Dependencies

### Python Packages

- `pyhwp==0.1b15`: HWP file parser library (hwp5)

### System Libraries

- `libxml2`: XML parsing library
- `libxslt1.1`: XSLT transformation library
- `zlib1g`: Compression library

## Development

### Running Tests Locally

```bash
# Without Docker
cd src
python main.py --input ./2025.12.31.hwp --mode text

# With Docker
docker run --rm -v "$(pwd)/src:/app/data" hwp-parser \
  --input /app/data/2025.12.31.hwp --mode text
```

### Adding New Features

To extend the parser functionality:

1. Add new functions to `src/hwp_parser.py`
2. Update `src/main.py` to expose new CLI options
3. Update `src/__init__.py` to export new functions
4. Rebuild the Docker image
5. Update this documentation

## Version History

- **0.1.0** (2025-12-31): Initial release
  - Text extraction
  - Table parsing
  - JSON export
  - Docker containerization

## License

This project uses the pyhwp library which is licensed under the GPLv3 or later.

## Support

For issues and questions:
- Check the Troubleshooting section above
- Review HWP file compatibility with pyhwp
- Ensure Docker and volume mounts are configured correctly

## Future Enhancements

Potential improvements for future versions:

- Web API interface (Flask/FastAPI)
- Batch processing support
- Additional output formats (CSV, XML)
- Image extraction from HWP files
- Advanced table structure detection
- HWP metadata extraction
- Docker image optimization
