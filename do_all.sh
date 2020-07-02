declare -a arr=(
"https://topsale.am/product/hm-patterned-jersey-dress-black-flora/14977/"
"https://topsale.am/product/hm-lace-dress-white/14971/"
"https://topsale.am/product/hm-flounced-jersey-dress-dark-blue-floral/14939/"
"https://topsale.am/product/hm-belted-cotton-shorts-dark-blue/14934/"
"https://topsale.am/product/hm-belted-cotton-shorts-light-yellow/14933/"
"https://topsale.am/product/hm-printed-jersey-top-powder-pink-_-paris/14963/"
"https://topsale.am/product/hm-printed-jersey-top-white-_-brklyn/14964/"
"https://topsale.am/product/hm-printed-jersey-top-white-_-statesville/14965/"
"https://topsale.am/product/hm-printed-jersey-top,white-usa/14966/"
"https://topsale.am/product/hm-boxy-t-shirt-mint-green-_-flowers/14936/"
"https://topsale.am/product/hm-boxy-t-shirt-white_-floral/14937/"
)


for i in "${arr[@]}"; do
   ./run.sh "$i"
done