FROM python:3.8

COPY ./app/ /app

RUN apt-get update \
&& apt install -y ffmpeg \
&& pip install --upgrade pip \
&& pip install espnet \
&& pip install Flask \
&& pip install IPython \
&& pip install audiosegment \
&& pip install pymysql \
&& pip install g2pk  \
&& pip install torchaudio

CMD ["python3", "/app/ttsvoice.py"]

EXPOSE 5000