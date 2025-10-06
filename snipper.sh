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

rm -rf $path/results.html
cp template.html $path/results.html
for file in $(ls $path | grep '.png$'); do
  url=$(echo $file | sed 's/\.png$//')
  echo "<div class="item-card"><div class="content"><h3>File: $path/$file</h3><p>URL: <a href="https://$url">https://$url</a></p></div><div class="image-container"><img src="$file" alt="Screenshot of $url"></div></div>" >> $path/results.html 
done
echo "</main></div></body></html>" >> $path/results.html