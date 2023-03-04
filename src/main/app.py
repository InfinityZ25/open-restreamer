from typing import List

import ffmpeg
from dotenv import dotenv_values
from flask import Flask, jsonify, request
from pymongo import MongoClient

config = dotenv_values(".env")
app = Flask(__name__)
# Store ongoing processes streams in this map. Ideally this should be stored in a database, but in memory copy has to be enough for this example. Make it thread safe if you want to use it in a multi-threaded environment.
stream_processes = {}

# Connect to the database
mongo = MongoClient(config['ATLAS_URI'])
db = mongo[config['DB_NAME']]


# An endpoint that checks a collection in the database to see if the auth token provided is valid.
@app.route('/auth', methods=['POST'])
def auth():
    """ Checks if the given auth token is valid. """
    auth_token = request.get_json().get('auth_token', None)
    if not auth_token:
        return jsonify({'message': 'auth token not provided'}), 400

    user = db['auth'].find_one({'auth_token': auth_token})
    print(user)
    if not user:
        return jsonify({'message': 'invalid auth token'}), 401

    user_info = {
        'username': user['user'],
        'email': 'none@just.pics',
        'auth_token': user['auth_token']
    }

    return jsonify({'message': 'auth token valid', 'user_info': user_info})


@app.route('/status/<stream_id>', methods=['GET'])
def get_stream_status(stream_id):
    """ Returns the status of the stream with the given stream id."""
    global stream_processes

    if stream_id not in stream_processes:
        return jsonify({'message': 'stream not found'}), 404

    twitch_process, youtube_process = stream_processes[stream_id]

    twitch_status = 'running' if twitch_process and not twitch_process.poll() else 'stopped'
    youtube_status = 'running' if youtube_process and not youtube_process.poll() else 'stopped'

    return jsonify({
        'twitch': twitch_status,
        'youtube': youtube_status
    })


def get_streaming_input(rtmp_url_with_key: str) -> ffmpeg.input:
    """Returns an ffmpeg input stream for the given rtmp url and stream key."""
    return ffmpeg.input(rtmp_url_with_key, format='flv')


@app.route('/start/<stream_id>', methods=['POST'])
def start_stream(stream_id):
    """ Starts a stream with the given stream id and stream keys. """
    global stream_processes

    if stream_id in stream_processes and not any(poll is not None and poll.poll() is None for poll in stream_processes[stream_id]):
        return jsonify({'message': 'stream already running'}), 400

    stream_data = request.get_json()
    keys = stream_data.get('keys', {})
    twitch_key = keys.get('twitch')
    youtube_key = keys.get('youtube')

    twitch_metadata = stream_data.get('stream_metadata', {}).get('twitch', {})
    youtube_metadata = stream_data.get(
        'stream_metadata', {}).get('youtube', {})

    # define the rtmp servers to stream to
    twitch_rtmp_url = f'rtmp://live.twitch.tv/app/{twitch_key}' if twitch_key else None
    youtube_rtmp_url = f'rtmp://a.rtmp.youtube.com/live2/{youtube_key}' if youtube_key else None

    # A variable to store the required input streams.
    outputs: List[ffmpeg.input] = []

    # Twitch
    if twitch_rtmp_url:
        twitch_output = get_streaming_input(twitch_rtmp_url).output(
            twitch_rtmp_url,
            format='flv',
            **twitch_metadata
        )
        outputs.append(twitch_output)

    # YouTube
    if youtube_rtmp_url:
        youtube_output = get_streaming_input(twitch_rtmp_url).output(
            youtube_rtmp_url,
            format='flv',
            **youtube_metadata
        )
        outputs.append(youtube_output)

    processes = [ffmpeg.run_async(output) for output in outputs]
    stream_processes[stream_id] = processes

    return jsonify({'message': f'stream {stream_id} started'})


# Programme entry poiny
if __name__ == '__main__':
    app.run(debug=True)  # flash stuff
