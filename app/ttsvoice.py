from espnet2.bin.tts_inference import Text2Speech
from flask import Flask, request, jsonify, send_file
from threading import Thread
from IPython.display import Audio
import soundfile as sf
import audiosegment
import os
import time
import io 
import scipy.io.wavfile as wavfile
import numpy as np
import string
import secrets
import time
from db import DbConnect
import os

class modelObj :
    def __init__(self, modelPath:string) -> None:
        self.__model = Text2Speech.from_pretrained(model_file=modelPath, device='cpu')
        self.__recentTime = time.time()
    
    def getTime(self):
        return self.__recentTime
    
    def getIsValid(self):
        return (time.time() - self.__recentTime) < 600
    
    def updateTime(self):
        self.__recentTime = time.time()

    def getModel(self):
        return self.__model
    
    def makeText(self, txt):
        return self.__model(txt)["wav"]

def generate_random_string(length):
    letters = string.ascii_letters + string.digits 
    return ''.join(secrets.choice(letters) for _ in range(length))

def mkapp():
    app = Flask(__name__)   

    app.config['models'] = {}

    __dbUrl = os.getenv('DB_URL', 'host.docker.internal')
    __dbUsr = os.getenv('DB_USR', 'myadmin')
    __dbPwd = os.getenv('DB_PWD', 'root')
    __dbName = os.getenv('DB_NAME', 'youcaloid')

    database = DbConnect(__dbUrl, __dbUsr, __dbPwd, __dbName)

    def garbageCollecter():
        while True: 
            time.sleep(300)
            models = app.config['models']
            print(models.keys())
            delete_list = []
            for key in models.keys():
                if not models[key].getIsValid():
                    delete_list.append(key)
            for key in delete_list:
                del models[key]


    @app.route('/')
    def home():
        return "root"
    
    #모델을 사용해 음성을 합성한 뒤 리턴. post 파라미터로 modelid, textmessage 사용
    @app.route('/aitts', methods = ['GET'])
    def aitts():
        modelid = request.args['modelid']
        textmessage = request.args['textmessage']
        print("request on!")

        if modelid not in app.config['models']: 
            modelPath = database.findPath(modelid)
            print(modelPath)
            app.config['models'][modelid] = modelObj(modelPath)
  
        wav = app.config['models'][modelid].makeText(textmessage)
        
        wavarr = wav.view(-1).cpu().numpy()
        #wavarr = wavarr.astype('int16')
        print(app.config['models'][modelid].getModel().fs)

        tfname = generate_random_string(5) + '.wav'
        #wav_bytes = io.BytesIO()
        wavfile.write(tfname,app.config['models'][modelid].getModel().fs,wavarr)
        #wav_bytes.seek(0)

        audio = audiosegment.from_file(tfname)
        audio = audio.resample(sample_width=3)
        mp3_bytes = io.BytesIO()
        audio.export(mp3_bytes, format="MP3")
        mp3_bytes.seek(0)

        os.remove(tfname)
        print("generate result")
        return send_file(mp3_bytes, mimetype="audio/mpeg")
    
    gc = Thread(target=garbageCollecter)
    gc.start()
    
    return app


if __name__ == '__main__':
    app = mkapp()
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000))) 