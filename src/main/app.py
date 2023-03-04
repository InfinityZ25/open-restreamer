import ffmpeg
from flask import Flask, jsonify, request

app = Flask(__name__)
stream_processes = {}


@app.route('/status/<stream_id>', methods=['GET'])
def get_stream_status(stream_id):
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


@app.route('/start/<stream_id>', methods=['POST'])
def start_stream(stream_id):
    global stream_processes

    if stream_id in stream_processes and not any(poll is not None and poll.poll() is None for poll in stream_processes[stream_id]):
        return jsonify({'message': 'stream already running'}), 400

    stream_data = request.get_json()
    keys = stream_data.get('keys', {})
    twitch_key = keys.get('twitch')
    youtube_key = keys.get('youtube')

    twitch_metadata = stream_data.get('stream_metadata', {}).get('twitch', {})
    youtube_metadata = stream_data.get('stream_metadata', {}).get('youtube', {})

    twitch_rtmp_url = f'rtmp://live.twitch.tv/app/{twitch_key}' if twitch_key else None
    youtube_rtmp_url = f'rtmp://a.rtmp.youtube.com/live2/{youtube_key}' if youtube_key else None

    input_stream = ffmpeg.input('rtmp://<your-rtmp-server>/<your-stream-key>')

    outputs = []
    if twitch_rtmp_url:
        outputs.append(
            ffmpeg.output(
                input_stream,
                twitch_rtmp_url,
                c:v='copy',
                c:a='aac',
                f='flv',
                metadata={'title': twitch_metadata.get('title'), 'game': twitch_metadata.get('game')}
            )
        )

    if youtube_rtmp_url:
        outputs.append(
            ffmpeg.output(
                input_stream,
                youtube_rtmp_url,
                c:v='copy',
                c:a='aac',
                f='flv',
                metadata={'title': youtube_metadata.get('title'), 'category': youtube_metadata.get('category')}
            )
        )

    processes = [ffmpeg.run_async(output) for output in outputs]
    stream_processes[stream_id] = processes

    return jsonify({'message': f'stream {stream_id} started'})


if __name__ == '__main__':
    app.run(debug=True)
