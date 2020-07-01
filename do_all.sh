declare -a arr=(
"https://topsale.am/product/u.s.-polo-assn.-womens-classic-fit-pique-polo-shirt---white/15183/"
"https://topsale.am/product/tommy-hilfiger-womens-short-sleeve-polo-flame/15172/"
"https://topsale.am/product/ck-monogram-logo-camo-crewneck-cropped-t-shirt;-white/15076/"
"https://topsale.am/product/u.s.-polo-assn.-juniors-lace-v-neck-t-shirt/15185/"
"https://topsale.am/product/u.s.-polo-assn.-womens-slim-fit-pique-polo-shirt/15300/"
"https://topsale.am/product/adidas-originals-3mc-sneaker,-black/14837/"
"https://topsale.am/product/nike-star-runner-infants-trainers/14886/"
"https://topsale.am/product/adidas-boys-lite-racer-2.0-k-sneaker,-blue/14889/"
"https://topsale.am/product/avia-boys-avi-factor-sneaker/14890/"
"https://topsale.am/product/avia-boys-avi-ryder-sneaker,-flame/14891/"
)


for i in "${arr[@]}"; do
   ./run.sh "$i"
done