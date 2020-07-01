trap ctrl_c INT
function ctrl_c() {
	rm index.html
	rm input.jpg 2> /dev/null
	rm "$1" 2> /dev/null
	rm result.png 2> /dev/null
}

ctrl_c
wget "$1"
image_link=$(grep -o -a -m 1 -h -r "https://topsale.am/img/prodpic/[a-zA-Z0-9_.-]*.jpg" index.html | head -1)
image_name=$(grep -o -a -m 1 -h -r "https://topsale.am/img/prodpic/[a-zA-Z0-9_.-]*.jpg" index.html | head -1 | grep -o "/[a-zA-Z0-9_.-]*.jpg" | grep -o "[a-zA-Z0-9_.-]*.jpg")
image_name_no_extension="${image_name::-4}"

price=$(grep -m 1 -A 1 "<span class=\"regular\">" index.html | grep -o "[0-9,]*" )


wget "$image_link"
mv "$image_name" input.jpg

if [ ! -f input.jpg ]; then
    >&2 echo "[ERROR] Image Download Failed"
    exit 1
else
  python image_gen.py "$price"
fi

if [ ! -d results ]; then
  mkdir results
fi
mv result.png results/"$image_name_no_extension".png

ctrl_c "$image_name"
