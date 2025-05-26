#!/bin/bash

echo "Обработка запроса..."

AGENT="User-Agent: api-test-agent"

URL="https://api.hh.ru/vacancies?text=Data+Scientist&per_page=20"

curl -k -H "$AGENT" "$URL" | jq > hh.json
