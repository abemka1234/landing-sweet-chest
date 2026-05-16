import flask, os
import pandas
from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_mail import Mail, Message
from jinja2 import Environment, FileSystemLoader, select_autoescape

load_dotenv()
email_my = os.getenv("EMAIL")
email_password_my = os.getenv("PASSWORD")

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465  
app.config['MAIL_USE_SSL'] = True  
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USERNAME'] = email_my
app.config['MAIL_PASSWORD'] = email_password_my
app.config['MAIL_DEFAULT_SENDER'] = email_my
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

mail = Mail(app)

cards_product = pandas.read_excel('cards.xlsx', sheet_name='Cards').to_dict("records")
instas_product = pandas.read_excel('cards.xlsx', sheet_name='Insta').to_dict("records")

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('index.html')
rendered_page = template.render(cards=cards_product, instas=instas_product)

with open('templates/index1.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

@app.route("/", methods=["GET", "POST"])
def Send_email():
    if request.method == "POST":
        username = request.form["username"]
        phone = request.form["phone"]
        discription = request.form["discription"]

        try:
            msg = Message("Новый заказ", sender=email_my, recipients=[email_my])
            msg.body = f"Имя клиента: {username} \nТелефонный номер: {phone} \nОписание заказа: {discription}"
            mail.send(msg)
            print("Email отправлен успешно!")
        except Exception as e:
            print(f"Ошибка при отправке: {e}")
        
        return render_template("index1.html")
    
    return render_template("index1.html")

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)