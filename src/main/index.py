

def get_index_html():
    return """
    <html>
        <head>
            <title>Stream to YouTube and Twitch</title>
        </head>
        <body>
            <h1>Stream to YouTube and Twitch</h1>
            <p>Use the form below to stream to YouTube and Twitch.</p>
            <form action="/stream" method="POST" enctype="multipart/form-data">
                <input type="file" name="file" />
                <input type="submit" value="Stream" />
            </form>
        </body>
    </html>
    """
