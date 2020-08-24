#------------Settings-------------
use_set=false
set_len=2
#---------------------------------
trap ctrl_c INT
function ctrl_c() {
  rm -rf results/*
  rm -f vid/no_audio.mov tmp.html
  exit 0
}

rm -rf results/*

if grep -q "Ընտրել" input/todo.html; then
  cat input/todo.html | grep "Ընտրել" > tmp.html
  num_of_items=$(cat tmp.html | wc -l)
  mv tmp.html input/todo.html
  printf "Page detected; with %d products", "$num_of_items"
fi



arr=""
if [ -f input/todo.html ]; then
  arr=($(cat input/todo.html | grep -o "https://topsale.am/product/[a-zA-Z0-9+%;_&,\./\-]*"))
else
  echo >&2 "input/todo.html is missing"
  exit 1
fi
if [ ! -f input/music.mp3 ]; then
  echo >&2 "music.mp3 is missing please place music at input/music.mp3"
  exit 1
fi
len="${#arr[@]}"
ctr=1
set=1

for i in "${arr[@]}"; do
  echo "$i"
  printf "[%d/%d] " $ctr $len
  if [ "$use_set" = true ]; then
    ./run.sh $i $set # for sets
    num=$(((ctr % set_len)))
    if ! ((num)); then
      num=3
    fi
    mv "results/$set/set_res.jpg" "results/$set/$num.jpg"
  else
    ./run.sh "$i" # for individual
  fi

  if ! ((ctr % set_len)); then
    set=$((set + 1))
  fi
  ctr=$((ctr + 1))
  echo
done

if [ "$use_set" = true ]; then
  res=$(ls results | grep -o "[0-9]*")
  for i in $res; do
    set=$(find "results/$i/" | grep "results/[0-9]*/.*\.jpg")
    k=1
    for j in $set; do
      mv "$j" "results/$i$k.jpg"
      k=$((k + 1))
    done
    rmdir "results/$i"
  done
fi

cp assets/end_logo.jpg results/z_logo.jpg
cp assets/end_logo.jpg results/zz_logo.jpg
afade_st=$((2 * (len - 1) - 1))
image_count=$((len + 2))
./make_ffmpeg.sh "$image_count"
rm results/z_logo.jpg results/zz_logo.jpg

ffmpeg -y -i "vid/no_audio.mov" -i input/music.mp3 -vol 160 -af "afade=in:st=0:d=3,afade=out:st=$afade_st:d=6" -shortest -r 30 vid/output.mov
if [ $? -eq 1 ]; then
  printf "\n--\n"
  read -p "Video Failed. Press enter to continue"
fi
mpv vid/output.mov
ctrl_c
