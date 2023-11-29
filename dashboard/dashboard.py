import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

# Set style seaborn
sns.set(style='dark')

# Data Preparation
df = pd.read_csv("day.csv")

# Drop unused column
drop_col = ['windspeed']

for i in df.columns:
    if i in drop_col:
        df.drop(labels=i, axis=1, inplace=True)

# Change column name
df.rename(columns={
    'dteday': 'date',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather_condition',
    'cnt': 'count',
    'hum': 'humidity'
}, inplace=True)

# Change value detail for column weekday, month, season, and weather condition
df['month'] = df['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})
df['season'] = df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
df['weekday'] = df['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
})
df['weather_condition'] = df['weather_condition'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Misty/Cloudy',
    3: 'Light Snow/Light Rain',
    4: 'Severe Weather'
})


# Creating daily_rent_df
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='date').agg({
        'count': 'sum'
    }).reset_index()
    return daily_rent_df

# Creating daily_casual_rent_df


def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by='date').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_rent_df

# Creating daily_registered_rent_df


def create_daily_registered_rent_df(df):
    daily_registered_rent_df = df.groupby(by='date').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_df

# Creating season_rent_df

def create_season_rent_df(df):
    season_rent_df = df.groupby(
        by='season')[['registered', 'casual']].sum().reset_index()
    return season_rent_df

# Creating monthly_rent_df


def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by='month').agg({
        'count': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df

# Creating weekday_rent_df


def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_rent_df

# Creating workingday_rent_df


def create_workingday_rent_df(df):
    workingday_rent_df = df.groupby(by='workingday').agg({
        'count': 'sum'
    }).reset_index()
    return workingday_rent_df

# Creating holiday_rent_df


def create_holiday_rent_df(df):
    holiday_rent_df = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_rent_df

# Creating weather_rent_df


def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by='weather_condition').agg({
        'count': 'sum'
    })
    return weather_rent_df


min_date = pd.to_datetime(df['date']).dt.date.min()
max_date = pd.to_datetime(df['date']).dt.date.max()

with st.sidebar:

    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df[(df['date'] >= str(start_date)) &
             (df['date'] <= str(end_date))]

# Creating several dataframe
daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
monthly_rent_df = create_monthly_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
workingday_rent_df = create_workingday_rent_df(main_df)
holiday_rent_df = create_holiday_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)


# Creating The full dashboard

# Creating Title
st.header('Bike Rental Dashboard 🚲')

# Creating Daily bike rentals
st.subheader('Daily Bike Rentals')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_registered = daily_registered_rent_df['registered'].sum()
    st.metric('Registered Bike User', value=daily_rent_registered)

with col2:
    daily_rent_casual = daily_casual_rent_df['casual'].sum()
    st.metric('Casual Bike User', value=daily_rent_casual)

with col3:
    daily_rent_total = daily_rent_df['count'].sum()
    st.metric('Total Bike User', value=daily_rent_total)

# Creating Monthly Bike Rentals
st.subheader('Monthly Bike Rentals')
fig, ax = plt.subplots(figsize=(24, 8))
ax.plot(
    monthly_rent_df.index,
    monthly_rent_df['count'],
    marker='o',
    linewidth=2,
    color='tab:orange'
)

for index, row in enumerate(monthly_rent_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

# Creating Seasonly Bike Rentals
st.subheader('Seasonly Bike Rentals')

fig, ax = plt.subplots(figsize=(16, 8))

sns.barplot(
    x='season',
    y='registered',
    data=season_rent_df,
    label='Registered',
    color='tab:green',
    ax=ax
)

sns.barplot(
    x='season',
    y='casual',
    data=season_rent_df,
    label='Casual',
    color='tab:orange',
    ax=ax
)

for index, row in season_rent_df.iterrows():
    ax.text(index, row['registered'], str(row['registered']),
            ha='center', va='bottom', fontsize=12)
    ax.text(index, row['casual'], str(row['casual']),
            ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20, rotation=0)
ax.tick_params(axis='y', labelsize=15)
ax.legend()
st.pyplot(fig)

# Creating Weekday, Workingday, and Holiday Rentals
st.subheader('Weekday, Workingday, and Holiday Rentals')

fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(15, 10))

colors1 = ["tab:green", "tab:orange"]
colors2 = ["tab:green", "tab:orange"]
colors3 = ["tab:red", "tab:orange", "tab:pink",
           "tab:green", "tab:blue", "tab:cyan", "tab:purple"]

# Based on workingday
sns.barplot(
    x='workingday',
    y='count',
    data=workingday_rent_df,
    palette=colors1,
    ax=axes[0])

for index, row in enumerate(workingday_rent_df['count']):
    axes[0].text(index, row + 1, str(row),
                 ha='center', va='bottom', fontsize=12)

axes[0].set_title('Number of Rents based on Working Day')
axes[0].set_ylabel(None)
axes[0].tick_params(axis='x', labelsize=15)
axes[0].tick_params(axis='y', labelsize=10)

# Based on holiday
sns.barplot(
    x='holiday',
    y='count',
    data=holiday_rent_df,
    palette=colors2,
    ax=axes[1])

for index, row in enumerate(holiday_rent_df['count']):
    axes[1].text(index, row + 1, str(row),
                 ha='center', va='bottom', fontsize=12)

axes[1].set_title('Number of Rents based on Holiday')
axes[1].set_ylabel(None)
axes[1].tick_params(axis='x', labelsize=15)
axes[1].tick_params(axis='y', labelsize=10)

# Based on weekday
sns.barplot(
    x='weekday',
    y='count',
    data=weekday_rent_df,
    palette=colors3,
    ax=axes[2])

for index, row in enumerate(weekday_rent_df['count']):
    axes[2].text(index, row + 1, str(row),
                 ha='center', va='bottom', fontsize=12)

axes[2].set_title('Number of Rents based on Weekday')
axes[2].set_ylabel(None)
axes[2].tick_params(axis='x', labelsize=15)
axes[2].tick_params(axis='y', labelsize=10)

plt.tight_layout()
st.pyplot(fig)

# Creating Weatherly Bike Rentals
st.subheader('Weatherly Bike Rentals')

fig, ax = plt.subplots(figsize=(16, 8))

colors = ["tab:blue", "tab:red", "tab:green"]

sns.barplot(
    x=weather_rent_df.index,
    y=weather_rent_df['count'],
    palette=colors,
    ax=ax
)

for index, row in enumerate(weather_rent_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

st.caption('Copyright (c) Chalil Al Vareel 2023')
