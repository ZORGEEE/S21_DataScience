#!/bin/sh

input_file="../ex02/hh_sorted.csv"
output_file="hh_positions.csv"

awk -v FPAT='([^,]+)|("[^"]+")' '
BEGIN {
    OFS = ","
}
NR == 1 {
    print $0
    next
}
{
    name = $3
    lower_name = tolower(name)

    found_roles = ""
    if (lower_name ~ /junior/) found_roles = "Junior"
    if (lower_name ~ /middle/) found_roles = found_roles (found_roles ? "/" : "") "Middle"
    if (lower_name ~ /senior/) found_roles = found_roles (found_roles ? "/" : "") "Senior"

    $3 = (found_roles == "") ? "\"-\"" : "\"" found_roles "\""
    print
}
' "$input_file" > "$output_file"