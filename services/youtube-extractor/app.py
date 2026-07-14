import re
from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

app = Flask(__name__)

def extract_video_id(url: str) -> str:
    """Extracts the YouTube video ID from various forms of YouTube URLs."""
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    return None

@app.route('/transcript', methods=['GET'])
def get_transcript():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    video_id = extract_video_id(url)
    if not video_id:
        return jsonify({"error": "Invalid YouTube URL"}), 400

    try:
        # Instantiate the API object
        ytt_api = YouTubeTranscriptApi()
        
        # Fetch the transcript
        fetched_transcript = ytt_api.fetch(video_id)
        
        # Combine all text segments into one long string using snippet.text
        full_text = " ".join([snippet.text for snippet in fetched_transcript])
        
        return jsonify({
            "success": True,
            "video_id": video_id,
            "text": full_text
        })
        
    except TranscriptsDisabled:
        return jsonify({"error": "Transcripts are disabled for this video."}), 400
    except NoTranscriptFound:
        return jsonify({"error": "No transcript found for this video."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run on port 5000 inside the container
    app.run(host='0.0.0.0', port=5000)
