#!/bin/bash

tot=0

while read -r i
do
        tmp=0
        tmp=`ffprobe "$i" -show_format 2>/dev/null | grep "^duration" | cut -d '=' -f 2 | cut -d '.' -f 1`

        if [ -n "$tmp" ]; then
                let tot+=$tmp
        fi
done < <(find . -type f -iname "*[.mp3,.wav]")

echo "Total duration: $(($tot)) seconds"
