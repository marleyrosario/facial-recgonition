# import necessary packages
from google.cloud import storage
import os
import pandas as pd
import requests
import json
import csv
from flask import Flask, request, jsonify
from deepface import DeepFace 

# set up environment variables
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
os.environ["GOOGLE_CLOUD_PROJECT"] = project_id
bucket_name = os.getenv("BUCKET_NAME")
bqtable = os.getenv("BQTABEL")

# setup options
pd.set_option('display.width', 1500)
storage_client = storage.Client()

app = Flask(__name__)

def upload_blob(contents, destination_blob_name):
    '''Uploads the data stored in the passed variable contents to the file name specified in destination_blob_name'''
    global storage_client, bucket_Name
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(contents, content_type="image/jpg")
class FacialRec:
    def __init__(self, js):
        self.data = pd.read_json(js)
        self.js = js
        self.userids = self.data['userID'].tolist()
    def download_images(self):
        df = pd.read_json(self.js)
        df['imageUrl'] = df['imageUrl'].astype("string")
        df = df[df['imageUrl'].str.contains('http')]
        profile_pictures = df['imageUrl'].to_list()
        i=0
        for url in profile_pictures:
            try:
                img_data = requests.get(url).content
                userid = self.userids[i]
                with open(f'/tmp/image_{userid}.jpg', 'wb') as handler:
                    handler.write(img_data)
                    handler.close()
                upload_blob(img_data, f'image_{userid}.jpg')
                i = i + 1
            except Exception as e:
              print(e)
    def run_facial_rec(self, img_path):
        try:
          face = DeepFace.analyze(img_path = img_path, actions = ['age', 'gender', 'race'], enforce_detection = False, prog_bar = False)
        except Exception as e:
          print(str(e))
          face = {'error': '500'}
        return face
    def get_list_of_files(self):
        fname = "/tmp/image_"
        list_of_fnames = []
        df = pd.read_json(self.js)
        df['imageUrl'] = df['imageUrl'].astype("string")
        df = df[df['imageUrl'].str.contains('http')]
        profile_pictures = df['imageUrl'].to_list()
        for i in range(len(profile_pictures)):
            userid = self.userids[i]
            list_of_fnames.append(fname + f"{userid}")        
        list_of_fnames = [fname + ".jpg" for fname in list_of_fnames]
        return list_of_fnames
    
    def run_facial(self):
      list_of_fnames = FacialRec.get_list_of_files(self)
      x = []
      i = 0
      for fname in list_of_fnames:
          try:  
              results = FacialRec.run_facial_rec(self, img_path = fname)
              tmp = self.data.iloc[[i]].values.tolist()
              results['imageUrl'] = tmp[0][0]
              results['userID'] = tmp[0][1]
              x.append(results)       
          except ValueError: 
              pass
          i+=1

      return x
@app.route('/', methods=['POST'])
def handle():
    global bqtable
    try:
        post_req = request.get_json()
        js = json.dumps(post_req)
        start = FacialRec(js) 
        start.download_images()    
        dataset = start.run_facial()
        dataframe = pd.json_normalize(dataset)
        cols = list(dataframe.columns)
        cols = [col.replace('.', "_") for col in cols]
        cols = [col.replace(' ', "_") for col in cols]
        dataframe.columns = cols
        dataframe.to_gbq(bqtable, project_id = project_id, if_exists='append') 
        return "200\n";
    except Exception as e:
        return str(e)
