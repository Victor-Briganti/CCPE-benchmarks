#!/bin/bash

raw_dir="./raw"
csv_dir="./csv"

for dir in "$raw_dir"/*; do
	dirname=$(basename "$dir")

	for subdir in "$dir"/*; do
		if [[ ! -d $subdir ]]; then
			filename=$(basename "$subdir")
			sed -e "s/[0-9]://g" -e "s/ /,/g" -e "s/^,//g" -e "s/,$//g" -e "2d" -e "4d" -e "6d" -e "8d" -e "10d" $subdir > "$csv_dir/$dirname/$filename.csv" 
		else 
			subdirname=$(basename "$subdir")
			for file in "$subdir"/*; do
				filename=$(basename "$file")
				sed -e "s/[0-9]://g" -e "s/ /,/g" -e "s/^,//g" -e "s/,$//g" -e "2d" -e "4d" -e "6d" -e "8d" -e "10d" $file > "$csv_dir/$dirname/$subdirname/$filename.csv"
			done
		fi
	done
done

