# Desinged by Ian Boraks
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH
# THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

#https://api.bestbuy.com/v1/stores(area(80127,250mi))+products(sku%20in(6451330))?format=json&show=products.name,name,storeId,postalCode&pageSize=10&page=1&apiKey=

import requests
import sys
import random
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed
import re
import time
import json

def importData():
    global apiKey; global webhook
    apiKey = webhook = ''

    importData = []
    with open(".\meta\data.bb") as f:
        for i in f:
            importData.append(i.replace('\n', ''))

    webhook = importData[1]

    with open('.\meta\\api.key') as f:
        for i in f:
            apiKey = i.replace('\n', '')

def getGPUData():
    global gpuJson

    print('Gathering GPU data . . .')
    gpuDataURL = 'https://api.bestbuy.com/v1/products(categoryPath.id=abcat0507002&(name=RTX%203060*%20|%20name=RTX%203070*%20|%20name=RTX%203080*|%20name=RTX%203090*)&name!=NVLINK*)?show=name,regularPrice,sku,url,addToCartUrl,image&format=json&pageSize=100&page=1&apiKey=' + apiKey
    gpuDataPage = requests.get(gpuDataURL); gpuJson = json.loads(str(BeautifulSoup(gpuDataPage.content, features='html.parser')))

    time.sleep(1)

    print('Gathering STORE data . . .')
    storeDataURL = 'https://api.bestbuy.com/v1/stores(area(80127,250))?format=json&show=name,storeId,postalCode&pageSize=100&page=1&apiKey=' + apiKey
    storeDataPage = requests.get(storeDataURL); storeJson = json.loads(str(BeautifulSoup(storeDataPage.content, features='html.parser')))

    if ('errorCode' in storeJson):
        print('Collecting of storeJson data ended with an error code')
        temp = input('Waiting for user input . . .\n')
    elif ('errorCode' in gpuJson):
        print('Collecting of gpuJson data ended with an error code')
        temp = input('Waiting for user input . . .\n')

    with open(".\meta\GPU_data.json", 'w') as f:
        f.write(json.dumps(gpuJson, indent=4))

    with open(".\meta\Store_data.json", 'w') as f:
        f.write(json.dumps(storeJson, indent=4))

class BestBuy:
    def __init__(self, prodIndex):
        self.name = gpuJson['products'][prodIndex]['name']
        self.sku = gpuJson['products'][prodIndex]['sku']
        self.url = gpuJson['products'][prodIndex]['url']
        self.addToCartUrl = gpuJson['products'][prodIndex]['addToCartUrl']
        self.image = gpuJson['products'][prodIndex]['image']
        self.regularPrice = gpuJson['products'][prodIndex]['regularPrice']

def classifyGPUData():
    global classList
    classList = []
    for prodIndex in range(len(gpuJson['products'])):
        className = gpuJson['products'][prodIndex]['name'] = BestBuy(prodIndex)
        classList.append(className)

def startUp():
    importData()
    getGPUData()
    classifyGPUData()

def checkStock():
    print(classList[3].regularPrice)

def main():
    startUp()
    checkStock()

if __name__ == "__main__":
    main()


# item = apiResponse
#
# webhook = DiscordWebhook(url = 'https://discord.com/api/webhooks/841315455854706729/j8bhB9MzrxJpKbQbsya44hW0hPjD0-VNl2DT2yEGLieN-RSV3fZPrs4BJL41qJ6RChBO')
# embed = DiscordEmbed(title = item['name'], description = '[LINK TO PAGE](' + item['url'] + ')', color='bd1904')
# embed.add_embed_field(name='SOLD OUT or UNAVAILABLE', value = 'SKU: ' + str(item['sku']))
# webhook.add_embed(embed)
# embed.set_image(url = item['image'])
# response = webhook.execute()
