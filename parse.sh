#!/bin/bash
# Convenience script for parsing HWP files

if [ $# -eq 0 ]; then
    echo "Usage: $0 <hwp-file> [mode] [output]"
    echo ""
    echo "Examples:"
    echo "  $0 data/sample.hwp                    # Extract text to stdout"
    echo "  $0 data/sample.hwp text               # Extract text to stdout"
    echo "  $0 data/sample.hwp json result.json   # Export to JSON"
    echo "  $0 data/sample.hwp tables tables.json # Extract tables"
    echo ""
    echo "Modes: text (default), json, tables"
    exit 1
fi

HWP_FILE=$1
MODE=${2:-text}
OUTPUT=$3

# Get filename from path
FILENAME=$(basename "$HWP_FILE")
CONTAINER_INPUT="/app/data/$FILENAME"

# Ensure directories exist
mkdir -p data output

# Check if file exists
if [ ! -f "$HWP_FILE" ]; then
    echo "Error: File not found: $HWP_FILE"
    exit 1
fi

# Copy file to data directory if not already there
if [[ "$HWP_FILE" != data/* ]]; then
    cp "$HWP_FILE" "data/$FILENAME"
fi

# Build command
CMD="docker run --rm -v $(pwd)/data:/app/data -v $(pwd)/output:/app/output hwp-parser --input $CONTAINER_INPUT --mode $MODE"

# Add output if specified
if [ -n "$OUTPUT" ]; then
    CMD="$CMD --output /app/output/$OUTPUT"
fi

echo "Running: $CMD"
eval $CMD
