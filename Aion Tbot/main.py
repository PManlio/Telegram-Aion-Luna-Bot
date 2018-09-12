from telegram.ext import Updater
import logging
import time
from PIL import Image, ImageGrab, ImageChops

updater = Updater(token='Insert your token here')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

#################### Main routine method ####################
####in the bbox you have to put your (minX, minY, maxX, maxY) pixel in wich Ranks are shown (50x50 px)
####those pixel are good if your resolution is 1920x1080px
def routine():
    screen = ImageGrab.grab(bbox=(941.5, 475, 977.5, 509))
    screen.save('screen.jpg', "JPEG")
#################### Main routine method ####################

def equal(im1, im2):
  return ImageChops.difference(im1, im2).getbbox() is None

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm AionBot, here to serve you. Type /help to know what can you ask me.")

def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Type /start to begin me;\n"
                                                          "Type /bm to know how much AP gives 1 blood medal;\n"
                                                          "Type /luna to receive a message when your luna dungeon ends (so you can go afk);")

def bm(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="1 blood mark = 363 AP \n"
                                                          "230 blood marks = 83490 AP")


def luna(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm starting watching your screen. When Luna result will appair, i will poke you.")
    imgB = Image.open('rankB.jpg')
    imgS = Image.open('rankS.jpg')

    ####### this variable a is put here just to let your bot do something
    ####### the reason is that if your bot do nothing for too much time
    ####### it just will stop working; it's like a control or smth like that
    a = 0
    while a <= 900:
        routine()
        screenshot = Image.open('screen.jpg')
        b = equal(imgB, screenshot)
        s = equal(imgS, screenshot)
        if b==1:
            bot.send_message(chat_id=update.message.chat_id, text="Luna dungeon ended (rank B).\n"
                                                                  "Come back and get your rewards.")
            a = a + 1800
        elif s==1:
            bot.send_message(chat_id=update.message.chat_id, text="Luna dungeon ended (rank S).\n"
                                                                  "Come back and get your rewards.")
            a = a + 1800
        else:
            #bot.send_message(chat_id=update.message.chat_id, text="Still nothing.")
            time.sleep(10)
        a = a + 1
        print(a)


#import command handler
from telegram.ext import CommandHandler



####################### This method allows the bot to read your caps-lock instruction #######################
def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)

caps_handler = CommandHandler('caps', caps, pass_args=True)
dispatcher.add_handler(caps_handler)
####################### This method allows the bot to read your caps-lock instruction #######################


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

bm_handler = CommandHandler('bm', bm)
dispatcher.add_handler(bm_handler)

luna_handler = CommandHandler('luna', luna)
dispatcher.add_handler(luna_handler)

updater.start_polling(poll_interval = 1.1, timeout = 1900)