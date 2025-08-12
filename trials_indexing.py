import httpx
import json
import asyncio
from dbconnection import auth, url
import dbconnection
from utilities import settings
from data_loader import load_json

def file_names():
    return [
        '300000-draft.json',
        '100000-draft.json',
        '500000-draft.json',
        '548000-draft.json',
        '400000-draft.json',
        '200000-draft.json',
    ]

headers = {"Content-Type": "application/json"}

async def data_indexing(trial, url):
    async with httpx.AsyncClient() as client:
        response = await client.post(url, auth=auth, headers=headers, content=json.dumps(trial))
        return response

async def process_file(file_path, url, index_name):
    # Load JSON data from file
    data = load_json(source=file_path,source_type="local")
    
    start = 0
    offset = 100
    count = 0
    total = len(data)

    while start < total:
        batch = data[start : start + offset]
        tasks = [data_indexing(trial=item, url=f"{url}{index_name}/_doc/") for item in batch]
        try:
            responses = await asyncio.gather(*tasks)
            count += len(batch)
            print(f"Indexed {count}/{total} from {file_path}")
        except Exception as e:
            print(f"Error indexing batch starting at {start} from {file_path}: {e}")
            await asyncio.sleep(5)  # async sleep instead of time.sleep
            continue  # retry the same batch on error (optional)

        start += offset

async def main():
    # Define your Elasticsearch/OpenSearch URL and index name here
    url = dbconnection.url  # <-- replace with your actual URL
    index_name = settings.index_name          # <-- replace with your actual index name

    files = file_names()

    # Process files sequentially, one after another
    for file_path in files:
        print(f"Starting indexing for {file_path}...")
        await process_file(file_path, url, index_name)
        print(f"Finished indexing {file_path}.")

if __name__ == "__main__":
    asyncio.run(main())
