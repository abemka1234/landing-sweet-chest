import flask,os
import pandas
from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_mail import Mail, Message
from jinja2 import Environment, FileSystemLoader, select_autoescape


#Загружаем из файла .evn наш email адрес
load_dotenv()
email_my = os.getenv("EMAIL")
email_password_my = os.getenv("PASSWORD")

app = Flask(__name__) # Создание экземпляра приложения

# Конфигурация (например, для Gmail)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = email_my
app.config['MAIL_PASSWORD'] = email_password_my

mail = Mail(app)

cards_product = pandas.read_excel('cards.xlsx', sheet_name='Cards').to_dict("records")#Считываем файл cards.xlsx

instas_product = pandas.read_excel('cards.xlsx', sheet_name='Insta').to_dict("records")#Считываем файл cards.xlsx

env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('index.html')

rendered_page = template.render(cards=cards_product,instas=instas_product)

with open('templates/index1.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

@app.route("/", methods=["GET","POST"])
def Send_email():
    if request.method == "POST":
        username = request.form["username"]
        phone = request.form["phone"]
        discription = request.form["discription"]

        msg = Message("Новый заказ", sender = email_my, recipients = [email_my])
        msg.body = f"Имя клиента: {username} \nТелефонный номер: {phone} \nОписание заказа: {discription}"
        mail.send(msg)
        return render_template("index1.html")
    return render_template("index1.html")

if __name__ == '__main__':
    app.run(debug=True) # Запуск в режиме отладки