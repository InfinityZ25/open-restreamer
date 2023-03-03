# create a Flask app that exposes a GET endpoint to check the status of the ap

import subprocess

from index import get_index_html

# Set up the RTMP server using Flask
from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return get_index_html()


@app.route('/stream', methods=['POST'])
def stream():
    # Use FFMPEG to encode and stream the incoming RTMP stream to YouTube and Twitch
    youtube_stream_url = 'rtmp://youtube_stream_url'
    twitch_stream_url = 'rtmp://twitch_stream_url'

    ffmpeg_cmd = f"ffmpeg -i {request.stream} -c:v libx264 -preset fast -b:v 3000k -maxrate 3000k -bufsize 6000k -c:a aac -b:a 128k -f flv {youtube_stream_url} -f flv {twitch_stream_url}"

    # Start the FFMPEG subprocess
    subprocess.Popen(ffmpeg_cmd.split())

    return 'Streaming started successfully!'


if __name__ == '__main__':
    app.run(debug=True)
