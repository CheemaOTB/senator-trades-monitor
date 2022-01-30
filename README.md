
# Senator Trades Monitor

This monitor will grab the most recent trades by senators and send them as a webhook to discord. 


## Installation

To use the monitor, install the requirements, run:

```cmd
pip install -r requirements.txt
```
    
## Usage/Examples



```python
# For recent trades from any senator run:
recentTransactions.py

# For trades from specific senators run:
senatorTransactions.py

```


## FAQ

#### Where do I get senator ids?

Find the senator you want on https://app.capitoltrades.com/politician, click on the senator you want, and the senator id will be the numbers on the end of the link, so for https://app.capitoltrades.com/politician/726, the id is 726

#### Do I need proxies?

No, you can run the monitor without proxies (edit the files accordingly).


## Screenshots

![Webhook Screenshot](https://i.imgur.com/DDKO1dM.png)


## Acknowledgements

 - [API](https://www.capitoltrades.com/)

## Authors

- [@CheemaOTB](https://github.com/CheemaOTB)

