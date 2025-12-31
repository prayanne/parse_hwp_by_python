#!/bin/bash
# Build the HWP Parser Docker image

echo "Building HWP Parser Docker image..."
docker build -t hwp-parser .

if [ $? -eq 0 ]; then
    echo "Build successful!"
    echo "You can now run the parser with:"
    echo "  ./parse.sh your-file.hwp"
else
    echo "Build failed!"
    exit 1
fi
