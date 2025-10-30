from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url', '').strip()
        print(f"URL received: {url}")

        if not url:
            return "⚠️ Please enter a valid YouTube URL."

        # Generate unique file name
        unique_filename = f"{uuid.uuid4()}.mp4"
        output_path = os.path.join(DOWNLOAD_DIR, unique_filename)

        try:
            # yt-dlp options for public videos only
            ydl_opts = {
                'format': 'best',
                'outtmpl': output_path,
                'noplaylist': True,
                'quiet': True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            print(f"✅ Download complete: {output_path}")
            return send_file(output_path, as_attachment=True)

        except Exception as e:
            error_text = str(e)
            print(f"Download failed: {error_text}")

            # Handle restricted or unavailable videos gracefully
            if "Sign in to confirm" in error_text or "Private video" in error_text:
                return "❌ This video is restricted, private, or age-limited. Only public videos can be downloaded."
            elif "unavailable" in error_text.lower():
                return "⚠️ This video is unavailable or removed."
            else:
                return f"⚠️ Unexpected error: {error_text}"

    return render_template('index.html')


if __name__ == '__main__':
    # For local testing
    app.run(host='0.0.0.0', port=5000, debug=True)
