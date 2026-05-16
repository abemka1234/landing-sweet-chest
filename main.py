import os
import pandas
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Загружаем переменные окружения
load_dotenv()

# Получаем данные из .env
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM")  # Например: onboarding@resend.dev или ваш подтвержденный email
EMAIL_TO = os.getenv("EMAIL_TO")      # Ваш email для получения заказов

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Читаем данные из Excel
cards_product = pandas.read_excel('cards.xlsx', sheet_name='Cards').to_dict("records")
instas_product = pandas.read_excel('cards.xlsx', sheet_name='Insta').to_dict("records")

# Генерируем HTML страницу
env = Environment(
    loader=FileSystemLoader('templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('index.html')
rendered_page = template.render(cards=cards_product, instas=instas_product)

with open('templates/index1.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

def send_email_resend(username, phone, discription):
    """
    Отправка email через Resend API
    """
    # Формируем содержимое письма
    email_content = f"Имя клиента: {username}\nТелефонный номер: {phone}\nОписание заказа: {discription}"
    
    try:
        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "from": EMAIL_FROM,
                "to": [EMAIL_TO],
                "subject": "🔔 Новый заказ с сайта",
                "text": email_content
            }
        )
        
        if response.status_code == 200:
            print(f"✅ Email успешно отправлен через Resend!")
            print(f"📧 Ответ: {response.json()}")
            return True
        else:
            print(f"❌ Ошибка отправки: {response.status_code}")
            print(f"📝 Детали: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Исключение при отправке: {e}")
        return False

@app.route("/", methods=["GET", "POST"])
def Send_email():
    if request.method == "POST":
        username = request.form["username"]
        phone = request.form["phone"]
        discription = request.form["discription"]
        
        # Отправляем email
        send_email_resend(username, phone, discription)
        
        return render_template("index1.html")
    
    return render_template("index1.html")

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)