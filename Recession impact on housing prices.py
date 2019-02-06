# In[ ]:

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.

# In[17]:

# Use this dictionary to map state names to two letter acronyms
import pandas as pd
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[1]:

import pandas as pd

def get_list_of_university_towns():
  
    states_towns = []

    with open("university_towns.txt", "r") as file:
        for line in file:
            curline = line[:-1]
            if curline[-6] == '[':
                state_name = curline[:-6] 
                continue
            if '(' in curline:
                town_name = curline[:curline.index('(')-1] 
                states_towns.append([state_name, town_name])
            else:
                town_name = curline
                states_towns.append([state_name, town_name])
    df = pd.DataFrame(states_towns,columns = ['State','RegionName'])

    for row in df['State']:
        if 'University' in row:
            df.loc[df.index[df['State'] == row], 'State'] = row[:row.index('(')-1] 
            #print(df[df['State']==row[:row.index('(')-1]])

    for row in df['RegionName']:
        if 'University' in row:
            new_row = row.split(',')[1]
            df.loc[df.index[df['RegionName'] == row], 'RegionName'] = new_row 
            #print(df[df['RegionName']==new_row])
        
    return df




# In[10]:

import pandas as pd

def get_recession_start():
    gdplev = pd.read_excel('gdplev.xls', skiprows=219)
    gdplev = gdplev.iloc[:, 4:6]
    gdplev.columns = ['Quarter','GDP']
    for i in range(0, len(gdplev)):
        if (gdplev.iloc[i-2][1] > gdplev.iloc[i-1][1]) & (gdplev.iloc[i-1][1] > gdplev.iloc[i][1]):
            return gdplev.iloc[i-2][0]



# In[11]:

import pandas as pd

def get_recession_end():
    gdplev = pd.read_excel('gdplev.xls', skiprows=219)
    gdplev = gdplev.iloc[:, 4:6]
    gdplev.columns = ['Quarter','GDP']
    rec_start = get_recession_start()
    rec_start_index = gdplev[gdplev['Quarter'] == rec_start].index.tolist()[0]
    gdplev=gdplev.iloc[rec_start_index:]
    for i in range(0, len(gdplev)):
        if (gdplev.iloc[i-2][1] < gdplev.iloc[i-1][1]) & (gdplev.iloc[i-1][1] < gdplev.iloc[i][1]):
            return gdplev.iloc[i][0]


# In[27]:

import pandas as pd
     
def get_recession_bottom():
    gdplev = pd.read_excel('gdplev.xls', skiprows=219)
    gdplev = gdplev.iloc[:, 4:6]
    gdplev.columns = ['Quarter','GDP']
    start = get_recession_start()
    end = get_recession_end()
    start_index = gdplev[gdplev['Quarter'] == start].index.tolist()[0]
    end_index = gdplev[gdplev['Quarter'] == end].index.tolist()[0]
    gdplev=gdplev.iloc[start_index:end_index]
    gdplev = gdplev.reset_index(drop=True)
    min_gdp_index = gdplev[gdplev['GDP'] == gdplev['GDP'].min()].index.tolist()[0]
    return gdplev.iloc[min_gdp_index][0]



# In[14]:

import pandas as pd

states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

def convert_housing_data_to_quarters():
    housing_data = pd.read_csv('City_Zhvi_AllHomes.csv')
    years = list(range(2000, 2017))
    quarts = ['q1', 'q2', 'q3', 'q4']
    years_quarts = [] 
    for y in years:
        for q in quarts:
            years_quarts.append(str(y)+q)
    years_quarts = years_quarts[:-1]
    housing_data['State'] = housing_data['State'].map(states)
    housing_data.drop(['Metro','CountyName','RegionID','SizeRank'],axis=1,inplace=1)
    housing_data.set_index(['State','RegionName'],inplace=True)
    housing_data = housing_data.iloc[:, 45:] 
    qs_groups = [list(housing_data.columns)[x:x+3] for x in range(0, len(list(housing_data.columns)), 3)]
    for c,q in zip(years_quarts,qs_groups):
        housing_data[c] = housing_data[q].mean(axis=1)
    housing_data = housing_data[years_quarts]
    return housing_data



# In[18]:

import pandas as pd
from scipy.stats import ttest_ind

def run_ttest():
    df = convert_housing_data_to_quarters()
    df = df.loc[:,'2008q3':'2009q2']
    df = df.reset_index()

    def price_ratio(row):
        return (row['2008q3'] - row['2009q2'])/row['2008q3']

    df['Ratio'] = df.apply(price_ratio, axis = 1)

    uni_town = list(get_list_of_university_towns()['RegionName'])
    
    def is_uni_town(row):
        if row['RegionName'] in uni_town:
            return 1
        else:
            return 0

    df['is_uni'] = df.apply(is_uni_town,axis=1)
    
    
    not_uni = df[df['is_uni']==0].loc[:,'Ratio'].dropna()
    is_uni  = df[df['is_uni']==1].loc[:,'Ratio'].dropna()
    
    if not_uni.mean() < is_uni.mean():
        type_of_town = 'non-university town'
    else:
        type_of_town = 'university town'
    
    p_val = "p-value: " + str(list(ttest_ind(not_uni, is_uni))[1])
    result = (True, p_val,type_of_town)
    return result

run_ttest()





