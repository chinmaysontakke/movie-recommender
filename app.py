from flask import Flask, request, jsonify, send_from_directory
from recommend import get_recommendations

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('frontend', path)

@app.route('/recommend', methods=['GET'])
def recommend():
    title = request.args.get('title')
    if not title:
        return jsonify({'error': 'No title provided'}), 400
    try:
        recs = get_recommendations(title)
        return jsonify({'recommendations': recs})
    except KeyError:
        return jsonify({'error': 'Movie not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
