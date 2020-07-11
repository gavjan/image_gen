trap ctrl_c INT
function ctrl_c() {
  rm -f results/*
  vid/no_audio.mov
  exit 0
}

rm -f results/*

declare -a arr=(
"https://topsale.am/product/karl-speckled-twofer-sweater/15223/"
)
if [ -f todo.html ]; then
  arr=($(cat todo.html | grep -o "https://topsale.am/product/[a-z0-9;_&,\./\-]*"))
fi
if [ ! -f music/music.mp3 ]; then
  >&2 echo "music.mp3 is missing please place music at music/music.mp3"
  exit 1
fi
len="${#arr[@]}"
ctr=1
set=1

for i in "${arr[@]}"; do
  echo "$i"
  printf "[%d/%d] " $ctr $len
    ./run.sh "$i" # for individual
    #./run.sh $i $set # for sets
  if ! ((ctr % 3)); then
    set=$((set+1))
  fi
  ctr=$((ctr+1))
  echo
done


cp assets/end_logo.png results/z_logo.png
cp assets/end_logo.png results/zz_logo.png
afade_st=$((2*(len-1)-1))
image_count=$((len+2))
./make_ffmpeg.sh "$image_count"
rm results/z_logo.png results/zz_logo.png

ffmpeg -y -i "vid/no_audio.mov" -i music/music.mp3 -af "afade=in:st=0:d=3,afade=out:st=$afade_st:d=6" -shortest -r 30 vid/output.mov
mpv vid/output.mov

ctrl_c
