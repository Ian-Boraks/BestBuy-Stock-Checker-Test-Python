# Desinged by Ian Boraks
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH
# THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import requests
import sys
import random
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed
import re
import time

cookies_dict_list = [
    { # Littelton
        'locStoreId' : '210',
        # 'analyticsStoreId' : '210',
        'locDestZip' : '80123'
    },
    { # Southglenn
        'locStoreId' : '1171',
        # 'analyticsStoreId' : '1171',
        'locDestZip' : '80122'
    },
    { # S.E. Denver
        'locStoreId' : '164',
        # 'analyticsStoreId' : '164',
        'locDestZip' : '80124'
    },
    { # Colorado Blvd
        'locStoreId' : '211',
        # 'analyticsStoreId' : '211',
        'locDestZip' : '80222'
    },
]


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'
}

ping = '<@&839272703051563048>'

def proxieSetUp():
    global proxy_dict_list
    proxy_dict_list = []

    try:
        with open(".\meta\proxies.txt") as f:
            d = {}
            for line in f:
                d['http'] = line.strip()
                proxy_dict_list.append(dict(d))
    except Exception:
        print("Using backup proxies . . .\nCheck .\meta\proxies.txt for problems in formating . . .\nAnKiT is dAd nOw . . .")
        proxy_dict_list = [ # Backup Proxies
            {'http' : ''},
            
        ]
def startUpMessage(classNames):
    itemPost = ''
    for i in range(len(classNames)):
        itemPost = itemPost + '[' + classNames[i].name.group(0) + '](' + classNames[i].url + ')\n > SKU for product: ' + classNames[i].sku +'\n\n'

    webhook = DiscordWebhook(url = webhookURL)
    embed = DiscordEmbed(title = 'STARTING UP . . .', description = 'Currently monitoring:\n' + itemPost, color='bd1904')
    webhook.add_embed(embed)
    embed.set_image(url = 'https://media1.tenor.com/images/528bb500b7d0cba55047ef0122e7f093/tenor.gif?itemid=14298094')
    response = webhook.execute()

    # webhook = DiscordWebhook(url=webhookURL, content=ping) #PING ON START
    # response = webhook.execute()

