import pandas as pd
import plotly.express as px
import numpy as np
import streamlit as st


data = pd.read_csv('vehicles_us.csv')

data['model_year'] = data['model_year'].fillna(data.groupby('model')['model_year'].transform('median')).astype('int64')

data['odometer'] = data['odometer'].fillna(data.groupby('model_year')['odometer'].transform('mean'))

data['car_manufacturer'] = data['model'].str.partition(' ')[0]

data['date_posted'] = pd.to_datetime(data['date_posted'],format='%Y-%m-%d')
data['year_posted'] = data['date_posted'].dt.year

data['car_age'] = data['year_posted'] - data['model_year']

data.odometer = data['odometer'].fillna(0).astype('int')


data = data[(data.price>500) & (data.price<34600) & (data.car_age<24)]

data['avg_price']=np.nan
data['avg_price'] = data['avg_price'].fillna(data.groupby(['car_manufacturer', 'type'])['price'].transform('mean')).astype('int')

data['quantity']=1

def assign_dlisted_group(days_listed):
    if days_listed>=0 and days_listed<=7:
        return 'first week'
    elif days_listed>7 and days_listed<=14:
        return 'second week'
    elif days_listed>14 and days_listed<=21:
        return 'third week'
    elif days_listed>21 and days_listed<=28:
        return 'fourth week' 
    elif days_listed>28 and days_listed<=35:
        return 'fifth week' 
    elif days_listed>35 and days_listed<=42:
        return 'sixth week' 
    elif days_listed>42 and days_listed<=49:
        return 'seventh week' 
    elif days_listed>49 and days_listed<=56:
        return 'eight week'
    elif days_listed>56 and days_listed<=63:
        return 'ninth week'
    elif days_listed>63 and days_listed<=70:
        return 'tenth week'
    elif days_listed>70 and days_listed<=77:
        return 'eleventh week'
    elif days_listed>77 and days_listed<=84:
        return 'twelfth week'
    elif days_listed>84 and days_listed<=91:
        return 'thirteenth week'
    elif days_listed>91 and days_listed<=98:
        return 'fourteenth week'
    else:
        return 'more then 98 days'
    
data['d_listed_group'] = data['days_listed'].apply(assign_dlisted_group)

st.title('Car advertisement analysis')

price_range = st.slider(
     "What is your price range?",
     value=(500, 35000))

actual_range=list(range(price_range[0],price_range[1]+1))

new_cars = st.checkbox('Cars not older 5 years')

if new_cars:
    filtered_data=data[data.price.isin(actual_range)]
    filtered_data=filtered_data[data.car_age<=5]
else:
    filtered_data=data[data.price.isin(actual_range)]

car_mileage = st.checkbox('Carmileage less 200')

if car_mileage:
    filtered_data=data[data.price.isin(actual_range)]
    filtered_data=filtered_data[data.car_mileage<=200]
else:
    filtered_data=data[data.price.isin(actual_range)]
    
st.write('Here is the list of cars with characteristics')
st.dataframe(filtered_data)

fig = px.sunburst(filtered_data, path=['car_manufacturer', 'type'], values = 'price', color='avg_price', 
                  title = 'Total price manufacturer & type')
fig.update_layout(title = {'font':dict(size = 25),
                          'x':0.47,
                          'y':0.9})
st.plotly_chart(fig)


fig1 = px.scatter(filtered_data, x="price", y="odometer", color="type", facet_col="condition", title = 'Price & odometer')
fig1.update_layout(title = {'font':dict(size = 25),
                          'x':0.47,
                          'y':0.93})
st.plotly_chart(fig1)


fig2 = px.histogram(filtered_data, x="d_listed_group", y="quantity", template = "simple_white", color="car_manufacturer", title = 'Week of purchase')
fig2.update_layout(title = {'font':dict(size = 25),
                          'x':0.47,
                          'y':0.93},
                xaxis={'categoryorder':'total descending'})
st.plotly_chart(fig2)


fig3 = px.scatter(filtered_data, x="price", y="car_age", marginal_x="histogram", title = 'Price & car age')
fig.update_layout(title = {'font':dict(size = 25),
                          'x':0.47,
                          'y':0.93})
st.plotly_chart(fig3)









