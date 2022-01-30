
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():

    from Clouix.Firebase import pageview as pv
    up = pv.run()

    return render_template('index.html',
                            g=up[0],
                            url=up[1],
                            )


@app.route('/youtube')
def youtube():
    import requests
    from Clouix.YouTube import ytube

    vid = request.args.get('q')
    if vid == None:
        vid = 'CSulY72GiX4'

    vid = ytube.yts(q=vid, maxResults=1)
    vid = vid['items'][0]['id']['videoId']

    data = ytube.tvl(vid)
    com = ytube.com(vid)

    return render_template('youtube.html',
                            vid=vid,
                            data=data,
                            com=com,
                           )

@app.route('/form')
def form():
    return render_template('form.html',
                            )

@app.errorhandler(404)
def page_not_found(e):
    return ( render_template('404.html'), 404 )

if __name__ == '__main__':
    app.run(debug=True)
