from discord_webhook import DiscordWebhook, DiscordEmbed
import requests
import json
import random
import csv
import pandas as pd
from datetime import timedelta, datetime

def main():
    
    print('[' + datetime.now().strftime("%H:%M:%S.%f") + '] Monitoring...')

    # Grab a random proxy from proxies.txt
    proxy = random.choice(open('proxies.txt').readlines())

    ip,port,proxy_username,proxy_password = proxy.split(':')
    
    # Enter proxy here ip:port or user:pass:ip:port
    
    proxies = {
        'http': 'http://'+proxy_username+':'+proxy_password+'@'+ip+':'+port+'/',
        'https': 'http://'+proxy_username+':'+proxy_password+'@'+ip+':'+port+'/',
        'ftp' : 'http://'+proxy_username+':'+proxy_password+'@'+ip+':'+port+'/'
        }
    
    headers = {
        'authority': 'api.capitoltrades.com',
        'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
        'sec-ch-ua-platform': '"Windows"',
        'origin': 'https://app.capitoltrades.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://app.capitoltrades.com/',
        'accept-language': 'en-CA,en-US;q=0.9,en;q=0.8',
    }

    data = '{"pageNumber":"1","pageSize":"50","ticker":false,"congressType":"Both","politicianParty":"Both"}'
    
    
    resp = requests.post('https://api.capitoltrades.com/trades', headers=headers, proxies=proxies, data=data).json()
    

    # Check if resp is already in data.txt
    for i in range(0,40,1): 
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


while True:
    try:
        main()
    except Exception as e: 
        print(e)
        main()







