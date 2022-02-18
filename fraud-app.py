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
ENDPOINT_NAME = "1785993911601201152"

def init_endpoint(endpoint_name):
    aiplatform.init(project=PROJECT, location=LOCATION) # , 
    endpoint = aiplatform.Endpoint(endpoint_name=endpoint_name)
    return endpoint

def predict(endpoint, payload):
    # prediction_obj = endpoint.predict(payload)
    explanation_obj = endpoint.explain(payload)
    # print(explanation_obj)
    # print(prediction_obj, print(endpoint), print(dir(endpoint)))
    predictions = np.array(explanation_obj.predictions, dtype=np.float16)
    explanations = explanation_obj.explanations
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
    print(payload.shape)
    st.table(payload)
    payload = payload.to_numpy().tolist()
    # mock payload
    # payload = [
    #     [1.00, 3.00, 1864.28, 21249.00, 19384.72, 0, 0, 0],
    #     [1.00, 3.00, 9964.28, 21249.00, 19384.72, 0, 0, 0]
    # ]

endpoint = init_endpoint(ENDPOINT_NAME)

clicked = st.button("Send for analysis", on_click=lambda: predict(endpoint, payload))
