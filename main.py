import telebot
from telebot import types
from geopy.geocoders import Nominatim #Подключаем библиотеку

token = '*'
bot = telebot.TeleBot(token)
global lon, lat

def coordintes_by_name(naming):
    geolocator = Nominatim(user_agent="Tester")
    adress = naming
    location = geolocator.geocode(adress)  # Создаем переменную, которая состоит из нужного нам адреса
    return [location.latitude, location.longitude]  # GPS-координаты нужного нам адреса


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

    itembtn1 = types.KeyboardButton('/about')
    itembtn2 = types.KeyboardButton('/road')

    markup.add(itembtn1, itembtn2)

    bot.send_message(message.chat.id, "Здравствуйте, "
                     + message.from_user.first_name
                     + ", я помогу Вам построить маршрут, для этого нажмите /road",
                     reply_markup=markup)


@bot.message_handler(commands=['about'])
def send_about(message):
    bot.send_message(message.chat.id, "Что умеет этот бот? " + "Бот может построить маршрут по заданным Вами условиям, рассказать про достопримечательности и проложить идеальный маршрут для туриста.")


@bot.message_handler(commands=['road'])
def geo(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Нажми на кнопку отправить местоположение, чтобы передать мне свое местоположение", reply_markup=keyboard)


@bot.message_handler(content_types=['location'])
def location(message):
    global lon, lat
    bot.send_message(message.chat.id, "Куда хотите придти?")
    if message.location is not None:
        print(message.location)
        print("latitude: %s; longitude: %s" % (message.location.latitude, message.location.longitude))
        lon = message.location.latitude
        lat = message.location.longitude
    else:
        print("bO")


@bot.message_handler(content_types='text')
def message_reply(message):
    global lon, lat
    adress = message.text
    if len(adress) != 0:
        print(lon, lat)
        coor = coordintes_by_name(adress)
        print(coor)
        ssilka = "https://yandex.ru/maps/?ll="+str(lon)+"%2C"+str(lat)+"&mode=routes&rtext="+str(coor[0])+"%2C"+str(coor[1])+"&rtt=pd&ruri=ymapsbm1%3A%2F%2Forg%3Foid%3D1196007194~ymapsbm1%3A%2F%2Forg%3Foid%3D1802533628&z=5.36"
        bot.send_message(message.chat.id, "" + ssilka)

bot.infinity_polling()
bot.polling()
