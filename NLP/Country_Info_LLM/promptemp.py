from langchain_community.llms import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

from langchain.chains import SequentialChain
import os
import streamlit as st



api_key = os.getenv("OPENAI_API_KEY")



### setting the UI ####
st.title('Country Search Results')
input_text=st.text_input("Type the country you want to search")

### Defining the LLM
## OPENAI LLMS
llm=OpenAI(temperature=0.8)

# Prompt Template
## Defining prompt templates that will act as different tempelates in an input memory

first_input_prompt=PromptTemplate(
    input_variables=['country'],
    template="give me information about this {country}"
)

second_input_prompt=PromptTemplate(
    input_variables=['country_info'],
    template="tell me the  borders of this {country} from the north, south, east and west"
)


third_input_prompt=PromptTemplate(
    input_variables=['country'],
    template="Mention Three unique things about an average person from that  {country} typical day consists of, something special about a person from that {country} "
)

# Defining the memory Memory

country_memory = ConversationBufferMemory(input_key='country', memory_key='chat_history')
borders_memory = ConversationBufferMemory(input_key='country', memory_key='borders_info')
descr_memory = ConversationBufferMemory(input_key='country', memory_key='description_history')


### different chains
first_chain=LLMChain(
    llm=llm,prompt=first_input_prompt,verbose=True,output_key='country_info',memory=country_memory)

second_chain=LLMChain(
    llm=llm,prompt=second_input_prompt,verbose=True,output_key='borders',memory=borders_memory)

third_chain =LLMChain(llm=llm,prompt=third_input_prompt,verbose=True,output_key='description',memory=descr_memory)

### Defining the connecting chain 
parent_chain=SequentialChain(
    chains=[first_chain,second_chain,third_chain],input_variables=['country'],output_variables=['country_info','borders','description'],verbose=True)



if input_text:
    result = parent_chain({'country':input_text})
    st.write(result)

    with st.expander('Country Info'): 
        st.info(country_memory.buffer)

    with st.expander('More Info'): 
        st.info(result['borders'])     

    with st.expander('A typical person day in this country includes'): 
        st.info(result["description"])



