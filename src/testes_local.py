import os
import io
from minio import Minio
from minio.error import S3Error
import pandas as pd
from dotenv import load_dotenv

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


if __name__ == "__main__":
    try:
        csv_to_parquet()
    except S3Error as exc:
        print("error occurred.", exc)
