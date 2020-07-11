#!/bin/bash
# Anh Nguyen <anh.ng8@gmail.com>
# 2016-04-30
# MIT License

#----------------------------------------------------------------
# SETTINGS
input_dir="results/"  # Replace this by a path to your folder /path/to/your/folder
n_files=$1                        # Replace this by a number of images
files=`ls ${input_dir}/*.png | head -${n_files}`  # Change the file type to the correct type of your images
output_file="vid/no_audio.mov"           # Name of output video
crossfade=0.2                     # Crossfade duration between two images
#----------------------------------------------------------------

# Making an ffmpeg script...
input=""
filters=""
output="[0:v]"

i=0

for f in ${files}; do
  input+=" -loop 1 -t 1 -i $f"

  next=$((i+1))
  if [ "${i}" -ne "$((n_files-1))" ]; then
    filters+=" [${next}:v][${i}:v]blend=all_expr='A*(if(gte(T,${crossfade}),1,T/${crossfade}))+B*(1-(if(gte(T,${crossfade}),1,T/${crossfade})))'[b${next}v];"
  fi

  if [ "${i}" -gt "0" ]; then
    output+="[b${i}v][${i}:v]"
  fi

  i=$((i+1))
done

output+="concat=n=$((i * 2 - 1)):v=1:a=0,format=yuv420p[v]\" -map \"[v]\" ${output_file}"

script="ffmpeg -y ${input} -filter_complex \"${filters} ${output}"

echo ${script}

# Run it
eval "${script}"
