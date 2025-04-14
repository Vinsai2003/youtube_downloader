from flask import Flask, render_template, request, send_file
import yt_dlp as youtube_dl
import os
import uuid

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url'].strip()
        print(f"URL received: {url}")

        try:
            # Generate a unique filename
            unique_filename = f"{uuid.uuid4()}.mp4"
            output_path = os.path.join("downloads", unique_filename)

            # yt-dlp options
            ydl_opts = {
                'format': 'best',
                'outtmpl': output_path,
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            return send_file(output_path, as_attachment=True)

        except Exception as e:
            print(f"Download failed: {e}")
            return f"Error: {str(e)}"

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
