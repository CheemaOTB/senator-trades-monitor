from discord_webhook import DiscordWebhook, DiscordEmbed
import requests
import json
import random
import csv
import pandas as pd
from datetime import timedelta, datetime


def main(senator):
    
    senatorNumber = str(senator)

    print('[' + datetime.now().strftime("%H:%M:%S.%f") + '] ['+senatorNumber+'] Monitoring...')

    # Grab a random proxy from proxies.txt
    proxy = random.choice(open('proxies.txt').readlines())

    ip,port,proxy_username,proxy_password = proxy.split(':')
    
    # Enter proxy here ip:port or user:pass:ip:port
    proxies = {
        'http': 'http://'+proxy_username+':'+proxy_password+'@'+ip+':'+port+'/',
        'https': 'http://'+proxy_username+':'+proxy_password+'@'+ip+':'+port+'/',
        'ftp' : 'http://'+proxy_username+':'+proxy_password+'@'+ip+':'+port+'/'
        }
    
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}

    
    
    resp = requests.get(f'https://api.capitoltrades.com/senators/trades/{senatorNumber}/false?pageSize=20&pageNumber=1', headers=headers, proxies=proxies).json()

    # Check if resp is already in data.txt
    for i in range(0,6,1): 
        with open('data.txt') as f:
            if str(resp[i]) in f.read():
                pass
            else:
                # Set Vars
                ticker = resp[i]["ticker"]
                publicationDate = resp[i]["filingDate"]
                politicianName = resp[i]["politicianName"]
                owner = resp[i]["owner"]
                transactionDate = resp[i]["transactionDate"]
                transactionType = resp[i]["shareType"]
                tradeType = resp[i]["tradeType"]
                sharesAmount = resp[i]["shares"]
                sharesRange = resp[i]["shareRange"]
                sharePrice = resp[i]["sharePrice"] 
                valueRange = resp[i]["tradeValueRange"]
                stockLink = f"https://finance.yahoo.com/quote/{resp[i]['ticker']}"
                senatorLink = f"https://app.capitoltrades.com/politician/{resp[i]['biographyId']}"
                
                # Check if vars are undefined
                if sharesAmount is None:
                    sharesAmount = "None"
                if sharesRange is None:
                    sharesRange = "None"
                if sharePrice is None:
                    sharePrice = "None"
                if valueRange is None:
                    valueRange = "None"
                
                    
                # Webhook
                webhookURL = ['webhook here']
                webhook = DiscordWebhook(url=webhookURL, rate_limit_retry=True,username="Capitol Trades")
                embed = DiscordEmbed(title='Ticker', description=(ticker), color=242424)
                embed.set_author(name='Senator Trades Monitor', url="https://twitter.com/CheemaOtb", icon_url='https://pbs.twimg.com/profile_images/1161809234725441537/P2Nz_JZ4_400x400.jpg')
                embed.set_footer(icon_url='https://pbs.twimg.com/profile_images/1161809234725441537/P2Nz_JZ4_400x400.jpg', text='Powered By CheemaOTB#8339')
                embed.set_timestamp()
                embed.add_embed_field(name='Publication Date', value=(publicationDate))
                embed.add_embed_field(name='Name', value=(politicianName))
                embed.add_embed_field(name='Owner', value=(owner))
                embed.add_embed_field(name='Transaction Date', value=(str(transactionDate)))
                embed.add_embed_field(name='Transaction Type', value=(str(transactionType)))
                embed.add_embed_field(name='Trade Type', value=(str(tradeType)))
                embed.add_embed_field(name='Shares', value=(str(sharesAmount)))
                embed.add_embed_field(name='Shares Range', value=(str(sharesRange)))
                embed.add_embed_field(name='Price', value=(str(sharePrice)))
                embed.add_embed_field(name='Value Range', value=(str(valueRange)))
                embed.add_embed_field(name='Stock', value=(str(stockLink)))
                embed.add_embed_field(name='Senator Info', value=(str(senatorLink)))
                webhook.add_embed(embed)
                response = webhook.execute() #pylint:disable=unused-variable;
                
                # Write resp to csv
                with open('data.txt', "a") as file:
                    file.write(str(resp[i]))


# Senators - You can change which sentators you want to follow here - add or remove senator ids
senators = [624,491,64,589,581,309,640,426]
while True:
    try:
        for x in senators:
            main(x)
    except Exception as e: 
        print(e)
        main(x)