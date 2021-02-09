#!/usr/bin/env python
# coding: utf-8

# In[1]:


# https://www.youtube.com/watch?v=eMOA1pPVUc4

# In[2]:

import os
import pandas as pd


# In[4]:


path = "C:\\Users\\prafulla.kamble\\Downloads\\0PRK\\ML\\Pandas-Data-Science-Tasks-master\\SalesAnalysis\\Sales_Data\\"


# In[5]:


files = [file for file in os.listdir(path)]
files


# In[6]:


all_months_data = pd.DataFrame()

for file in files:
    df = pd.read_csv(path+file)
    all_months_data = pd.concat([all_months_data, df])
    
all_months_data


# In[7]:


all_months_data.to_csv(path + "all_months_data.csv", index=False)


# In[8]:


all_data = pd.read_csv(path + "all_months_data.csv")
all_data.head()


# In[9]:


# https://youtu.be/eMOA1pPVUc4?t=683


# In[10]:


all_data['Month'] = all_data['Order Date'].str[0:2]
all_data.head()


# ## Cleaning data
# #### Removing NaN

# In[11]:


nan_df = all_data[all_data.isna().any(axis=1)]
nan_df


# In[12]:


all_data = all_data.dropna(how='all')
all_data


# In[13]:


## Convert column into integer type

all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = all_data['Month'].astype('int32')
all_data.head()


# ### ValueError: invalid literal for int() with base 10: 'Or'
# 
# ###### https://youtu.be/eMOA1pPVUc4?t=1426

# In[14]:


temp_df = all_data[all_data['Order Date'].str[0:2] == 'Or']
temp_df


# In[15]:


all_data = all_data[all_data['Order Date'].str[0:2] != 'Or']
all_data


# In[16]:


all_data['Month'] = all_data['Order Date'].str[0:2]
all_data['Month'] = all_data['Month'].astype('int32')
all_data.head()


# In[17]:


# Convert cells to int/ float datatype

all_data['Quantity Ordered'] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each'] = pd.to_numeric(all_data['Price Each'])

all_data.head()


# #### Add a sales column

# In[18]:


all_data['Sales'] =all_data['Quantity Ordered'] * all_data['Price Each']
all_data.head()


# ### What was the best sale of the month and how much was earned that month?

# In[19]:


results = all_data.groupby('Month').sum()
results


# In[20]:


import matplotlib.pyplot as plt
months = range(1,13)
plt.bar(months, results['Sales'])
plt.xticks(months)
plt.ylabel('Sales in USD ($)')
plt.xlabel('Month number')
plt.show()


# ### Best sale was in December

# In[21]:


all_data.head()


# ### Get city names

# In[22]:


# Split address on commas

# def get_city(address):
#     return address.split(',')[1]

def get_state(address):
    return address.split(',')[2].split(' ')[1]
    
all_data['City'] = all_data['Purchase Address'].apply(lambda x: x.split(',')[1] + ' ' + get_state(x))
all_data.head()


# ### City with highest number of sales

# In[23]:


results = all_data.groupby('City').sum()
results


# In[24]:


import matplotlib.pyplot as plt

# Bring cities in the same order as Sales

cities = [city for city, df in all_data.groupby('City')]

plt.bar(cities, results['Sales'])
plt.xticks(cities, rotation='vertical', size=8)

plt.ylabel('Sales in USD ($)')
plt.xlabel('City')

plt.show()


# In[ ]:





# In[25]:


# https://youtu.be/eMOA1pPVUc4?t=3127


# In[26]:


all_data['Order Date'] = pd.to_datetime(all_data['Order Date'])


# In[40]:


all_data['Order Date']


# In[27]:


type(all_data['Order Date'])


# In[28]:


all_data['Hour'] = all_data['Order Date'].dt.hour
all_data['Minute'] = all_data['Order Date'].dt.minute
all_data['Count'] = 1
all_data.head()


# #### Best time to show advertisements
# ##### ans: 11, 12, 13 and 18, 19, 29 hr 

# In[29]:


hours = [hour for hour, df in all_data.groupby('Hour')]
plt.plot(hours, all_data.groupby(['Hour']).count())
plt.xticks(hours)
plt.xlabel('Hour')
plt.ylabel('Number of Orders')
plt.grid()
plt.show()


# In[30]:


df = all_data[all_data['Order ID'].duplicated(keep=False)]
df.head()


# In[31]:


# Group all the products with the same product id

df['Grouped'] = df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
df = df[['Order ID', 'Grouped']].duplicates()
df.head(10)


# In[32]:


from itertools import combinations
from collections import Counter

count = Counter()

for row in df['Grouped']:
    row_list = row.split(', ')
    count.update(Counter(combinations(row_list, 2)))

# print(count)

# count.most_common(10)

for key, value in count.most_common(10):
    print(key, value)


# In[35]:


product_group = all_data.groupby('Product')
quantity_ordered = product_group.sum()['Quantity Ordered']


# In[36]:


products = [product for product, df in product_group]
plt.ylabel('Quantity ordered')
plt.xlabel('Product')
plt.bar(products, quantity_ordered)
plt.xticks(products, rotation='vertical', size=8)
plt.show()


# In[37]:


prices = all_data.groupby('Product').mean()['Price Each']
print(prices)


# In[54]:


fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(products, quantity_ordered, color='g')
ax2.plot(products, prices, 'b-')

ax1.set_xlabel('Product Name')
ax1.set_ylabel('Quantity Ordered', color ='g')

ax2.set_ylabel('Price ($)', color='b')
ax1.set_xticklabels(products, rotation='vertical', size=8)

plt.show()
