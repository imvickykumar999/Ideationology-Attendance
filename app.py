
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():

    from Clouix.Firebase import pageview as pv
    up = pv.run()

    from Clouix.Spreadsheets import dance
    Name = dance.fetch()
    print('=========> ', Name)

    return render_template('index.html',
                            g=up[0],
                            url=up[1],
                            added=False,
                            Name=Name,
                            )


@app.route("/attendance", methods=['POST', 'GET'])
def attendance():

    from Clouix.Firebase import pageview as pv
    up = pv.run()

    from Clouix.Spreadsheets import dance
    Name = dance.fetch()
    appn=[]

    for i in Name:
        text = request.form.get(i)
        appn.append(text)

    appn = ['A' if v is None else 'P' for v in appn]
    attend = dance.mark(appn)
    print(appn)
    return render_template('index.html',
                            g=up[0],
                            url=up[1],
                            added=True,
                            Name=Name,
                            )


@app.route('/bot')
def bot():
    return render_template('bot.html',
                            url=False,
                            )


@app.route("/vicks_bot", methods=['POST', 'GET'])
def vicks_bot():
    from flask import request as req

    text = req.form['text']
    if text == '':
        text = '''
    Hello from a Python script!
    - Vicks.
    '''

    url = req.form['url']
    if url == '':
        url = 'https://chat.googleapis.com/v1/spaces/AAAAJd5Znh4/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=y-_1xKKSD0v9jTCgtKrMiY9ATRiKu5rF7yV_obrPKbo%3D'

    imageUrl = req.form['imageUrl']
    openLink = req.form['openLink']

    if imageUrl != '' or openLink != '':
        bot_message = {
            'text' : text + '\nMessage sent from https://vixtest.herokuapp.com/bot',
            "cards": [
             {
              "sections": [
                {
                  "widgets": [
                    {
                      "image": {
                        "imageUrl": imageUrl,
                        "onClick": {
                          "openLink": {
                            "url": openLink
                          }
                        }
                      }
                    }
                  ]
                }
              ]
            }
          ]
        }
    else:
        bot_message = {
            'text' : text
        }

    from Clouix.Hangouts import hangouts
    hangouts.chatting(url, text, bot_message)
    return render_template('bot.html',
                            url=url,
                            )


@app.route('/youtube')
def youtube():
    import requests
    from Clouix.YouTube import ytube

    vid = request.args.get('q')
    if vid == None:
        vid = 'CSulY72GiX4'

    # vid = ytube.yts(q=vid)
    # vid = vid['items'][0]['id']['videoId']

    data = ytube.tvl(vid)
    try:
        com = ytube.com(vid)
    except Exception as e:
        com = {'error' : ['Comment is Disabled.']}

    print(com)
    return render_template('youtube.html',
                            vid=vid,
                            data=data,
                            com=com,
                           )


@app.route("/ytube", methods=['POST', 'GET'])
def ytube():
    try:
        import requests
        from Clouix.YouTube import ytube

        vid = request.form['q']
        if vid == None:
            vid = 'CSulY72GiX4'

        vid = ytube.yts(q=vid)
        vid = vid['items'][0]['id']['videoId']

        data = ytube.tvl(vid)
        try:
            com = ytube.com(vid)
        except Exception as e:
            com = {'error' : ['Comment is Disabled.']}

        print(com)
        return render_template('youtube.html',
                                vid=vid,
                                data=data,
                                com=com,
                               )
    except Exception as e:
        return ( render_template('404.html', e=e), 404 )


@app.route('/form')
def form():
    return render_template('form.html')


@app.errorhandler(404)
def page_not_found(e):
    e = 'Page not Found'
    return ( render_template('404.html', e=e), 404 )


if __name__ == '__main__':
    app.run(debug=True)
