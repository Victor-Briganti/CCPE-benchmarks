#!/bin/bash

raw_dir="./raw"
csv_dir="./csv"

for dir in "$raw_dir"/*; do
	dirname=$(basename "$dir")

	for subdir in "$dir"/*; do
		if [[ ! -d $subdir ]]; then
			filename=$(basename "$subdir")
			echo $filename
			sed -e "s/ $//g" -e "s/ /,\n/g" -e "s/[0-9]$/&,/g" $subdir > "$csv_dir/$dirname/$filename.csv"
		else 
			subdirname=$(basename "$subdir")
			echo $subdirname
			for file in "$subdir"/*; do
				filename=$(basename "$file")
				echo $filename
				sed -e "s/ $//g" -e "s/ /,\n/g" -e "s/[0-9]$/&,/g" $subdir/$filename > $csv_dir/$dirname/$subdirname/$filename.csv
			done
		fi
	done
done
