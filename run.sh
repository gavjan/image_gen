# ./run.sh <product_link> (optional)<set_number>

#------------Settings-------------
split=false
#---------------------------------
trap ctrl_c INT
function debug_info() {
  printf "\n\n--------Debug Info--------\n"
  echo "files before editing:"
  ls
  echo "image_link = \"$image_link\""
  echo "brand_svg_link = \"$brand_svg_link\""
  echo "brand_png_link = \"$brand_png_link\""
  echo "item_name = \"$item_name\""
  echo "--------------------------"
  echo
}
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
brand_png_link=$(grep -o -a -m 1 -h -r "<div class=\"product-brnd-logo\"><img src=\"https://topsale.am/img/brands/.*\.png\"></div>" index.html | head -1 | grep -o "https://topsale.am/img/brands/.*\.png")
brand_svg_link=$(grep -o -a -m 1 -h -r "<div class=\"product-brnd-logo\"><img src=\"https://topsale.am/img/brands/.*\.svg\"></div>" index.html | head -1 | grep -o "https://topsale.am/img/brands/.*\.svg")
item_name=$(grep -o -a -m 1 -h -r "<meta property=\"og:title\" content=\"TopSale.am - [^\"/>]*" | grep -o "\"TopSale.am - [^\"]*")
item_name="${item_name:14}"

printf "Starting $item_name"

curl --silent "$image_link" --output input.jpg
curl --silent "$brand_svg_link" --output brand.svg
curl --silent "$brand_png_link" --output brand.png


if [ -f brand.svg ]; then
  cairosvg brand.svg -o brand.png #2> /dev/null
fi

#debug_info

if [ ! -f input.jpg ]; then

    printf "\n[ERROR] Product Image Download Failed\n"
    echo "Product link: \"$image_link\""
    ls
    ctrl_c
    exit 1
elif [ ! -f brand.png ]; then

    printf "\n[ERROR] Brand Image Download Failed\n"
    echo "brand.svg link: \"$brand_svg_link\""
    echo "brand.png link: \"$brand_png_link\""
    ctrl_c
    exit 1
else
  parsed_price="$price"
  if [ "$split" = true ]; then
    python3 split.py $parsed_price
  else
    python3 image_gen.py $parsed_price
  fi
fi


if [ $# -eq 2 ]; then
  if [ ! -d results/$2 ]; then
    mkdir -p results/$2
  fi
  mv result.png results/$2/set_res.png
else
  if [ ! -d results ]; then
    mkdir results
  fi
  mv result.png results/"$image_name_no_extension".png
fi



ctrl_c "$image_name"
