
from bs4 import BeautifulSoup
import json
import email
import imaplib
import configparser
import threading
from binance import Client # to interact with binance we will use the library python-binance v1.0.16   https://python-binance.readthedocs.io/en/latest/

# Connect a file for reading data, passwords and keys for connecting to accounts
config = configparser.ConfigParser()
config.read("./venv/config.ini")

# set the parameters of the keys as an ordinary variable
api_key = config['Config']['api']
api_secret = config['Config']['secret']
# log in to Binance and create a Binance session
client = Client(api_key, api_secret)

#  function returns the coin value of our symbol for example "DREPUSDT"
def price(symbol):
    price = client.get_avg_price(symbol=symbol)['price']
    return float(price)

# the function sells all available coins of a certain symbol in our case "DREP"
def sell_coin():
    balance = client.get_asset_balance(asset='DREP') # ask binance for information about the balance of the coin
    all_coin_balanse = balance['free']  #  select the amount of free coins from our balance, "free" are those we can work with and are not scheduled in other orders(see the documentation " get_asset_balance" https://python-binance.readthedocs.io/en/latest/binance.html?highlight=client.get_asset_balance#binance.client.Client.get_asset_balance)
    order = client.order_market_sell(  # we create an order at the market price
        symbol='DREPUSDT',  # the currency pair on which you want to create an order
        quantity=all_coin_balanse)  # the number of coins we want to sell, in our case we selected all the coins of this pair
    return 0

# the function buys coins for the entire balance of the wallet
def buy_coin():   # функція для покупки понеток, купуємо на всі гроші які у нас є
    balance_usdt = client.get_asset_balance(asset='USDT')
    all_coin_balanse_usdt = float(balance_usdt['free']) # get the amount of USDT contained in our cart
    a = price('DREPUSDT') # here we lose the price(symbol) function described above and get the price of DREP vs. USDT
    coin_byers = all_coin_balanse_usdt // a #  by a simple formula we calculate how many coins we can buy
    order = client.order_market_buy( # we create a purchase order
        symbol='DREPUSDT',
        quantity=coin_byers)
    return 0


# a function that implements receiving information and reading the message that we received from the Tradingview website
def get_messege():

    config = configparser.ConfigParser()
    config.read("./venv/config.ini")

    # assign values to internal variables
    user_name = config['Config']['username']
    pass_word = config['Config']['password']

    mail = imaplib.IMAP4_SSL('imap.ukr.net') # establish a connection with the server that will process our requests
    mail.login(user_name, pass_word)
    mail.list()
    mail.select("inbox")
    typ, data = mail.search(None, 'ALL')
    #print(data)
    ids = data[0]  # We receive a number of emails

    id_list = ids.split()  # divide by ID
    i1 = id_list[::-1]
    i = i1[0] #select the last message
    typ, data = mail.fetch(i, "(RFC822)")

    messege = email.message_from_bytes(data[0][1]) # read its contents
    #print(messege)
    # select messages only from TradingView we decode the contents of the letter and select the information we need
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


dTime = "None"
def logic():   #  the logic of our bot, according to which and when we will buy/sell on the market
    messege_mail = get_messege()
    global dTime
    if messege_mail['dTime'] != dTime:  # we filter the new message from the old one so that the system does not take the previous message again
        dTime = messege_mail['dTime']
        balance_main = client.get_asset_balance(asset='DREP')
        all_coin_balanse_main = balance_main['free'] # see if we have coins
        if messege_mail['do_it'] == 'sell ':  # we read what is done on the market, people sell (sell)
            if all_coin_balanse_main == 0:  # if there are no coins - we buy them
                count = True
                buy_coin()
                price_order_duy = price("DREPUSDT") # fix the price at which we bought it
        elif messege_mail['do_it'] == 'buy ':  # if people buy we will sell
            if all_coin_balanse_main != 0:
                sell_coin()
                count = False
    if count == True:  #   this block of code will sell coins if their price changes by 1 percent in any direction, I decided so based on my risk management
        proc = price_order_duy/100
        prise_real_time = price("DREPUSDT")
        delta = abs(prise_real_time - price_order_duy)
        delta_proch = delta/proc
        if delta_proch >= 1:
            sell_coin()



def runner():   #   needed to restart the functions, we restart the script for reactivation
  threading.Timer(60.0, runner).start()  # Restart after 60 seconds
  logic()


if __name__ == '__main__':
    runner()
