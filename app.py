from flask import Flask, render_template, request, redirect, url_for
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

app = Flask(__name__)

# Configure Spotify client credentials
client_credentials_manager = SpotifyClientCredentials(client_id='d9aa157930ea49c581c114f749180751', client_secret='21df97b86dd04803a1b53bd86f6ec956')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['song']
        if query:
            return redirect(url_for('search', query=query))  # Changed 'result' to 'search'
    return render_template('index.html')

@app.route('/search')  # Changed '/result' to '/search'
def search():
    query = request.args.get('query')
    if not query:
        return redirect(url_for('index'))

    results = sp.search(q=query, limit=10)
    tracks = results['tracks']['items']
    track_info = []
    for track in tracks:
        album_cover_url = track['album']['images'][0]['url'] if track['album']['images'] else None
        track_info.append({'name': track['name'], 'artist': track['artists'][0]['name'], 'album_cover_url': album_cover_url})
    return render_template('result.html', query=query, track_info=track_info)

if __name__ == '__main__':
    app.run(debug=True)
