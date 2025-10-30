from flask import Flask, render_template, request, send_file
import yt_dlp as youtube_dl
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url'].strip()
        print(f"URL received: {url}")

        try:
            # Create downloads folder if it doesn't exist
            os.makedirs("downloads", exist_ok=True)

            # yt-dlp options to keep original title
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',  # <-- keeps original video title
                'noplaylist': True
            }

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            print(f"Downloaded file: {filename}")
            return send_file(filename, as_attachment=True)

        except Exception as e:
            print(f"Download failed: {e}")
            return f"Error: {str(e)}"

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
