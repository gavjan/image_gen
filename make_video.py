# https://gist.github.com/anguyen8/d0630b6aef6c1cd79b9a1341e88a573e?permalink_comment_id=2896979#gistcomment-2896979
import glob
from subprocess import Popen


def make_command(imgs, xfade_len=0.3, save_path="no_audio.mp4", ext="jpg"):
    filters = ""
    output = "[0:v]"
    in_command = "-y"
    files = sorted(glob.glob(f"{imgs}/*.{ext}"))
    len_files = len(files)

    for i, file in enumerate(files):
        frame_duration = 1
        in_command += " -loop 1 -t {} -i {}".format(frame_duration, file)
        frame_num = i + 1

        if i != len_files - 1:
            filters += " [{}:v][{}:v]blend=all_expr='".format(frame_num, i)
            filters += "A*(if(gte(T,{0}),1,T/{0}))".format(xfade_len)
            filters += "+B*(1-(if(gte(T,{0}),1,T/{0})))'".format(xfade_len)
            filters += "[b{}v];".format(frame_num)

        if i > 0:
            output += "[b{0}v][{0}:v]".format(i)

    frame_count = len_files * 2 - 1
    output += "concat=n={}:v=1:a=0,format=yuv420p[v]\"".format(frame_count)
    output += " -map \"[v]\" {}".format(save_path)

    return f"./ffmpeg {in_command} -filter_complex \"{filters} {output}"


if __name__ == "__main__":
    command = make_command(imgs="results")
    print(command)
    exit(Popen(command, shell=True).returncode)
