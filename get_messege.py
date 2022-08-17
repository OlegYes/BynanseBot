import imaplib
import base64
import os, re
import email
import pprint
import configparser
import bs4
from bs4 import BeautifulSoup
import json



def get_messege():
    # Считываем учетные данные
    config = configparser.ConfigParser()
    config.read("./venv/config.ini")

    # Присваиваем значения внутренним переменным
    user_name = config['Telegram']['username']
    pass_word = config['Telegram']['password']

    mail = imaplib.IMAP4_SSL('imap.ukr.net')
    mail.login(user_name, pass_word)
    mail.list()
    mail.select("inbox")
    typ, data = mail.search(None, 'ALL')
    #print(data)
    ids = data[0]  # Получаем сроку номеров писем

    id_list = ids.split()  # Разделяем ID писем
    i1 = id_list[::-1]
    i = i1[0]
    #print(i)
    typ, data = mail.fetch(i, "(RFC822)")
    #print(data[0][1])
    messege = email.message_from_bytes(data[0][1])
    #print(messege)

    if messege.get("From") == "TradingView <noreply@tradingview.com>":
        raw_email = data[0][1]
        #print(raw_email)
        raw_email_string = raw_email.decode('utf-8')
        #print(raw_email_string)
        email_message = email.message_from_string(raw_email_string)
        # print(email_message)
        if email_message.is_multipart():
            for payload in email_message.get_payload():
                # print(payload)
                body = payload.get_payload(decode=True).decode('utf-8')
                #print(body)
        else:
            body = email_message.get_payload(decode=True).decode('utf-8')
            #print(body)

            soup = BeautifulSoup(body, 'lxml')
            #soups = soup.find_all("td", valign="top", align="left", style="text-align: left; padding: 0px 0px;")
            soups = soup.find("p", style="font-family: -apple-system, BlinkMacSystemFont, 'Trebuchet MS', Roboto, Ubuntu, sans-serif;font-size: 18px;line-height: 28px;margin: 0;padding: 0;text-align: center !important;white-space: pre-line;color: #131722;")
            #print(soups.text)

            with open("test.json", "w", encoding='utf-8') as w:
                w.write(soups.text)
            with open("test.json", "r") as read_file:
                dataInfo = json.load(read_file)
            return dataInfo



dTime = "2022-08-11T09:39:00Z"
def logic():   #  логіка нашого бота, за яких умов і коли ми будемо здійснювати покупку/продажу на ринку
    messege_mail = get_messege()
    global dTime
    if messege_mail['dTime'] != dTime:  # так ми відсіюємо нове повідомлення від старого щоб система не брала повторно попередне повідомлення
        dTime = messege_mail['dTime']
        print(dTime)

if __name__ == '__main__':
    #get_messege()
    a = get_messege()
    logic()
    print(dTime)