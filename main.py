import flask,os
from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_mail import Mail, Message
from flask_wtf import FlaskForm

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

@app.route("/home", methods=["GET","POST"])
@app.route("/", methods=["GET","POST"])
def home():
    if request.method == "POST":
        username = request.form["username"]
        phone = request.form["phone"]
        discription = request.form["discription"]

        msg = Message("Новый заказ", sender = email_my, recipients = [email_my])
        msg.body = f"Имя клиента: {username} Телефонный номер: {phone} Описание заказа: {discription}"
        mail.send(msg)
        return "Заказ отправлен."
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True) # Запуск в режиме отладки