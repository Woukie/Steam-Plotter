from requests_html import HTMLSession
import re
import matplotlib.pyplot as plt
import datetime
import calendar
from bs4 import BeautifulSoup
import base64

user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/76.0.3809.87 Safari/537.36"
)

cookie = 'locale=en_US;'

headers = {
    'User-Agent': user_agent,
    'Accept-Language': 'en-US,en;q=0.5',
    'cookie': cookie,
}

while True:
    session = HTMLSession()
    session.headers.update(headers)

    url = input("Enter item url: ")
    resp = session.get(url)

    print(resp)

    resp.html.render()

    htmlLines = resp.html.html.split('\n')

    numLines = len(htmlLines)

    rawDates = [];
    rawPrices = [];
    rawQuantities = [];
    dates = rawDates

    if url.startswith("https://steamcommunity.com/market/listings") :
        print("Steam detected")
        print("Resolution (empty for raw):")
        inputResolution = input()

        if inputResolution != "":
            resolution = int(inputResolution)
            
            dates = [0] * resolution
            prices = [0] * resolution
            #quantities = [0] * resolution

            numEntries = len(rawDates)

            lowestDate = rawDates[0]
            highestDate = rawDates[numEntries - 1]

            for i in range(numEntries - 1):
                equivelantCoord = resolution * (rawDates[i] - lowestDate) / (highestDate - lowestDate)
                #quantities[int(equivelantCoord)] += rawPrices[i]

            for i in range(resolution):
                entry = int(i * numEntries / resolution)
                dates[i] = (i / resolution) * (highestDate - lowestDate) + lowestDate
                prices[i] = rawPrices[entry]
        else:
            dates = rawDates
            prices = rawPrices
            #quantities = rawQuantiti
        
        for i in range(numLines):
            line = htmlLines[numLines - i - 1]
            
            if line.__contains__('var line1='): 
                arrayData = line.split('var line1=')[1]
                
                splitData = list(filter(str.strip, re.split('\[|\]|,|"|;', arrayData)))
                
                for i in range(len(splitData)):
                    if(i%3==0):
                        dateData = re.split("\s|:", splitData[i])
                        rawDates.append(datetime.datetime(int(dateData[2]), int(list(calendar.month_abbr).index(dateData[0])), int(dateData[1]), int(dateData[3])))
                    if(i%3==1): rawPrices.append(float(splitData[i]))
                    if(i%3==2): rawQuantities.append(int(splitData[i]))
        
    elif url.startswith("https://backpack.tf") :
        print("TF2 detected")
        
        for i in range(numLines):
            line = htmlLines[i]
            
            print(line)
            
            if line.__contains__('<span class="alt-price-text">'): 
                print(htmlLines[numLines - i])
    else :
        print("Unknown input")
        quit()

    fig, host = plt.subplots(figsize=(8,5))

    par1 = host.twinx()

    host.set_xlabel("Date")
    host.set_ylabel("Price")
    #par1.set_ylabel("Quantity")

    color1 = plt.cm.viridis(0.2)
    color2 = plt.cm.viridis(0.1)

    p1, = host.plot(dates, prices,    color=color1, label="Price")
    #p2, = par1.plot(dates, quantities,    color=color2, label="Quantity")

    lns = [p1]
    host.legend(handles=lns, loc='best')

    host.yaxis.label.set_color(p1.get_color())
    #par1.yaxis.label.set_color(p2.get_color())

    # Adjust spacings w.r.t. figsize
    fig.tight_layout()
    # Alternatively: bbox_inches='tight' within the plt.savefig function 
    #                (overwrites figsize)

    # Best for professional typesetting, e.g. LaTeX
    #plt.savefig("pyplot_multiple_y-axis.pdf")
    # For raster graphics use the dpi argument. E.g. '[...].png", dpi=200)'

    #plt.plot(dates, prices)
    #plt.plot(dates, quantities)
    plt.show()