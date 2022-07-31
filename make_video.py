import glob
import os
import sys
import tkinter as tk
from subprocess import Popen
from tkinter import filedialog
import shutil


def err_exit(*args, **kwargs):
    print("[ERROR] ", end="", file=sys.stderr)
    print(*args, file=sys.stderr, **kwargs)
    print("\nPress Enter to exit...", file=sys.stderr)
    input()
    sys.exit(1)


def select_file():
    root = tk.Tk()
    root.withdraw()

    return filedialog.askopenfilename()


# https://gist.github.com/anguyen8/d0630b6aef6c1cd79b9a1341e88a573e?permalink_comment_id=2896979#gistcomment-2896979
def make_command(imgs, xfade_len=0.3, save_path="no_audio.mov", ext="jpg"):
    filters = ""
    output = "[0:v]"
    in_command = "-y"
    files = sorted(glob.glob(f"{imgs}/*.{ext}"))
    len_files = len(files)
    if len_files < 1:
        err_exit("input doesn't have .jpg images")

    if not os.path.exists("assets/end_logo.jpg"):
        err_exit("assets/eng_logo.jpg missing")

    files += ["assets/end_logo.jpg"]*2
    len_files += 2
    for i, file in enumerate(files):
        frame_duration = 1
        in_command += f' -loop 1 -t {frame_duration} -i "{file}"'
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
    output += f' -map "[v]" "{save_path}"'

    return f"ffmpeg.exe {in_command} -filter_complex \"{filters} {output}", len_files


def make_audio(vid="no_audio.mov", music='', save_path="result.mov", count=0):
    if count < 1:
        err_exit("input doesn't have .jpg images")

    if not music:
        err_exit("music not selected")

    afade_st = 2 * (count - 3) - 1
    flags = f'-af "afade=in:st=0:d=3,afade=out:st={afade_st}:d=6" -t {count*2} -r 30'
    return f'ffmpeg.exe -y -i "{vid}" -i "{music}" {flags} "{save_path}"'


def main():
    def assert_folder(name):
        if not os.path.exists(name):
            os.makedirs(name)

    def run(command):
        exe = "call " if os.name == "nt" else "./"
        command = exe + command
        print("[RUNNING]", command)

        p = Popen(command, shell=True)
        p.wait()
        if os.name == "nt" and p.returncode != 0:
            err_exit("making video without video")

        return p.returncode

    assert_folder(".cache")
    assert_folder("input")
    music = select_file()

    cmd, count = make_command(imgs="input", save_path=".cache/no_audio.mov")

    run(cmd)
    run(make_audio(vid=".cache/no_audio.mov", music=music, count=count))


if __name__ == "__main__":
    main()
