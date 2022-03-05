
from flask import Flask, render_template, request, url_for, redirect, flash, \
session, abort

from flask_sqlalchemy import sqlalchemy, SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Change dbname here
db_name = "auth.db"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{db}'.format(db=db_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# SECRET_KEY required for session, flash and Flask Sqlalchemy to work
app.config['SECRET_KEY'] = 'configure strong secret key here'

db = SQLAlchemy(app)
# db.create_all()

class User(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    bio = db.Column(db.String(500), nullable=True)
    dp_url = db.Column(db.String(600), nullable=True)
    pass_hash = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '' % self.username


@app.route('/')
def index():

    from Clouix.Firebase import pageview as pv
    up = pv.run()

    from Clouix.Spreadsheets import dance
    Name = dance.fetch()
    print('=========> ', Name)

    from Clouix.Spreadsheets import grapha
    plotted = grapha.plotme(Name[1])

    return render_template('index.html',
                            g=up[0],
                            url=up[1],
                            added=False,
                            Name=Name[0],
                            plotted=plotted,
                            )


@app.route("/attendance", methods=['POST', 'GET'])
def attendance():

    otp = request.form['otp'].strip()
    f=open("otp.txt",'r')
    f = f.read()
    geto = f[:4]
    person = f[4:].split('@')[0]

    f = open("otp.txt", "w")
    f.write('-')
    f.close()

    if otp == geto and otp != '-':
        from Clouix.Firebase import pageview as pv
        up = pv.run()

        from Clouix.Spreadsheets import dance
        Name = dance.fetch()
        appn=[]

        for i in Name[0]:
            text = request.form.get(i)
            appn.append(text)

        appn = ['A' if v is None else 'P' for v in appn]
        attend = dance.mark(appn)
        print(appn)

        from Clouix.Spreadsheets import grapha
        Name = dance.fetch()
        plotted = grapha.plotme(Name[1])

        return render_template('index.html',
                                g=up[0],
                                url=up[1],
                                added=True,
                                Name=Name[0],
                                plotted=plotted,
                                )
    else:
        return render_template("404.html", e = 'Wrong OTP')


@app.route('/tweet')
def tweet():
    try:
        from Clouix.TwitterAPI import tweet_cast as tc
        aid = tc.funaid()
        return render_template('tweet.html', aid=aid)
        
    except Exception as e:
            return ( render_template('404.html', e=e), 404 )

@app.route('/bot')
def bot():
    return render_template('bot.html',
                            url=False,
                            )


@app.route("/vicks_bot", methods=['POST', 'GET'])
def vicks_bot():
    try:
        from flask import request as req

        text = req.form['text']
        if text == '':
            text = '''
        Hello from a Python script!
        - Vicks.
        '''

        url = req.form['url']
        # if url == '':
        #     url = 'https://chat.googleapis.com/v1/spaces/AAAAJd5Znh4/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=y-_1xKKSD0v9jTCgtKrMiY9ATRiKu5rF7yV_obrPKbo%3D'

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
    except Exception as e:
        return ( render_template('404.html', e=e), 404 )


@app.route('/youtube')
def youtube():
    import requests
    from Clouix.YouTube import ytube

    vid = request.args.get('q')
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


# https://myaccount.google.com/u/3/lesssecureapps?pli=1&rapt=AEjHL4MpjjYh8Z-01vJ5GRsQXICYQsXHG0PweSjWenlbAJfes6qNKbHKs_CfCVh0d5qUO58qFeeB0sYCbA3GANLf-965469dVA

@app.route("/vicksmail")
def vicksmail():
    return render_template("mailsent.html", sent='no')

@app.route("/mail_sent", methods=['POST'])
def mail_sent():
    from Clouix.OTPmail import verify
    verify.getotp()
    return render_template("mailsent.html", sent='yes')

@app.route('/form')
def form():
    return render_template('form.html')


@app.errorhandler(404)
def page_not_found(e):
    e = 'Page not Found'
    return ( render_template('404.html', e=e), 404 )


# ===============================================

def create_db():
    """ # Execute this first time to create new db in current directory. """
    db.create_all()

# @app.route("/", methods=["GET", "POST"])
@app.route("/signup/", methods=["GET", "POST"])
def signup():
    """
    Implements signup functionality. Allows username and password for new user.
    Hashes password with salt using werkzeug.security.
    Stores username and hashed password inside database.

    Username should to be unique else raises sqlalchemy.exc.IntegrityError.
    """

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        dp_url = request.form['dp_url'].strip()

        bio = request.form['bio']
        # print('=====>>> ', type(bio))
        if bio is None:
            bio = 'hey...'
            
        if not (username and password):
            flash("Username or Password cannot be empty")
            return redirect(url_for('signup'))
        else:
            username = username.strip()
            password = password.strip()

        # Returns salted pwd hash in format : method$salt$hashedvalue
        hashed_pwd = generate_password_hash(password, 'sha256')
        # print(hashed_pwd)
        
        new_user = User(username=username, bio=bio, pass_hash=hashed_pwd, dp_url=dp_url)
        db.session.add(new_user)

        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            flash("Username {u} is not available.".format(u=username))
            return redirect(url_for('signup'))

        flash("User account has been created.")
        return redirect(url_for("login"))

    return render_template("signup.html")


# @app.route("/", methods=["GET", "POST"])
@app.route("/login/", methods=["GET", "POST"])
def login():
    """
    Provides login functionality by rendering login form on get request.
    On post checks password hash from db for given input username and password.
    If hash matches redirects authorized user to home page else redirect to
    login page with error message.
    """

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if not (username and password):
            flash("Username or Password cannot be empty.")
            return redirect(url_for('login'))
        else:
            username = username.strip()
            password = password.strip()

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.pass_hash, password):
            session[username] = True
            return redirect(url_for("user_home", username=username))
        else:
            flash("Invalid username or password.")

    return render_template("login_form.html")


