# app.py
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from dotenv import load_dotenv
import ssl

if os.environ.get('FLASK_ENV') != 'production':
    load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')

secret_key = os.environ.get('FLASK_SECRET_KEY')

app.config['SECRET_KEY'] = secret_key
app.config['WTF_CSRF_ENABLED'] = True  

SMTP_SERVER = os.environ.get('SMTP_SERVER')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
SMTP_USER = os.environ.get('SMTP_USER')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD')
MAIL_FROM = os.environ.get('MAIL_FROM')
MAIL_TO = os.environ.get('MAIL_TO')


# お問い合わせフォームの定義
class ContactForm(FlaskForm):
    company_name = StringField('貴社名')
    name = StringField('お名前', validators=[DataRequired(message='お名前を入力してください')])
    email = StringField('ご連絡先メールアドレス', validators=[
        DataRequired(message='メールアドレスを入力してください'), 
        Email(message='有効なメールアドレスを入力してください')
    ])
    phone = StringField('ご連絡先電話番号')
    category = SelectField('ご相談カテゴリ', choices=[
        ('補助金関連', '補助金関連'),
        ('M&A', 'M&A'),
        ('事業再生', '事業再生'),
        ('その他', 'その他')
    ])
    details = TextAreaField('ご相談内容', validators=[DataRequired(message='ご相談内容を入力してください')])
    submit = SubmitField('送信')


@app.route('/', methods=['GET', 'POST'])
def home():
    form = ContactForm()
    if form.validate_on_submit():
        # フォームデータの取得
        company_name = form.company_name.data
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        category = form.category.data
        details = form.details.data

        # メール本文作成
        mail_body = f'''
        お問い合わせがありました。
        
        貴社名: {company_name}
        お名前: {name}
        メールアドレス: {email}
        電話番号: {phone}
        カテゴリ: {category}
        ご相談内容:
        {details}
        '''
        msg = MIMEText(mail_body, 'plain', 'utf-8')
        msg['Subject'] = Header('ウェブサイトからのお問い合わせ', 'utf-8')
        msg['From'] = MAIL_FROM
        msg['To'] = MAIL_TO
        msg['Reply-To'] = email
        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.set_debuglevel(1)
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(MAIL_FROM, MAIL_TO, msg.as_string())
            server.quit()

            flash('お問い合わせありがとうございます。送信が完了しました。', 'success')
            return redirect('https://mipo.co.jp/')
        except Exception as e:
            print(e)
            flash('送信中にエラーが発生しました。しばらくしてから再度お試しください。', 'danger')
            return redirect('https://mipo.co.jp/')
    
    """ホームページを表示する関数"""
    return render_template('index.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)