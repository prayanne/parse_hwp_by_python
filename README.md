# HWP Parser

A Docker-based Python module for parsing HWP (Hangul Word Processor) files and extracting text and tables.

## Quick Start

### 1. Build the Docker Image

```bash
docker build -t hwp-parser .
```

Or using Docker Compose:

```bash
docker-compose build
```

### 2. Prepare Your Files

Create a `data` directory and place your HWP files there:

```bash
mkdir -p data output
cp your-file.hwp data/
```

### 3. Run the Parser

#### Extract Text

```bash
docker run --rm -v "$(pwd)/data:/app/data" hwp-parser \
  --input /app/data/your-file.hwp --mode text
```

#### Export to JSON

```bash
docker run --rm \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/output:/app/output" \
  hwp-parser \
  --input /app/data/your-file.hwp \
  --mode json \
  --output /app/output/result.json
```

#### Extract Tables

```bash
docker run --rm \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/output:/app/output" \
  hwp-parser \
  --input /app/data/your-file.hwp \
  --mode tables \
  --output /app/output/tables.json
```

### Using Docker Compose (Easier!)

```bash
# Extract text
docker-compose run --rm hwp-parser \
  --input /app/data/your-file.hwp --mode text

# Export to JSON
docker-compose run --rm hwp-parser \
  --input /app/data/your-file.hwp \
  --mode json \
  --output /app/output/result.json
```

## Features

- Extract plain text from HWP files
- Parse pipe-delimited tables
- Export to JSON format
- Text normalization
- Docker containerization for consistent environment

## Documentation

For detailed documentation, see [docs.md](./docs.md)

## Project Structure

```
hwp_parse/
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose setup
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── docs.md                # Detailed documentation
├── src/                   # Source code
│   ├── __init__.py       # Module initialization
│   ├── main.py           # CLI entry point
│   └── hwp_parser.py     # Core parser
├── data/                  # Place your HWP files here
└── output/                # Output files go here
```

## Command-Line Options

- `--input PATH`: Path to HWP file (required)
- `--output PATH`: Output file path (for json/tables mode)
- `--mode {text|json|tables}`: Output mode (default: text)
- `--normalize`: Normalize text output

## Requirements

- Docker 20.10+
- Docker Compose (optional)

## License

GPLv3 or later (due to pyhwp dependency)
