
def getotp():
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    fromaddr = "sagar.sws2000@gmail.com"
    toaddr = "18erecs080.vicky@rietjaipur.ac.in"

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Vicks OTP"

    import random
    otp = str(random.randint(1000,9999))
    # otp = '7639'

    file1 = open("otp.txt", "w")
    file1.write(otp)
    file1.write(toaddr)
    file1.close()

    body = f'''\
        <html>
          <head>Vicks Quotes</head>
          <body>
            <h2 style="color:green;">
               Hi, <br> {''.join(toaddr.split('@')[0])}
            </h2>
            <br>
           <h1>
               Here is the OTP you wanted.
               <br><br> {otp}
           </h1>
          </body>
        </html>
    '''
    
    msg.attach(MIMEText(body, 'html'))
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, "Sagarsws2000@")

    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()
