from langchain.llms import OpenAIpip
import os
import streamlit as st


api_key = os.getenv("OPENAI_API_KEY")

### setting the UI ####
st.title("Langchain Demo WITH OPENAI API")
input_text = st.text_input("Search the country u want")
### open AI llms###

llm = OpenAI(temperature= 0.8)

if input_text:
    st.write(llm(input_text))



