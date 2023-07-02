import os
import subprocess
import datetime

# Create a directory with prefix and date stamp
prefix = "Ripped"
timestamp = datetime.datetime.now().strftime("%Y%m%d")
directory = f"{prefix}_{timestamp}"

# Check if the directory already exists
if os.path.exists(directory):
    print("Directory already exists. Using existing directory.")
else:
    os.mkdir(directory)

# Navigate to the created or existing directory
os.chdir(directory)

# Prompt the user to enter the URL
url = input("Enter the URL: ")

# Download the video using yt-dlp
subprocess.run([
    "yt-dlp",
    "--external-downloader",
    "aria2c",
    "--username",
    "add username here",
    "--password",
    "enter pass here",
    "--ffmpeg-location",
    "/usr/bin/ffmpeg",
    url
])

# Get the downloaded video file name
filename = None
for file in os.listdir():
    if file.endswith(".mp4"):
        filename = os.path.splitext(file)[0]
        break

if filename:
    # Mux the downloaded video into .mkv format using FFmpeg
    subprocess.run([
        "/usr/bin/ffmpeg",
        "-i",
        f"{filename}.mp4",
        "-c",
        "copy",
        f"{filename}.mkv"
    ])

    # Deleting the original .mp4 file
    os.remove(f"{filename}.mp4")

    # Upload the .mkv file to Google Drive using rclone with progress
    subprocess.run([
        "gclone",
        "--config",
        "/home/ubuntu/Downloads/sab/scripts/rclone.conf",
        "move",
        f"{filename}.mkv",
        "share:test",
	"--drive-chunk-size",
	"256M",
	"--transfers",
	"20",
        "-P"
    ])
else:
    print("No .mp4 file found.")
