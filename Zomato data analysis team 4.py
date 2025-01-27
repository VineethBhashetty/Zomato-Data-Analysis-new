#!/usr/bin/env python
# coding: utf-8

# # **Zomato Data Set Analysis and Visualization**
# 

# ![](http://mc.webpcache.epapr.in/discover.php?in=https://mcmscache.epapr.in/post_images/website_350/post_21404986/full.jpg)

# ## Importing Libraries

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('dark_background')


# ## Reading CSV

# In[2]:


df = pd.read_csv('../input/zomato-bangalore-restaurants/zomato.csv')
df.head()


# In[3]:


df.shape


# In[4]:


df.columns


# In[5]:


df = df.drop(['url', 'address', 'phone', 'menu_item', 'dish_liked', 'reviews_list'], axis = 1)
df.head()


# In[6]:


df.info()


# ## Dropping Duplicates

# In[7]:


df.drop_duplicates(inplace = True)
df.shape


# ## Cleaning Rate Column

# In[8]:


df['rate'].unique()


# ## Removing "NEW" ,  "-" and "/5" from Rate Column

# In[9]:


def handlerate(value):
    if(value=='NEW' or value=='-'):
        return np.nan
    else:
        value = str(value).split('/')
        value = value[0]
        return float(value)
    
df['rate'] = df['rate'].apply(handlerate)
df['rate'].head()


# ## Filling Null Values in Rate Column with Mean

# In[10]:


df['rate'].fillna(df['rate'].mean(), inplace = True)
df['rate'].isnull().sum()


# In[11]:


df.info()


# ## Dropping Null Values

# In[12]:


df.dropna(inplace = True)
df.head()


# In[13]:


df.rename(columns = {'approx_cost(for two people)':'Cost2plates', 'listed_in(type)':'Type'}, inplace = True)
df.head()


# In[14]:


df['location'].unique()


# In[15]:


df['listed_in(city)'].unique()


# ## Listed in(city) and location, both are there, lets keep only one.

# In[16]:


df = df.drop(['listed_in(city)'], axis = 1)


# In[17]:


df['Cost2plates'].unique()


# ## Removing , from Cost2Plates Column

# In[18]:


def handlecomma(value):
    value = str(value)
    if ',' in value:
        value = value.replace(',', '')
        return float(value)
    else:
        return float(value)
    
df['Cost2plates'] = df['Cost2plates'].apply(handlecomma)
df['Cost2plates'].unique()
        


# In[19]:


df.head()


# ## Cleaning Rest Type Column

# In[20]:


rest_types = df['rest_type'].value_counts(ascending  = False)
rest_types


# In[21]:


rest_types_lessthan1000 = rest_types[rest_types<1000]
rest_types_lessthan1000


# ## Making Rest Types less than 1000 in frequency as others

# In[22]:


def handle_rest_type(value):
    if(value in rest_types_lessthan1000):
        return 'others'
    else:
        return value
        
df['rest_type'] = df['rest_type'].apply(handle_rest_type)
df['rest_type'].value_counts()
        


# ## Cleaning Location Column

# In[23]:


location = df['location'].value_counts(ascending  = False)

location_lessthan300 = location[location<300]



def handle_location(value):
    if(value in location_lessthan300):
        return 'others'
    else:
        return value
        
df['location'] = df['location'].apply(handle_location)
df['location'].value_counts()


# ## Cleaning Cuisines Column

# In[24]:


cuisines = df['cuisines'].value_counts(ascending  = False)


cuisines_lessthan100 = cuisines[cuisines<100]



def handle_cuisines(value):
    if(value in cuisines_lessthan100):
        return 'others'
    else:
        return value
        
df['cuisines'] = df['cuisines'].apply(handle_cuisines)
df['cuisines'].value_counts()


# In[25]:


df.head()


# ## **Data is Clean, Lets jump to Visualization**

# ## Count Plot of Various Locations

# In[26]:


plt.figure(figsize = (16,10))
ax = sns.countplot(df['location'])
plt.xticks(rotation=90)


# ## Visualizing Online Order

# In[27]:


plt.figure(figsize = (6,6))
sns.countplot(df['online_order'], palette = 'inferno')


# ## Visualizing Book Table

# In[28]:


plt.figure(figsize = (6,6))
sns.countplot(df['book_table'], palette = 'rainbow')


# ## Visualizing Online Order vs Rate

# In[29]:


plt.figure(figsize = (6,6))
sns.boxplot(x = 'online_order', y = 'rate', data = df)


# ## Visualizing Book Table vs Rate

# In[30]:


plt.figure(figsize = (6,6))
sns.boxplot(x = 'book_table', y = 'rate', data = df)


# ## Visualizing Online Order Facility, Location Wise

# In[31]:


df1 = df.groupby(['location','online_order'])['name'].count()
df1.to_csv('location_online.csv')
df1 = pd.read_csv('location_online.csv')
df1 = pd.pivot_table(df1, values=None, index=['location'], columns=['online_order'], fill_value=0, aggfunc=np.sum)
df1


# In[32]:


df1.plot(kind = 'bar', figsize = (15,8))


# ## Visualizing Book Table Facility, Location Wise

# In[33]:


df2 = df.groupby(['location','book_table'])['name'].count()
df2.to_csv('location_booktable.csv')
df2 = pd.read_csv('location_booktable.csv')
df2 = pd.pivot_table(df2, values=None, index=['location'], columns=['book_table'], fill_value=0, aggfunc=np.sum)
df2


# In[34]:


df2.plot(kind = 'bar', figsize = (15,8))


# ## Visualizing Types of Restaurents vs Rate 

# In[35]:


plt.figure(figsize = (14, 8))
sns.boxplot(x = 'Type', y = 'rate', data = df, palette = 'inferno')


# ## Grouping Types of Restaurents, location wise

# In[36]:


df3 = df.groupby(['location','Type'])['name'].count()
df3.to_csv('location_Type.csv')
df3 = pd.read_csv('location_Type.csv')
df3 = pd.pivot_table(df3, values=None, index=['location'], columns=['Type'], fill_value=0, aggfunc=np.sum)
df3


# In[37]:


df3.plot(kind = 'bar', figsize = (36,8))


# ## No. of Votes, Location Wise

# In[38]:


df4 = df[['location', 'votes']]
df4.drop_duplicates()
df5 = df4.groupby(['location'])['votes'].sum()
df5 = df5.to_frame()
df5 = df5.sort_values('votes', ascending=False)
df5.head()


# In[39]:


plt.figure(figsize = (15,8))
sns.barplot(df5.index , df5['votes'])
plt.xticks(rotation = 90)


# In[40]:


df.head()


# ## Visualizing Top Cuisines

# In[41]:


df6 = df[['cuisines', 'votes']]
df6.drop_duplicates()
df7 = df6.groupby(['cuisines'])['votes'].sum()
df7 = df7.to_frame()
df7 = df7.sort_values('votes', ascending=False)
df7.head()


# In[42]:


df7 = df7.iloc[1:, :]
df7.head()


# In[43]:


plt.figure(figsize = (15,8))
sns.barplot(df7.index , df7['votes'])
plt.xticks(rotation = 90)


# In[ ]:




