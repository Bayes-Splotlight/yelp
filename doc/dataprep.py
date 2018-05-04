import pandas as pd
import numpy as np
numpy.set_printoptions(threshold=numpy.nan)

# Extract business data of Las Vegas
baseDataDir= 'yelp-dataset/'
review = pd.read_csv(baseDataDir+'yelp_review.csv')
business = pd.read_csv(baseDataDir+'yelp_business.csv')
user = pd.read_csv(baseDataDir+'yelp_user.csv')
NY = business[business.city == 'New York']
vegas = business[business.city == 'Las Vegas']
business = vegas

business = business.groupby('state').filter(lambda r: len(r) > 20)
business.groupby('state').size()

# Drop users and businesses which have less than 500 reviews
user = user[user.review_count > 50]
business = business[business.review_count > 50]
business = business.groupby('state').filter(lambda r: len(r) > 20)

# Merger review, business and user
rev_biz_usr = pd.merge(pd.merge(review, business, on='business_id'), user, on='user_id')
col_drop = rev_biz_usr.columns.difference(['business_id', 'user_id', 'stars_x'])
rev_biz_usr.drop(col_drop, axis=1, inplace=True)

# Drop users and businesses with less than 20 reviews
for _ in range(8):
    rev_biz_usr = rev_biz_usr.groupby('business_id').filter(lambda r: len(r) >= 15)
    rev_biz_usr = rev_biz_usr.groupby('user_id').filter(lambda r: len(r) >= 15)
rev_biz_usr.stars_x = rev_biz_usr.stars_x.astype(int)
X = pd.pivot_table(rev_biz_usr, index='business_id', columns='user_id', values='stars_x')#, fill_value=0)
X.fillna(0, inplace=True)

(X != 0).sum(1)

X.to_csv('rating.csv')


# Text data
text = pd.merge(pd.merge(review, business, on='business_id'), user, on='user_id')
col_drop = text.columns.difference(['business_id', 'user_id', 'stars_x', 'text'])
text.drop(col_drop, axis=1, inplace=True)
for _ in range(8):
    text = text.groupby('business_id').filter(lambda r: len(r) >= 15)
    text = text.groupby('user_id').filter(lambda r: len(r) >= 15)
text.stars_x = rev_biz_usr.stars_x.astype(int)
text.to_csv('text.csv')

