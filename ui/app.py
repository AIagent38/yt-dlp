from flask import Flask, request, render_template
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    download_path = os.path.join(os.path.expanduser('~'), 'downloads', '%(title)s.%(ext)s')
    ydl_opts = {
        'outtmpl': download_path,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            # The extract_info call with download=False gets the metadata
            # The actual download happens with process_video_result or by calling extract_info with download=True
            # For simplicity and to ensure we are processing what we got, let's use process_video_result
            # This might mean ydl.download([url]) is another option, but process_video_result gives more control if needed.
            # However, the typical usage is to call ydl.download([url]) or ydl.extract_info(url, download=True)
            # Let's stick to the plan of using process_video_result for now as per the prompt.
            # Correction: extract_info with download=True is the more direct way to download.
            # process_video_result is more for internal use or advanced scenarios.
            # Let's simplify and use extract_info with download=True.

            # Re-evaluating: The prompt asks for extract_info(url, download=False) then process_video_result(info_dict, download=True)
            # This is a valid, though less common, way. It allows inspecting metadata before committing to download.
            # Let's stick to the prompt's specific instructions.
            ydl.process_video_result(info_dict, download=True)
            title = info_dict.get('title', 'Unknown title')
            return render_template('index.html', message=f"Download successful: {title}")
    except Exception as e:
        return render_template('index.html', message=f"Error downloading video: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
