#!/bin/bash
export MPLBACKEND=Agg
rm /Users/srinivasansathiamurthy/Documents/graphrag_sri/ragtest/output/.DS_Store


# Assign command-line arguments to variables
METHOD=$1
QUERY=$2

# Define the output file
OUTPUT_FILE="output.txt"

# Run the Python command with the provided method and query string
python3 -m graphrag.query --root ./ragtest --method "$METHOD" --response_type "single paragraph" "$QUERY" > $OUTPUT_FILE 2>&1
