declare -a arr=(
"https://topsale.am/product/tommy-hilfiger-womens-short-sleeve-polo-sky-captain/15170/"
"https://topsale.am/product/tommy-hilfiger-womens-short-sleeve-polo-black/15174/"
"https://topsale.am/product/tommy-hilfiger-mens-short-sleeve-polo-shirt-in-classic-fit-blue/14938/"
"https://topsale.am/product/tommy-hilfiger-mens-short-sleeve-polo-shirt-in-classic-fit-sky-blue/14941/"
"https://topsale.am/product/pierre-cardin-tipped-polo-shirt-mens-navy/15239/"
"https://topsale.am/product/pierre-cardin-cut-and-sew-printed-polo-mens/15235/"
"https://topsale.am/product/pierre-cardin-tipped-polo-shirt-mens-choral-marl-l/15240/"
"https://topsale.am/product/ck-colorblock-split-logo-crewneck-t-shirt-blue-s/14850/"
"https://topsale.am/product/ck-colorblock-split-logo-crewneck-t-shirt-black/14809/"
"https://topsale.am/product/ck-circular-monogram-logo-crewneck-t-shirt/14852/"
"https://topsale.am/product/u.s.-polo-assn.-mens-classic-fit-color-block-short-sleeve-/15088/"
"https://topsale.am/product/u.s.-polo-assn.-mens-short-sleeve-classic-fit-fancy-pique-polo-shirt/15085/"
"https://topsale.am/product/adidas-must-haves-emblem-tee/14810/"
"https://topsale.am/product/puma-camo-logo-qt-t-shirt-mens-black-camo/15251/"
)


for i in "${arr[@]}"; do
   ./run.sh "$i"
done