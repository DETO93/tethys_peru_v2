# Import libraries and dependencies
import os
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Change the work directory
user = os.getlogin()
user_dir = os.path.expanduser('~{}'.format(user))
os.chdir(user_dir)
os.chdir("TETHYS_PERU/backend-geoglows_peru")
print("paso")
# Import enviromental variables
load_dotenv()
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')
print("paso2")
# Generate the conection token
token = "postgresql+psycopg2://{0}:{1}@localhost:5432/{2}".format(DB_USER, DB_PASS, DB_NAME)
print("paso3")
print(token)
# Establish connection
db = create_engine(token)
print(db)
print("paso4")
conn = db.connect()

# Read streamflow stations and insert to database
data = pd.read_excel('Peru_Stations_Streamflow.xlsx', index_col=0) 
df = pd.DataFrame(data)
df.to_sql('streamflow_station', con=conn, if_exists='replace', index=False)
print("paso5")
# Read water level stations and insert to database
data = pd.read_excel('Peru_Stations_WaterLevel2.xlsx', index_col=0) 
df = pd.DataFrame(data)
print(df)
df.to_sql('waterlevel_station', con=conn, if_exists='replace', index=False)
print("paso")
# Close connection
conn.close()