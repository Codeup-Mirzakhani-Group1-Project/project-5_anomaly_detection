import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import os
import env



def get_db_url(db, user=env.user, password=env.password, host=env.host):
    '''
    This function uses the imported host, username, password from env file, 
    and takes in a database name and returns the url to access that database.
    '''

    return f'mysql+pymysql://{user}:{password}@{host}/{db}' 

def convert_txt_data():
    '''
    Takes the txt file we received and converts to a df
    '''
    # Import .txt file and convert it to a DataFrame object
    df = pd.read_table("anonymized-curriculum-access.txt", sep = '\s', header = None, 
                    names = ['date', 'time', 'page', 'user_id', 'cohort_id', 'ip'])
    
    return df

def get_cohort_data():
    '''
    This reads the cohort data from the Codeup db into a df.
    '''
    # Create SQL query.
    sql_query = '''
                SELECT id as cohort_id, 
                name,
                start_date,
                end_date,
                program_id 
                FROM cohorts;
                '''

    # Read in DataFrame from Codeup db.
    df = pd.read_sql(sql_query, get_db_url(db = 'curriculum_logs'))

    return df

def acquire_anonymized_curriculum_access_data():
    ''' 
    Checks to see if there is a local copy of the data, 
    if not then go get data from Codeup database and combine it with our txt file
    '''

    filename = 'curriculum_access_data.csv'
    
    #if we don't have cached data or we want to get new data go get it from server
    if (os.path.isfile(filename) == False):
        #run function to convert txt file to df
        df = convert_txt_data()

        #run function to get cohort data from the db server
        df2 = get_cohort_data()

        #combine the two dfs
        df = df.merge(df2, on = 'cohort_id', how='left')

        #save as csv
        df.to_csv(filename,index=False)

    #else used cached data
    else:
        df = pd.read_csv(filename)
          
    return df

def add_program_type(df):
    '''
    Takes in a df and converts the program id into the appropriate
    program type
    '''
    #convert program_id to string
    df['program_id'] = df['program_id'].astype(str)

    #replace the program id with the type
    df['program_id'] = df['program_id'].replace(str(1.0), "PHP")
    df['program_id'] = df['program_id'].replace(str(2.0), "Java")
    df['program_id'] = df['program_id'].replace(str(3.0), "Data Science")
    df['program_id'] = df['program_id'].replace(str(4.0), "Front End")

    return df

def convert_datetimes(df):
    '''
    Takes the three dates in the df and converts to datetime type
    '''
    # change dates to datetime type
    df['date'] = pd.to_datetime(df['date'])
    df['start_date'] = pd.to_datetime(df['start_date'])
    df['end_date'] = pd.to_datetime(df['end_date'])
    
    #set df index as the access date
    df = df.set_index(df['date'])

    return df

def clean_the_data(df):
    '''
    Takes in a df and runs the appropriate functions to clean the data
    '''

    df = add_program_type(df)
    df = convert_datetimes(df)

    return df