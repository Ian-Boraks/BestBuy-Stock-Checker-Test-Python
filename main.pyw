# Desinged by Ian Boraks
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH
# THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import BestBuy
import PySimpleGUI as sg
import re
import os

webhookURL = ''
itemsBB = []
default_SKU = '6429434,6429440,6429442,6439402,6428324,6426149,6430161'

def startMain():
    data = open(".\meta\data", 'w')

    SKUs = values["SKU"]
    SKUs = SKUs.replace(" ", "")
    data.write(SKUs + '\n')
    SKUs = SKUs.split(",")

    webhookURL = values["WEB"]
    data.write(webhookURL)

    for i in SKUs:
        itemsBB.append('https://www.bestbuy.com/site/'+i+'.p')

    window.close()
    data.close()
    BestBuy.proxieSetUp()
    BestBuy.main(itemsBB, webhookURL)

layout = [[sg.Text(text="Enter the SKUs you want to monitor", size=(40, 1)), sg.Text(text="Webhook", size=(40, 1))], [sg.Input(default_text=default_SKU, size=(40, 1), key="SKU"), sg.Input(default_text="Webhook URL", size=(40, 1), key="WEB")], [sg.Button(button_text="Start", key="START")]]

window = sg.Window('Window Title', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == "START":
        print("Started")
        startMain()

window.close()
