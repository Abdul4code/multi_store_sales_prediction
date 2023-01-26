import calendar
from calendar import monthrange
import pandas as pd
import pickle as pkl
from sklearn.preprocessing import StandardScaler
import numpy as np

def create_prediction_dataframe(start_date, period, store_id, product_id):
    year = start_date.year
    month = start_date.month
    day = start_date.day

    days_in_month = monthrange(year, month)[1] # number of days in the month
    weeks_in_month = calendar.monthcalendar(year, month)

    if period == 'daily':
        date = ["{}-{}-{}".format(year, month, day)]
    elif period == 'weekly':
        current_week = [x for x in weeks_in_month if day in x][0]
        date =  [
                    "{}-{}-{}".format(year, month, current_week[index]) 
                    for index in range(current_week.index(day), len(current_week))
        ]
    elif period == 'monthly':
        date = [
            "{}-{}-{}".format(year, month, index) 
            for index in range(day, days_in_month + 1)
        ]
    
    store_id = [store_id] * len(date)
    product_id = [product_id] * len(date)

    df = pd.DataFrame({'id':range(len(date)), 'date':date, "store":store_id, "item":product_id})
    df['date'] = pd.to_datetime(df['date'])
    
    return df

def create_time_features(df):
    ''' Returns a dataframe with new features added 
        
        Parameters
        ------------
        df: dataframe - takes a dataframe with date feature. 
        
        Return
        ------------
        df - Dataframe with new features added to it.
    '''
 
    df['year'] = df.date.dt.year # Add year extracted from date feature
    df['month'] = df.date.dt.month # Add month. Value range from 1 - 12.
    df['day'] = df.date.dt.day # Add day of the month. Ranges between 1 - 31
    df['week'] = df.date.dt.isocalendar().week # Add week of the year. Ranges from 1 - 53
    df['day_of_week'] = df.date.dt.day_of_week # Add day of week. Ranges from 0 to 6
    df['day_of_year'] = df.date.dt.day_of_year # Add day of year. Ranges from 1 to 366
    df['quarter'] = df.date.dt.quarter # add quarter. Ranges from 1 - 4
    
    return df


def drop_date(df):
    df = df.drop('date', axis=1)
    return df


def split(df, target):
    X = df.drop(target, axis=1)
    y = df[target]
    return X, y


# use saved scaler
def scale_features(df):
    with open('./models/scaler.plk', 'rb') as f:
        scaler = pkl.load(f)

    df_scaled = scaler.transform(df)
    return df_scaled

def clean_data(df, split_data = False):
    
    # create time features
    df_cleaned = create_time_features(df)
    
    # drop the initial date feature
    df_cleaned = drop_date(df_cleaned)
    
    # fill missing values
    df_cleaned = df_cleaned.fillna(0)
    
    # split data if the purpose is for model training
    if split_data:
        try:
            df_X, df_y = split(df_cleaned, 'sales')
            scaled_X = scale_features(df_X)
        except:
            return ('Failed to split your dataset. Try passing in a dataframe with sales feature')
        
        return scaled_X, df_y
    else:
        df_cleaned = df_cleaned.drop('id', axis=1)
        return scale_features(df_cleaned)


def preprocess(df):
    df = clean_data(df)
    return df

def predict(df):
    with open('./models/model.plk', 'rb') as f:
        model = pkl.load(f)

    prediction = model.predict(df)
    num_days = len(prediction)
    prediction = np.sum(prediction)
    return (int(np.round(prediction, decimals=0)), 
            int(np.round(prediction / num_days, decimals=0))
            )