trap ctrl_c INT
function ctrl_c() {
	mv input/todos.html input/todo.html 2> /dev/null
	exit 0
}
rm -rf categories/* 2> /dev/null
if [ ! -d categories ]; then
	mkdir categories
fi
cp input/todo.html input/todos.html


declare -A category_map
declare -A sub_category_map
category_map["178"]="Men"
category_map["179"]="Womeen"
category_map["180"]="Boys"
category_map["189"]="Girls"
category_map["181"]="Accessories"

# Men
sub_category_map["182"]="Footwear"
sub_category_map["195"]="TShirts_Polos"
sub_category_map["194"]="Jeans"
sub_category_map["196"]="Flip_Flops"
sub_category_map["200"]="Sportswear"
sub_category_map["215"]="Jacket"
sub_category_map["209"]="Swimwears_and_Underwears"
sub_category_map["183"]="Sweaters"

# Women
sub_category_map["187"]="Footwear"
sub_category_map["205"]="TShirts_Polos"
sub_category_map["204"]="Dresses"
sub_category_map["208"]="Jeans"
sub_category_map["206"]="Blooses"
sub_category_map["214"]="Jackets"
sub_category_map["207"]="Sportswear"
sub_category_map["203"]="Flip_Flops"

# Boys and Gilrs
sub_category_map["190"]="Clothing"
sub_category_map["191"]="Footwear"
sub_category_map["192"]="Clothing"
sub_category_map["193"]="Footwear"

# Accessories
sub_category_map["216"]="Watches"
sub_category_map["197"]="Belts"
sub_category_map["198"]="Wallets"
sub_category_map["199"]="Sunglasses"

arr=""
arr=($(cat input/todos.html | grep -o "https://topsale.am/category/[a-zA-Z0-9\+%;_&,\./\-]*"))
len="${#arr[@]}"
echo " with ${len} categories"
ctr=0
for i in "${arr[@]}"; do
	ctr=$((ctr + 1))
	name=$(grep -o "category/.*" <<< "$i")
	name=${name:9}
	name=$(grep -o "^[^/]*" <<< "$name")
	folder=$(grep -o -E "[0-9]+/[0-9]+" <<< "$i")

	category_number=$(grep -o -E -m1 "[0-9]+" <<< "$folder" | head -n1)
	sub_category_number=$(grep -o -E -m1 "[0-9]+" <<< "$folder" | tail -n1)
	category=${category_map["$category_number"]}
	sub_category=${sub_category_map["$sub_category_number"]}
	echo $sub_category
	folder="$category/$sub_category"
	mkdir -p categories/$folder
	echo
	echo "Starting Category $name [$ctr/$len]"
	curl --silent "$i" --output input/todo.html
	./do_all.sh --novid

	mv results/* categories/$folder
done

ctrl_c