#!/bin/bash

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <url_list_file> <output_directory>"
  exit 1
fi

urls="$1"
path="$2"

[[ "${path}" != */ ]] && path="${path}/"

while IFS= read url; do
  filename=$(echo "$url" | cut -d '/' -f3).png
  google-chrome --headless --screenshot="$path""$filename" "$url"
done < $urls
