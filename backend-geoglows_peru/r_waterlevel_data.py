from hs_restclient import HydroShare, HydroShareAuthBasic
from dotenv import load_dotenv
import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import numpy as np


# Change the work directory
user = os.getlogin()
user_dir = os.path.expanduser('~{}'.format(user))
os.chdir(user_dir)
os.chdir("tethys_peru_v2/backend-geoglows_peru")


# Import enviromental variables
load_dotenv()
HS_USER = os.getenv('HS_USER') # Hydroshare username
HS_PASS = os.getenv('HS_PASS') # Hydroshare password
HS_REID = os.getenv('HS_REID') # Hydroshare resource ID
DB_USER = os.getenv('DB_USER') # Database username
DB_PASS = os.getenv('DB_PASS') # Database password
DB_NAME = os.getenv('DB_NAME') # Database name

# Authentication on hydroshare
auth = HydroShareAuthBasic(username = HS_USER, password = HS_PASS)
hs = HydroShare(auth=auth)

def __download_data__(url):
    try:
        tmp = pd.read_csv(url, index_col=0)
    except:
        __download_data__(url)
    finally:
        return tmp


# Function to retrieve the observed data from station
def get_observed_data(code):
    # Open the resource
    hs.setAccessRules(HS_REID, public=True)
    # Download observed data
    #Caudales
    #url = 'https://www.hydroshare.org/resource/{0}/data/contents/Waterlevel_Data/{1}.csv'.format(HS_REID, code)
    #Niveles
    url = 'https://www.hydroshare.org/resource/{0}/data/contents/Water_Level_Data/{1}.csv'.format(HS_REID, code)

    df = pd.read_csv(url, index_col=0)
    
    # Close the resource
    hs.setAccessRules(HS_REID, public=False)
    # Formating the data
    df.index = pd.to_datetime(df.index)
    df.index.name = "datetime"
    df = df.rename(columns={"Water_level (m)":"waterlevel"})
    # Returning
    return(df)

# Generate the conection token for database
token = "postgresql+psycopg2://{0}:{1}@localhost:5432/{2}".format(DB_USER, DB_PASS, DB_NAME)
  
# Establish connection to database
db = create_engine(token)
conn = db.connect()
try:
    # Retrieve data from database
    stations =  pd.read_sql("select code from waterlevel_station;", conn)
    # stations = ["202930", "221811", "221506","4726E508"]
    #stations = ['472147C4',
    '472182DA',
    '472191AC',
    '472210B6',
    '4724966C',
    '4724A3F6',
    '4724D566',
    '472501F4',
    '472501F4',
    '47251282',
    '47251282',
    '47251282',
    '47252718',
    '47265686',
    '4726D092',
    '4726E508',
    '47270400',
    '47278214',
    '47278214',
    '472A32FC',
    '472A571A',
    '472A9204',
    '472B2370',
    '472B3006',
    '472B55E0',
    '472B607A',
    '472B730C',
    '472D0552',
    '472D1624',
    '472D23BE',
    '472DA5AA',
    '472E8448',
    '472ED434',
    '472EE1AE',
    '47A03AC4',
    '47E01126',
    '47E024BC',
    '47E0415A',
    '47E0522C',
    '47E067B6',
    '47E074C0',
    '47E08444',
    '47E08444',
    '47E0B1DE',
    '47E0C74E',
    '47E0D438',
    '47E113DC',
    '47E13530',
    '47E143A0',
    '47E150D6',
    '47E1654C',
    '47E186BE',
    '47E195C8',
    '47E1A052',
    '47E1B324',
    '47E1C5B4',
    '47E1D6C2',
    '47E1E358',
    '47E1F02E',
    '47E207A4',
    '47E214D2',
    '47E214D2',
    '47E22148',
    '47E2323E',
    '47E244AE',
    '47E257D8',
    '47E26242',
    '47E27134',
    '47E2E456',
    #'47E9177A']


    # Error list
    error_list = []

    # Loop routine
    # n = len(stations.code)
    n = len(stations)

    for i in range(n):
        code = stations[i]
        # code = stations.code[i]

        # Progress
        prog = round(100 * i/n, 3)
        print("Progress: {0} %. Station: {1}".format(prog, code))
        try:
            # Download and insert into database
            observed_df = get_observed_data(code.upper())
            table = 'wl_{0}'.format(code.lower())
            table_tmp = 'wl_{0}'.format(code)

            print(observed_df.head())

            conn.execute("DROP TABLE IF EXISTS {0};".format(table))
            conn.execute("DROP TABLE IF EXISTS {0};".format(table_tmp))

            observed_df.to_sql(table, con=conn, if_exists='replace', index=True)
        except Exception as e :
            print(e)
            print("Error downloading data in station {0}".format(code))
            error_list = np.append(error_list, code)

finally:
    # Close connection
    conn.close()








