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
    "USERNAME/EMAIL HERE",
    "--password",
    "PASSWORD HERE",
    "--write-subs",
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
    # Find the subtitle file with .vtt extension
    subtitle = None
    for file in os.listdir():
        if file.endswith(".vtt"):
            subtitle = os.path.splitext(file)[0]
            break

    if subtitle:
        # Convert the subtitle from .vtt to .srt format using FFmpeg
        subprocess.run([
            "/usr/bin/ffmpeg",
            "-i",
            f"{subtitle}.vtt",
            f"{subtitle}.srt"
        ])

        # Mux the downloaded video and converted subtitle into .mkv format using FFmpeg
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

        # Deleting the original .mp4, .vtt, and .srt files
        os.remove(f"{filename}.mp4")
        os.remove(f"{subtitle}.vtt")
        os.remove(f"{subtitle}.srt")

        # Upload the .mkv file to Google Drive using rclone
        subprocess.run([
            "gclone",
            "--config",
            "/path/to/rclone.conf",
            "move",
            f"{filename}.mkv",
            "share:test",
            "--drive-chunk-size",
            "256M",
            "--transfers",
            "20",
            "-P"
        ])

        print("Video and subtitles muxed successfully!")
    else:
        print("No .vtt subtitle file found.")
else:
    print("No .mp4 file found.")
