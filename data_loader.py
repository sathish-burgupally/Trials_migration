import json
import os
import requests

def load_json(source: str, source_type: str):
    """
    Load JSON data from a local file or an S3/HTTP URL.

    Args:
        source (str): Local file path or HTTPS URL.
        source_type (str): 'local' or 's3'.

    Returns:
        dict | list: Parsed JSON data.
    """
    source_type = source_type.lower()

    if source_type == "s3":
        if not (source.startswith("http://") or source.startswith("https://")):
            raise ValueError("For 's3', source must be a valid HTTP/HTTPS URL")
        response = requests.get(source)
        response.raise_for_status()
        print(source,"File from s3 loaded sucessfully")
        return response.json()

    elif source_type == "local":
        l1 = os.listdir()
        if not "filtered_records" in l1:
            print(l1)
            raise FileNotFoundError("No file fouubd filtered_records in the working directory ")
        else :
            with open(f"filtered_records/{source}","r") as fp:
                data  =  json.load(fp=fp)
            print(source,"File from local loaded sucessfully")
            return data
          
    else:
        raise ValueError("source_type must be 'local' or 's3'")
    
if __name__ == "__main__" :
    load_json(source="empty",source_type="empty")