@app.route("/user/<username>")
def user_home(username):
    """
    Home page for validated users.

    """
    if not session.get(username):
        abort(401)

    from Clouix.Firebase import flower as fire
    obj = fire.Bank_Account(username)
    user = User.query.filter_by(username=username).first()

    return render_template("user_home.html",
                            username=username,
                            bio=user.bio,
                            dp_url=user.dp_url,
                            disp = obj.display(),
                            )


@app.route("/profile/<username>")
def profile(username):
    user = User.query.filter_by(username=username).first()
    return render_template("profile.html",
                            username=username,
                            bio=user.bio,
                            dp_url=user.dp_url,
                            )


@app.route("/account/<username>", methods=["GET", "POST"])
def user_account(username):
    """
    Home page for validated users.

    """
    if not session.get(username):
        abort(401)

    money = float(request.form['money'])
    from Clouix.Firebase import flower as fire

    '''
    # flower as fire

    flower samjhi kya ?
    fire hai mai... XD

    (firebase chatting feature will be add soon...)
    '''

    obj = fire.Bank_Account(username)
    pay = request.form['pay']
    obj_pay = fire.Bank_Account(pay)

    if money>0:
        obj_pay.deposit(money)
        disp = obj.withdraw(money)

        flash(f'''
        Paid Successfully
        ''')

    else:
        disp = obj.display()
        flash("Amount should NOT be Negative number.")

    user = User.query.filter_by(username=username).first()
    return render_template("user_home.html", 
                            username=username,
                            bio=user.bio,
                            dp_url=user.dp_url,
                            disp = disp,
                            )


@app.route("/logout/<username>")
def logout(username):
    """ Logout user and redirect to login page with success message."""
    session.pop(username, None)
    flash("successfully logged out.")
    return redirect(url_for('login'))

# =================================================

if __name__ == '__main__':
    app.run(debug=True)
