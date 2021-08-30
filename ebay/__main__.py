from pathlib import Path

import pandas as pd

from .scrape import get_listings, listings_to_df
from .notify import email, text

LISTINGS_CSV = Path(Path(__file__).parent.parent, 'data', 'csv',
'listings.csv')
URL = r"https://www.ebay.com/sch/i.html?_dcat=261186&_fsrp=1&_from=R40&_armrs=1&_sacat=0&_nkw=andrzej+sapkowski+set&_sop=10"

def main():
    try: # try loading witcher.csv
        df_old = pd.read_csv(LISTINGS_CSV)
        df = listings_to_df(get_listings(URL))
        # check for rows in df not in df
        diff = set(df['Date Added']) - set(df_old['Date Added'])
        # if any new rows, email with data
        if diff:
            df_new = df[df['Date Added'].isin(diff)]
            msg = ""
            for idx, row in df_new.iterrows():
                msg += "{}\n{}\n{}\n".format(row.Title, row.Price, row.Link)
            email(msg)
            text(msg)
    except OSError: # file doesn't exist
        df = listings_to_df(get_listings(URL))
    finally:
        df.to_csv(LISTINGS_CSV, index=False)

if __name__ == '__main__':
    main()
