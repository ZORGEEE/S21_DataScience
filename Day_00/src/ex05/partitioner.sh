#!/bin/sh

input="../ex03/hh_positions.csv"

awk -F ',' '
BEGIN {
    OFS = ","
}
NR == 1 {
    header = $0
    next
}
{
    split($2, datetime, /T/)
    date = datetime[1]

    if (!processed[date]) {
        print header > (date ".csv")
        processed[date] = 1
    }

    print >> (date ".csv")
}
' "$input"