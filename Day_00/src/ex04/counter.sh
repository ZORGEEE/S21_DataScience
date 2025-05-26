#!/bin/sh

input="../ex03/hh_positions.csv"
output="hh_uniq_positions.csv"

echo '"name","count"' > "$output"

tail -n +2 "$input" | \
awk -F ',' '
{
    if ($3 != "\"-\"") {
        count[$3]++
    }
}
END {
    for (name in count) {
        printf "%s,%d\n", name, count[name]
    }
}' | \
sort -t ',' -k2,2nr -k1,1 >> "$output"