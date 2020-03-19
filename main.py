import pytrends
import pandas as pd             
import re           
import google.auth
from google.cloud import bigquery
import pandas_gbq
import os
from pytrends.request import TrendReq
pytrend = TrendReq()

credentials, your_project_id = google.auth.default(
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
client = bigquery.Client(
    credentials=credentials,
    project=your_project_id,
    location='[specify location, default = 'US']'
    )

def extract():
    """
    query input keyword from GBQ
    """
    query_job = client.query("""[query]
    """)
    results = query_job.result()
    return results
def preprocess():
    """
    Some special characters in keywords need to be preprocessed in advanced
    """
    df = extract().to_dataframe()
    df.keyword_norm = df.keyword.apply(lambda x:x.replace("'",""))
    df.keyword_norm =df.keyword_norm.apply(lambda x: x.split(' (')[0])
    return df

def main(data, context):
    """
    extract related queries/topics with input keyword. Filter for last 1 month and specific geography
    """
    tops=pd.DataFrame([])
    risings=pd.DataFrame([])
    df = preprocess()
    for k,k_norm, country in zip(df.keyword,df.keyword_norm,df.country_code):
        pytrend.build_payload(kw_list=[cate2_norm],cat=0, timeframe='today 1-m', geo=country, gprop='')
        related_queries = pytrend.related_queries() #or related_queries = pytrend.related_topics()

        cate2_queries=related_queries[cate2_norm]

        top=cate2_queries['top']
        if top is not None:
            top.keyword=k
            top.country_code = country
            tops = tops.append(top,ignore_index=True)

        rising=cate2_queries['rising']
        if rising is not None:
            rising.keyword = k
            rising.country_code = country
            risings=risings.append(rising,ignore_index=True)
        credentials, your_project_id = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
        client = bigquery.Client(credentials=credentials,project=your_project_id,location='['specify loaction, default='US')
        pandas_gbq.to_gbq(tops,destination_table='[dataset_id.table_id]',project_id='[project_id]',if_exists='replace')
        pandas_gbq.to_gbq(risings,destination_table='[dataset_id.table_id]',project_id='[project_id]',if_exists='replace')
    return print('channel google trends to GBQ')
if __name__ == "__main__":
    main('data','context')