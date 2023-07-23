for file in ./*.opus
do
  ffmpeg -i "$file" -c:a aac "${file%.*}.m4a"
  rm "$file"
done