class BestBuy:
    def __init__(self, url):
        i = random.randint(0, len(proxy_dict_list) - 1)
        j = random.randint(0, len(cookies_dict_list) - 1)
        self.url = url
        self.inStockOutStock = True

        connected = False
        while connected == False:
            try:
                self.page = requests.get(self.url, headers = headers, proxies = proxy_dict_list[i], cookies = cookies_dict_list[j])
                connected = True
            except Exception as e:
                print('Proxy Dumb: ', proxy_dict_list.pop(i))
                print(e)
                i = random.randint(0, len(proxy_dict_list) - 1)
                j = random.randint(0, len(cookies_dict_list) - 1)

        self.soup = BeautifulSoup(self.page.content, 'html.parser')
        self.stock = self.soup.find_all("div", {"class": "fulfillment-add-to-cart-button"})

        self.img = self.soup.find_all("img", {"class": "primary-image"})
        self.img = re.search('(https://pisces).*(.jpg)', str(self.img[0]))

        self.sku = self.url.split('site/')[1][:-2]

        self.name = self.soup.find_all("div", {"class": "sku-title"})
        self.name = re.search('(?<=r"\>)(.*)(?=</h1></div>)', str(self.name[0]))

        print('Setup for ' + self.name.group(0) + ' is done . . .')

    def checkStock(self):
        i = random.randint(0, len(proxy_dict_list) - 1)
        j = random.randint(0, len(cookies_dict_list) - 1)

        connected = False
        while connected == False:
            try:
                self.page = requests.get(self.url, headers = headers, proxies = proxy_dict_list[i], cookies = cookies_dict_list[j])
                connected = True
            except Exception as e:
                print('Proxy Dumb: ', proxy_dict_list.pop(i))
                print(e)
                i = random.randint(0, len(proxy_dict_list) - 1)
                j = random.randint(0, len(cookies_dict_list) - 1)

        self.soup = BeautifulSoup(self.page.content, 'html.parser')
        self.stock = self.soup.find_all("div", {"class": "fulfillment-add-to-cart-button"})

    def notInStock(self):
        webhook = DiscordWebhook(url = webhookURL)
        embed = DiscordEmbed(title = self.name.group(0), description = '[LINK TO PAGE](https://www.bestbuy.com/site/'+self.sku+'.p)', color='bd1904')
        embed.add_embed_field(name='SOLD OUT or UNAVAILABLE', value = 'SKU: ' + self.sku)
        webhook.add_embed(embed)
        embed.set_image(url = self.img.group(0))
        response = webhook.execute()

    def runStock(self):
        self.checkStock()
        try:
            inStock = re.search("Add to", str(self.stock[0]))
        except IndexError:
            print(self.stock)
            inStock = False
        if not inStock: # SOLD OUT
            if not self.inStockOutStock:
                self.notInStock()
            if oosPing: self.notInStock()
            self.inStockOutStock = True
            pass
        elif inStock and self.inStockOutStock: # IN STOCK
            print(self.name.group(0) + ":    IN STOCK!!!!!!!!!!!!")
            webhook = DiscordWebhook(url = webhookURL)
            embed = DiscordEmbed(title = self.name.group(0), description = '[LINK TO PAGE]('+self.url+')', color='14de57')
            embed.add_embed_field(name='IN STOCK', value = 'SKU: ' + self.sku)
            webhook.add_embed(embed)
            embed.set_image(url = self.img.group(0))
            response = webhook.execute()
            webhook = DiscordWebhook(url=webhookURL, content = ping + ' ' + self.name.group(0))
            response = webhook.execute()
            self.inStockOutStock = False

def main(itemsBB, webhook):
    try:
        global webhookURL
        webhookURL = webhook
        classNames = []

        proxieSetUp()

        for i in itemsBB:
            regex = re.compile('[^a-zA-Z]')
            className = regex.sub('', i)
            className = BestBuy(i)
            classNames.append(className)

        print("STARTING . . .")
        if not silent: startUpMessage(classNames)
        if restartPing:
            webhook = DiscordWebhook(url=webhookURL, content = "Running again . . . ")
            response = webhook.execute()

        while True:
            for i in classNames:
                i.runStock()
    except KeyboardInterrupt:
        print("Closing . . .")
        webhook = DiscordWebhook(url=webhookURL, content = "Shutting down . . .")
        response = webhook.execute()
        exit()

if __name__ == "__main__":
    global a; global b; global c; global silent; global oosPing
    a = ''
    b = ''
    c = ''
    silent = False
    oosPing = False
    restartPing = False

    try:
        a = sys.argv[1].lower()
        if a == '-s':
            print("Silent Start")
            silent = True
        elif a == '-oos':
            print('OOS Ping')
            oosPing = True
        elif a == '-r':
            print('Restart Ping')
            restartPing = True
        b = sys.argv[2].lower()
        if b == '-s':
            print("Silent Start")
            silent = True
        elif b == '-oos':
            print('OOS Ping')
            oosPing = True
        elif b == '-r':
            print('Restart Ping')
            restartPing = True
        c = sys.argv[3].lower()
        if c == '-s':
            print("Silent Start")
            silent = True
        elif c == '-oos':
            print('OOS Ping')
            oosPing = True
        elif c == '-r':
            print('Restart Ping')
            restartPing = True
    except IndexError:
        pass

    items = []
    importData = []
    with open(".\meta\data.bb") as f:
        for i in f:
            importData.append(i.replace('\n', ''))

    SKUs = importData[0].split(",")
    for i in SKUs:
        items.append('https://www.bestbuy.com/site/'+i+'.p')

    webhook = importData[1]

    print("SETTING UP . . .")
    main(items, webhook)
