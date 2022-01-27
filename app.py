
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
    import pageview as pv
    up = pv.run()

    import insta as i
    l = i.followers()
    print(l)

    vid = request.args.get('vid')
    if vid == None:
        vid = 'KZehm-meGMg'

    return render_template('index.html', vid=vid, scroll='form',
                            g=up[0], url=up[1], followers=l[0]
                            )

@app.errorhandler(404)
def page_not_found(e):
    return ( render_template('404.html'), 404 )

if __name__ == '__main__':
    app.run(debug=True)
