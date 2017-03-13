import mygmail
import pandas as pd
from lxml import html
from pandas import DataFrame, Series
from datetime import datetime
import sqlite3
from dateutil import parser
# from sqlalchemy import create_engine

entries = []
g = mygmail.login("teamgavtay@gmail.com", "teamgavtay123!")

inboxmail = g.inbox().mail(sender="dealalerts@slickdeals.net")

for mail in inboxmail:
    mail.fetch()
    tree = html.fromstring(mail.html)
    mail.archive()

    links = tree.xpath('//a')
    if links is None:
        continue
        
    titlelink = [link for link in links if link.get('style') is not None and '#0072bc' in link.get('style')][0]
    link = titlelink.xpath('./@href')[0]
    title = titlelink.xpath('.//span/text()')[0]
    
    price = tree.xpath('//*[@color="#60a430"]//span/text()')
    if len(price) == 0:
        price = "N/A"
    else:
        price = price[0]

    entries.append({
        "title": title,
        "price": price,
        "link": link,
        "detected_at": str(datetime.now()),
        "received_at": str(parser.parse(mail.headers['Date']))
    })
    
    
df = pd.DataFrame(entries)

db = 'sqlite:///database/slickdeals.db'
db = 'database/slickdeals.db'
conn = sqlite3.connect(db)
c = conn.cursor()

# Create table
c.execute("""CREATE TABLE IF NOT EXISTS email_deals(
   link text PRIMARY KEY,
   price text NOT NULL,
   title text NOT NULL,
   detected_at TEXT NOT NULL,
   received_at TEXT NOT NULL
   ) 
   WITHOUT ROWID;
""")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.

for idx in range(len(df)):
    try:
        df[idx:idx+1].to_sql("email_deals", conn, if_exists='append', index=False, chunksize=None, dtype=None)
    except:
        print("Duplicate deal. Continuing...")

conn.close()
