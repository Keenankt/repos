import pandas as pd
import numpy as np
import random
import sklearn
from faker import Faker

fakedata = Faker()
## name, postcode, total_donations, number_donations 
## name
name = []
for i in range(1100):
    newname = fakedata.name()
    name.append(newname)
name = pd.DataFrame(name)

## post code
vic_postcodes = []
vic_postcodes = pd.read_csv('australian_postcodes.csv')
vic_postcodes = vic_postcodes[vic_postcodes["state"] == "VIC"]
vic_postcodes = vic_postcodes[vic_postcodes["postcode"] < 4000]
vic_postcodes = vic_postcodes[["postcode","locality"]]
vic_postcodes.dropna(inplace=True)

postcode_dict = vic_postcodes.set_index('locality')['postcode'].to_dict()

postcode_prices = []
postcode_prices = pd.read_csv("C:/Users/kkuli/repos/median_property.csv")
postcode_prices['suburb'] = postcode_prices['suburb'].map(postcode_dict)

price_dict = postcode_prices.set_index('suburb')['med_price'].to_dict()

print(postcode_prices['med_price'].describe())
##
postcode = []
for y in range(1100):
    newcode = random.choice(list(vic_postcodes['postcode']))
    postcode.append(newcode)

postcode = pd.DataFrame(postcode)
postcode['price'] = postcode.replace(to_replace=price_dict)
postcode.rename(columns={0:'postcode'},inplace=True)    

##merged names and postcodes
df = name.join(postcode)

##generate donations functions
def annual_donation_generator(price):
    if price <= 600000:
        annual_donations = random.randint(10,1000)
    elif price <= 850000:
        annual_donations = random.randint(10,5000)
    elif price <= 1125000:
        annual_donations = random.randint(10,20000)
    else:
        annual_donations = random.randint(10,50000)
    return annual_donations

def number_donation_generator(price):
    if price <= 1125000:
        num_donations = random.randint(1,12)
    else:
        split_donor_type = random.randint(1,2)
        if split_donor_type == 1:
            num_donations = random.randint(1,14)
        if split_donor_type == 2:
            num_donations = random.randint(10,30)
    return num_donations

#### generate donation behaviour

df['annual_donation'] = df['price'].apply(annual_donation_generator)
df['num_donation'] = df['price'].apply(number_donation_generator)

df.to_csv('donor_data.csv', index=False, encoding='utf-8')
