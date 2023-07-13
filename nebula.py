import os
import subprocess
import datetime

# Create Dir
prefix = "nebula"
timestamp = datetime.datetime.now().strftime("%Y%m%d")
directory = f"{prefix}_{timestamp}"

# Check if dir exists
if os.path.exists(directory):
    print("Directory already exists. Using existing directory.")
else:
    os.mkdir(directory)

# go to dir
os.chdir(directory)

# prompt user for URL
url = input("Enter the URL: ")

# initiate yt-dlp to download
subprocess.run([
    "yt-dlp",
    "--external-downloader",
    "aria2c",
    "--username",
    "USERNAME/EMAIL HERE",
    "--password",
    "PASSWORD HERE",
    "--write-subs",
    "--ffmpeg-location",
    "/usr/bin/ffmpeg",
    url
])

# mehhhh
filename = None
for file in os.listdir():
    if file.endswith(".mp4"):
        filename = os.path.splitext(file)[0]
        break

if filename:
    # Find the subtitle file with .vtt extension
    subtitle = None
    for file in os.listdir():
        if file.endswith(".vtt"):
            subtitle = os.path.splitext(file)[0]
            break

    if subtitle:
        # convrt vtt to srt
        subprocess.run([
            "/usr/bin/ffmpeg",
            "-i",
            f"{subtitle}.vtt",
            f"{subtitle}.srt"
        ])

        # muxvux
        subprocess.run([
            "/usr/bin/ffmpeg",
            "-i",
            f"{filename}.mp4",
            "-i",
            f"{subtitle}.srt",
            "-c",
            "copy",
            "-scodec",
            "srt",
            f"{filename}.mkv"
        ])

        # delete the files
        os.remove(f"{filename}.mp4")
        os.remove(f"{subtitle}.vtt")
        os.remove(f"{subtitle}.srt")

        # rclonrrrrr
        subprocess.run([
            "gclone",
            "--config",
            "/path/to/rclone.conf",
            "move",
            f"{filename}.mkv",
            "remote:",
            "--drive-chunk-size",
            "256M",
            "--transfers",
            "20",
            "-P"
        ])

        print("done!")
    else:
        print("No .vtt subtitle file found.")
else:
    print("No .mp4 file found.")
