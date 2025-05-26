#!/bin/sh

output="hh_concatenated.csv"

files=$(find ./*.csv | sort -n)

if [ -z "$files" ]; then
    echo "Error: CSV files not found." >&2
    exit 1
fi

head -1 "$(echo "$files" | head -1)" > "$output"

for file in $files; do
    tail -n +2 "$file" >> "$output"
done