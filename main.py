#Flask mail web for personal use and developmental use and other things

from flask import Flask, render_template, request , url_for,redirect
from flask_mail import Mail , Message
import time

app = Flask(__name__,template_folder = "templates")
app.secret_key = "abdul_sobur"

#setting up the config email .........-
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "h26015762@gmail.com"
app.config["MAIL_PASSWORD"] = "gune jqfg ftip xpgi"

#initialize the mail 
mail = Mail(app)

#creating my route 
@app.route("/" , methods = ["GET" , "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("sender_name","").replace('\n','').replace("\r",'')
        recipient = request.form.get("recipient")
        File = request.files.get("email-file")
        subject = request.form.get("subject","").replace('\n','').replace("\r",'')
        body = request.form.get("body")

        #Getting user input from textarea recipient
        user_input = request.form.get("recipient" , "")

        #Getting the uploaded txt file
        File = request.files.get("email-file")
        emails = []

        #recorrecting and checking user gmail that is input
        if user_input:
            new_textarea = user_input.replace("," , "\n").replace(" " , "\n")
            emails +=[email.strip() for email in new_textarea.split("\n") if email.strip()]

        #now checking the uploaded file 
        if File and File.filename.endswith(".txt"):
            file_contents = File.read().decode("utf-8-sig")
            file_emails = [line.strip() for line in file_contents.splitlines() if line.strip()]
            emails += file_emails

        #now remove duplicate email 
        emails = list(set(emails))
        valid_emails = [email for email in emails if '@' in email and '.' in email]

        #looping through to send emails
        with mail.connect() as conn:
          for email in valid_emails:
              user_msg = Message(
                  subject = subject,
                  sender = (name,app.config["MAIL_USERNAME"]),
                  recipients = [email],
                  body = body
              )
              mail.send(user_msg)
              time.sleep(3)

        return render_template("index.html", success = f"{len(valid_emails)} emails sent successfully!!!")


    return render_template("index.html")    




if __name__ == "__main__":
    app.run(debug=True)
    time.sleep(2)