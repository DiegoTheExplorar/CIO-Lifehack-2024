import pandas as pd
import re
from datetime import datetime

# Load the dataset
crime_data = pd.read_csv('City_of_Chicago_Crime_Data.csv')

# Convert the 'Date' column to datetime format
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%m/%d/%Y %I:%M:%S %p')
    except ValueError:
        return datetime.strptime(date_str, '%m/%d/%y %H:%M')

crime_data['date_time'] = crime_data['Date'].apply(parse_date)

# Extract latitude and longitude from 'Location' column
def parse_location(location_str):
    if pd.isna(location_str):
        return None, None
    match = re.match(r'\(([^,]+), ([^,]+)\)', location_str)
    if match:
        return float(match.group(1)), float(match.group(2))
    return None, None

crime_data[['latitude', 'longitude']] = crime_data['Location'].apply(lambda loc: pd.Series(parse_location(loc)))

# Drop rows with missing latitude or longitude
crime_data.dropna(subset=['latitude', 'longitude'], inplace=True)

# Extract date and time components
crime_data['date'] = crime_data['date_time'].dt.date
crime_data['time'] = crime_data['date_time'].dt.time
crime_data['day_of_week'] = crime_data['date_time'].dt.dayofweek
crime_data['month'] = crime_data['date_time'].dt.month
crime_data['hour'] = crime_data['date_time'].dt.hour
crime_data['is_weekend'] = crime_data['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)

#just to check if code works
#print(crime_data.head())
