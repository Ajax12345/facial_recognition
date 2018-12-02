import json, flask, random, string
import collections

app = flask.Flask(__name__)
app.secret_key = ''.join(random.choice(string.printable) for _ in range(20))



@app.route('/', methods=['GET'])
def home():
    flask.session['seen_films'] = json.dumps([])
    return flask.render_template('main_rec_page.html')


@app.route('/recommend_movie')
def recommend_movie():
    vals = json.loads(flask.request.args.get('vals'))
    with open('movie_data.json') as f:
        all_movies = json.load(f)
    
    #print([i for i in vals if any(c not in i for c in all_movies)])
    _category, _ = max([[i, sum(c.get(i, 0) for c in vals)/float(len(vals))] for i in all_movies], key=lambda x:x[-1])
    _film = random.choice(all_movies[_category])
    while _film['title'] in json.loads(flask.session['seen_films']) and (lambda x:_film['title'] not in [a for a,b in x.items() if b == min(x.values())])(collections.Counter(json.loads(flask.session['seen_films']))):
        _film = random.choice(all_movies['_category'])
    
    flask.session['seen_films'] = json.dumps(json.loads(flask.session['seen_films'])+[_film])
    print('final film', _film)
    return flask.jsonify({"success":"True", **_film})
if __name__ == '__main__':
    app.debug = True
    app.run()