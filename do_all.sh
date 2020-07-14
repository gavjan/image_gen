trap ctrl_c INT
function ctrl_c() {
  rm -rf results/*
  vid/no_audio.mov
  exit 0
}

rm -rf results/*
#------------Settings-------------
use_set=false
set_len=2
#---------------------------------

declare -a arr=(
  "https://topsale.am/product/karl-speckled-twofer-sweater/15223/"
)
if [ -f todo.html ]; then
  arr=($(cat todo.html | grep -o "https://topsale.am/product/[a-z0-9;_&,\./\-]*"))
fi
if [ ! -f music/music.mp3 ]; then
  echo >&2 "music.mp3 is missing please place music at music/music.mp3"
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
    mv "results/$set/set_res.png" "results/$set/$num.png"
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
    set=$(find "results/$i/" | grep "results/[0-9]*/.*\.png")
    k=1
    for j in $set; do
      mv "$j" "results/$i$k.png"
      k=$((k + 1))
    done
    rmdir "results/$i"
  done
fi

cp assets/end_logo.png results/z_logo.png
cp assets/end_logo.png results/zz_logo.png
afade_st=$((2 * (len - 1) - 1))
image_count=$((len + 2))
./make_ffmpeg.sh "$image_count"
rm results/z_logo.png results/zz_logo.png

ffmpeg -y -i "vid/no_audio.mov" -i music/music.mp3 -vol 160 -af "afade=in:st=0:d=3,afade=out:st=$afade_st:d=6" -shortest -r 30 vid/output.mov

ctrl_c
