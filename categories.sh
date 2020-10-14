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
	mkdir -p categories/$folder

	echo "\nStarting Category $name [$ctr/$len]"
	curl --silent "$i" --output input/todo.html
	./do_all.sh --novid

	mv results/* categories/$folder
done

ctrl_c