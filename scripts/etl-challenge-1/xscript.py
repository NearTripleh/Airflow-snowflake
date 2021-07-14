import pandas as pd
import os, sys, requests, io
from datetime import datetime

def create_insert(args):
    PWD = os.environ['pWD']
    file = PWD+'/scripts/etl-challenge-1/data.csv'
    df = pd.read_csv(file,encoding = "utf-8")
    df = df.head(100)
    inserts = "INSERT INTO ETL_CHALLENGE_1.DATA_EXAMPLE "
    for index,row in df.iterrows():
        if index == 0:
            inserts += "VALUES({0},'{1}','{2}','{3}','{4}','{5}','{6}')".format(
            row['year'],row['industry_code_ANZSIC'],row['industry_name_ANZSIC'],row['rme_size_grp'],row['variable'],row['unit'],row['value'])
        else:
            inserts += ", ({0},'{1}','{2}','{3}','{4}','{5}','{6}')".format(
            row['year'],row['industry_code_ANZSIC'],row['industry_name_ANZSIC'],row['rme_size_grp'],row['variable'],row['unit'],row['value'])

    if not  os.path.exists(PWD+'/dags/etl-challenge-1/'):
        os.mkdir(PWD+'/dags/etl-challenge-1/')

    with  io.open(PWD+'/dags/etl-challenge-1/data.sql','w') as f:
        f.write(inserts)


def download_data(args):
    PWD = os.environ['pWD']
    url = 'https://www.stats.govt.nz/assets/Uploads/Annual-enterprise-survey/Annual-enterprise-survey-2020-financial-year-provisional/Download-data/annual-enterprise-survey-2020-financial-year-provisional-size-bands-csv.csv'
    r = requests.get(url)
    open(PWD+'/scripts/etl-challenge-1/data.csv','wb').write(r.content)

def main():
    globals()[sys.argv[1]](sys.argv)

if __name__ == "__main__":
    main()