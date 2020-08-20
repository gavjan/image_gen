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
	rm result.jpg 2> /dev/null
	rm brand.png 2> /dev/null
	rm brand.svg 2> /dev/null
}

ctrl_c

curl "$1" --silent --output index.html

image_link=$(grep -o -a -m 1 -E -h -r "https://topsale.am/img/prodpic/[a-zA-Z0-9_.-]*.(jpg|png)" index.html | head -1)
image_name=$(grep -o -a -m 1 -E -h -r "https://topsale.am/img/prodpic/[a-zA-Z0-9_.-]*.(jpg|png)" index.html | head -1 | grep -E -o "/[a-zA-Z0-9_.-]*.(jpg|png)" | grep -E -o "[a-zA-Z0-9_.-]*.(jpg|png)")
image_name_no_extension="${image_name::-4}"
price=$(grep -m 1 -A 1 "<span class=\"regular\">" index.html | grep -o "[0-9,]*" )
brand_png_link=$(grep -o -a -m 1 -h -r "<div class=\"product-brnd-logo\"><img src=\"https://topsale.am/img/brands/.*\.png\"></div>" index.html | head -1 | grep -o "https://topsale.am/img/brands/.*\.png")
brand_svg_link=$(grep -o -a -m 1 -h -r "<div class=\"product-brnd-logo\"><img src=\"https://topsale.am/img/brands/.*\.svg\"></div>" index.html | head -1 | grep -o "https://topsale.am/img/brands/.*\.svg")
item_name=$(grep -o -a -m 1 -h -r "<meta property=\"og:title\" content=\"TopSale.am - [^\"/>]*" | grep -o "\"TopSale.am - [^\"]*")
item_name="${item_name:14}"
raw_product_data=$(xmllint --html --xpath '/html/body/div[@class="details-block"]' index.html 2>/dev/null)

off_tag="none"
if grep -q "https://topsale.am/img/8c93320-2.png" <<< "$raw_product_data"
then
    off_tag="20_off"
elif grep -q "https://topsale.am/img/6f814sale.png" <<<  "$raw_product_data"
then
    off_tag="50_20"
fi
printf "\noff_tag = %s\n" "$off_tag"

printf "Starting %s" "$item_name"

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
    python3 image_gen.py $parsed_price $off_tag
  fi
fi


if [ $# -eq 2 ]; then
  if [ ! -d results/$2 ]; then
    mkdir -p results/$2
  fi
  mv result.jpg results/$2/set_res.jpg
else
  if [ ! -d results ]; then
    mkdir results
  fi
  mv result.jpg results/"$image_name_no_extension".jpg
fi



ctrl_c "$image_name"
