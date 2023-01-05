import io
import os

import pandas as pd
from dotenv import load_dotenv
from minio import Minio
from pysus.online_data.CNES import download
from pysus.online_data.sinasc import download as download_sinasc

load_dotenv()


def csv_to_parquet():
    landing_bucket_name = "landing"
    curated_bucket_name = "curated"
    minio_endpoint = "localhost:9100"
    minio_access_key = os.getenv("minio_access_key")
    minio_secret_key = os.getenv("minio_secret_key")
    object_name_from = "events-sample.csv"
    object_name_to = "events-sample.parquet"

    client = Minio(
        minio_endpoint,
        access_key=minio_access_key,
        secret_key=minio_secret_key,
        secure=False
    )

    found = client.bucket_exists(landing_bucket_name)
    if not found:
        client.make_bucket(landing_bucket_name)
    else:
        print(f'Bucket {landing_bucket_name} já existe!')

    file = client.get_object(landing_bucket_name, object_name=object_name_from)

    df = pd.read_csv(file)
    bytes_data = df.to_parquet()
    buffer = io.BytesIO(bytes_data)

    print(buffer)
    client.put_object(
        curated_bucket_name,
        object_name_to,
        buffer,
        len(bytes_data),
        'application/parquet'
    )


def download_cnes():
    df = download_sinasc('SE', 2015)
    print("OK: " + df.head())
    df = download(group="ST", state="DF", year=2021, month=1, cache=True)
    print("OOOOK")
    print("GO" + df.head())


def cnes_download():
    print("!")



if __name__ == "__main__":
    download_cnes()
