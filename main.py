import flask,os
import pandas
from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_mail import Mail, Message
from jinja2 import Environment, FileSystemLoader


#Загружаем из файла .evn наш email адрес
load_dotenv()
email_my = os.getenv("EMAIL")
email_password_my = os.getenv("PASSWORD")

app = Flask(__name__, template_folder='static/page') # Создание экземпляра приложения

# Конфигурация (например, для Gmail)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = email_my
app.config['MAIL_PASSWORD'] = email_password_my

mail = Mail(app)

env = Environment(loader=FileSystemLoader('static/page'))
template = env.get_template('index.html')

excel_data_df = pandas.read_excel('cards.xlsx', sheet_name='Cards')#Считываем файл cards.xlsx
CardName = excel_data_df['CardName'].tolist()
CardIngredients = excel_data_df['CardIngredients'].tolist()
CardImage = excel_data_df['CardImagePath'].tolist()

excel_data_df = pandas.read_excel('cards.xlsx', sheet_name='Insta')#Считываем файл cards.xlsx
InstaImage = excel_data_df['InstaImagePath'].tolist()

rendered = template.render(
    Name = CardName[0],
    Name1 = CardName[1],
    Name2 = CardName[2],
    Name3 = CardName[3],
    Name4 = CardName[4],
    Name5 = CardName[5],
    Name6 = CardName[6],
    Name7 = CardName[7],
    Name8 = CardName[8],
    Ingredients = CardIngredients[0],
    Ingredients1 = CardIngredients[1],
    Ingredients2 = CardIngredients[2],
    Ingredients3 = CardIngredients[3],
    Ingredients4 = CardIngredients[4],
    Ingredients5 = CardIngredients[5],
    Ingredients6 = CardIngredients[6],
    Ingredients7 = CardIngredients[7],
    Ingredients8 = CardIngredients[8],
    Image = CardImage[0],
    Image1 = CardImage[1],
    Image2 = CardImage[2],
    Image3 = CardImage[3],
    Image4 = CardImage[4],
    Image5 = CardImage[5],
    Image6 = CardImage[6],
    Image7 = CardImage[7],
    Image8 = CardImage[8],
    ImageInsta = InstaImage[0],
    ImageInsta1 = InstaImage[1],
    ImageInsta2 = InstaImage[2],
    ImageInsta3 = InstaImage[3],
    ImageInsta4 = InstaImage[4],
    ImageInsta5 = InstaImage[5],
    ImageInsta6 = InstaImage[6],
    ImageInsta7 = InstaImage[7],
    ImageInsta8 = InstaImage[8],
)
with open('static/page/index1.html', 'w', encoding='utf-8') as f:
    f.write(rendered)


#@app.route("/", methods=["GET","POST"]) <- Если хотите вернуться к полю заполнения то  
def Send_email():
    if request.method == "POST":
        username = request.form["username"]
        phone = request.form["phone"]
        discription = request.form["discription"]

        msg = Message("Новый заказ", sender = email_my, recipients = [email_my])
        msg.body = f"Имя клиента: {username} \nТелефонный номер: {phone} \nОписание заказа: {discription}"
        mail.send(msg)
        return "Заказ отправлен."
    return render_template("index2.html")

@app.route("/")#вам нужно закоментировать это и изменить экземпляр приложения
def Creating_cards():
    return render_template("index1.html")

if __name__ == '__main__':
    app.run(debug=True) # Запуск в режиме отладки