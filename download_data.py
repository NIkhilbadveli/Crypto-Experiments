import os
import requests
import gzip, shutil
import pandas as pd


def download(url: str, dest_folder: str):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)  # create folder if it does not exist

    filename = url.split('/')[-1].replace(" ", "_")  # be careful with file names
    file_path = os.path.join(dest_folder, filename)

    r = requests.get(url, stream=True)
    if r.ok:
        print("saving to", os.path.abspath(file_path))
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 8):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
    else:  # HTTP status code 4XX/5XX
        print("Download failed: status code {}\n{}".format(r.status_code, r.text))


dates = [x.strftime("%Y%m%d") for x in pd.date_range(start="2021-09-01", end="2021-12-01").to_pydatetime().tolist()]

folder_name = "BlockData"

for date in dates:
    file_url = "https://gz.blockchair.com/bitcoin/blocks/blockchair_bitcoin_blocks_" + date + ".tsv.gz"
    download(file_url, folder_name)
    file_name = file_url.split('/')[-1].replace(" ", "_")
    with gzip.open(folder_name + '/' + file_name, 'r') as f_in, open(folder_name + '/' + file_name[:-3], 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    os.remove(folder_name + '/' + file_name)
