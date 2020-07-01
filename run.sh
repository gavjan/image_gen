trap ctrl_c INT
function ctrl_c() {
	rm index.html 2> /dev/null
	rm input.jpg 2> /dev/null
	rm "$1" 2> /dev/null
	rm result.png 2> /dev/null
	rm brand.png 2> /dev/null
	rm brand.svg 2> /dev/null
}

ctrl_c


curl "$1" --silent --output index.html

image_link=$(grep -o -a -m 1 -h -r "https://topsale.am/img/prodpic/[a-zA-Z0-9_.-]*.jpg" index.html | head -1)
image_name=$(grep -o -a -m 1 -h -r "https://topsale.am/img/prodpic/[a-zA-Z0-9_.-]*.jpg" index.html | head -1 | grep -o "/[a-zA-Z0-9_.-]*.jpg" | grep -o "[a-zA-Z0-9_.-]*.jpg")
image_name_no_extension="${image_name::-4}"
price=$(grep -m 1 -A 1 "<span class=\"regular\">" index.html | grep -o "[0-9,]*" )
brand_link=$(grep -o -a -m 1 -h -r "<div class=\"product-brnd-logo\"><img src=\"https://topsale.am/img/brands/[a-zA-Z0-9_.-]*\.svg\"></div>" index.html | head -1 | grep -o "https://topsale.am/img/brands/[a-zA-Z0-9_.-]*\.svg")

item_name=$(grep -o -a -m 1 -h -r "<meta property=\"og:title\" content=\"TopSale.am - .*\" />" | grep -o "\"TopSale.am - .*\"")
item_name="${item_name:14}"
item_name="${item_name::-1}"

echo
printf "Starting $item_name"

curl --silent "$image_link" --output input.jpg
curl --silent "$brand_link" --output brand.svg

inkscape -p brand.svg -o brand.png 2> /dev/null
if [ ! -f input.jpg ]; then
    >&2 echo "[ERROR] Image Download Failed"
    ctrl_c
    exit 1
else
  parsed_price="$price"
  python image_gen.py $parsed_price
fi

if [ ! -d results ]; then
  mkdir results
fi
mv result.png results/"$image_name_no_extension".png

ctrl_c "$image_name"
