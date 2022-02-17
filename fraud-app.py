import streamlit as st
from google.cloud import aiplatform
import pandas as pd
import numpy as np

# batch upload
# present data
# sent to vertex
# present predictions

PROJECT = "71149810252"
LOCATION = "us-west1"

def init_endpoint(endpoint_name):
    aiplatform.init(project=PROJECT, location=LOCATION) # , 
    endpoint = aiplatform.Endpoint(endpoint_name="5253765624676483072")
    return endpoint

def predict(endpoint, payload):
    prediction_obj = endpoint.predict(payload)
    predictions = np.array(prediction_obj.predictions, dtype=np.float16)
    isFraud = predictions >= 0.5
    result = pd.DataFrame({"prediction": predictions, "isFraud": isFraud})
    st.text("Results:")
    st.table(result)
    return result

st.title("Fraud Detection")
st.write("Dear Consultant, please upload your batch")
batch = st.file_uploader("CSV Batch upload", type=["csv"])
if batch:
    payload = pd.read_csv(batch)
    st.table(payload)
    # mock payload
    # payload = [
    #     [1.00, 3.00, 1864.28, 21249.00, 19384.72, 0, 0, 0],
    #     [1.00, 3.00, 9964.28, 21249.00, 19384.72, 0, 0, 0]
    # ]

endpoint = init_endpoint(ENDPOINT_NAME)

clicked = st.button("Send for analysis", on_click=lambda: predict(endpoint, payload))
