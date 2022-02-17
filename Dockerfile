FROM gcr.io/google-appengine/python

RUN pip3 install --upgrade pip

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt


ENV PORT=

COPY fraud-app.py

CMD streamlit run fraud-app.py --server.port=${PORT} --browser.serverAddress="0.0.0.0"
