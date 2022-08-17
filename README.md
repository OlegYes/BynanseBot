# BynanseBot

ENG.
This project connects Tradingview, Binance and email that can support imap.
this project is just an example of how you can solve the problem of automation of trading on Binanse, I do not recommend recklessly copying the code and hoping that your trade will be fully automated, you need to approach everything wisely and taking into account all the factors that can affect the productivity of your work.

Аll code is accompanied by comments, so you can easily navigate the understanding of each command.

Let's move on to the description of the project
In this project I use the following libraries:
 - python-binance v1.0.16 for interaction with Binanse
 - imaplib — IMAP4 protocol client
 - Beautiful Soup to find the original text from our message.

For the period itself, I set up the strategy on tradingview so that I received indicators of chart changes and received two indicators from the super trend strategy, I also described the output in json format and I can enter useful information on the chart there to receive it by e-mail.
when receiving the message i used the Imap protocol to get the content of the message and extract the json text i need from the whole message i ran into several problems
1. The message must be deciphered so that it can be read normally.
2. tradingview sends messages in the form of an Html letter, so I had to parse it using the Beautiful Soup library.
After receiving the information from the message, I analyze it and then make a purchase/sale, the code is written for a specific situation on the market and for a specific currency pair, it is not difficult to replace it in the code and customize it for yourself.

Аll the code is in the main.py file.
Library dependencies are described in the requirements.txt file.

You can use the configparser library to hide your API keys and passwords like I did, or write them explicitly as a regular variable:
```python
# Connect a file for reading data, passwords and keys for connecting to accounts
config = configparser.ConfigParser()
config.read("./venv/config.ini")

 set the parameters of the keys as an ordinary variable
api_key = config['Config']['api']
api_secret = config['Config']['secret']
```

Or:
```python
api_key = '********'
api_secret = '********'
```
I would be glad to hear your suggestions or comments.

#

UA.

Цей проект зв'язує між собою Tradingview, Binance та електронну почту що може пыдтримувати imap. 
цей проект лише приклад як можна вирішити проблему автоматизаціі торгівлі на Binanse я не рекомендую безрозсудно копіювати код і сподіватись що у вас торгівля буде повністю автоматизована, до усього потрібно підходити з розумом та з урахуванням всіх чинників що можуть вплинути на продуктивність вашої роботи. 

Весь код супроводжується коментарями, тому ви можете легко орієнтуватися в розумінні кожної команди.

Перейдемо до опису проекту
У цьому проекті я використовую бібліотеки:
 - python-binance v1.0.16 для взаемодії з Binanse 
 - imaplib — IMAP4 protocol client
 - Beautiful Soup для пошуку потрідного тексту з нашого повідомлення.

На сам перід я налаштував стратегію на tradingview так що я отримував індикотори зміни графіку та отримував два індикатори зі стратегії супер тренд, також я описав повыдомлення в json форматі і можу туди вписати корисну інформацію по графіку щоб отримати її на електронну почту. 
при отриманні повідомлення я використав протокол Imap щоб дістати вміст повідомлення і витягти з усього повідомлення потрібний мені текст json, я зіткнувся з кількома проблемами 
1. Повідомлення доводиться дешифрувати щоб його можна було нормально прочитати.
2. tradingview присилає повідомлення у вигляді Html листа тому довелось його парсити з використанням бібліотеки Beautiful Soup. 
Після отримання інформації з повідомлення я аналізую її і далі здійснюю покупку/продаж, код написаний під конкретну ситуацію на ринку і під конкретну валютну пару її не складно замінити у коді та налаштувати під себе.

Весь код знаходиться в файлі main.py.
Залежності бібліотек описані у файлі requirements.txt.

Ви можете використовувати бібдіотеку configparser для приховання своїх ключів та паролів для API так як це зробив я, або прописати їх явно як звичайну змінну:
```python
# Connect a file for reading data, passwords and keys for connecting to accounts
config = configparser.ConfigParser()
config.read("./venv/config.ini")

 set the parameters of the keys as an ordinary variable
api_key = config['Config']['api']
api_secret = config['Config']['secret']
```

Або:
```python
api_key = '********'
api_secret = '********'
```

Буду радий почути ваші пропозиції або зауваження.
