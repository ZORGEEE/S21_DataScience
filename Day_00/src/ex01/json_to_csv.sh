#!/bin/bash

FILE="../ex00/hh.json"

jq -r -f filter.jq $FILE > hh.csv