import os
import requests
from moviepy.editor import VideoFileClip

def get_latest_version_from_github():
    repo_url = "https://api.github.com/repos/user/repo/releases/latest"
    response = requests.get(repo_url)
    data = response.json()
    return data["tag_name"]

def convertToGif(filename):
    output_gif = os.path.splitext(filename)[0] + '.gif'
    clip = VideoFileClip(filename)
    clip.write_gif(output_gif)
    return output_gif