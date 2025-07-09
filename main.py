from flask import Flask, render_template, request, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email
from flask_mail import Mail, Message
import os
from flask.cli import load_dotenv

load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY')


# ------------Email Configuration (Gmail)--------------
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MY_EMAIL')
app.config['MAIL_PASSWORD'] = os.environ.get('MY_APP_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MY_EMAIL')

mail = Mail(app)

# -------------------------- Contact Form using FlaskForm ----------------------------
class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])


# ----------------------------Home Page with Contact Form----------------------------
@app.route('/', methods=['GET', 'POST'])
def home():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            # Send email to you
            msg = Message(
                subject=form.subject.data,
                sender=app.config['MAIL_DEFAULT_SENDER'],
                recipients=[os.environ.get('MY_EMAIL')],
                body=f"From: {form.name.data} <{form.email.data}>\n\n{form.message.data}"
            )
            msg.reply_to = form.email.data
            mail.send(msg)

            # Auto-reply to user
            auto_reply = Message(
                subject="Thanks for contacting me!",
                sender=app.config['MAIL_DEFAULT_SENDER'],
                recipients=[form.email.data],
                body=f"""
                    Hi {form.name.data},
                    
                    Thank you for reaching out! I've received your message and will get back to you as soon as I can.
                    
                    Best regards,  
                    Sabih Usmani  
                    Python Developer
                """
            )
            mail.send(auto_reply)

            flash('Your message has been sent successfully!', 'success')
        except Exception as e:
            print("Email sending failed:", e)
            flash('Failed to send message. Please try again later.', 'danger')
        return redirect(url_for('home'))

    return render_template('index.html', form=form)



if __name__ == '__main__':
    app.run(debug=True)
