import sys
sys.path.insert(0, '.')
from src.storage.s3_client import S3Client

BUCKET = "perfumeshop-ai-data-958125727387-eu-south-2-an"
s3 = S3Client(BUCKET)

s3.upload_file("data/embeddings/perfumes.npy", "embeddings/perfumes.npy")
print("embeddings upload OK")

s3.upload_file("data/raw/fragrantica.csv", "data/fragrantica.csv")
print("CSV upload OK")
