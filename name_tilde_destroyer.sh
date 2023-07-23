for file in *.*
do
  base_name="${file%.*}"
  extension="${file##*.}"
  new_name="${base_name%-*}.${extension}"
  mv -- "$file" "$new_name"
done