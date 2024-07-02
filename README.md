# Purpose of the repo:
<p> In the past years, I worked on alot of interesting problems and projects. However, as it is company realted problems, it is confidential and can't be viewed publicly. Therefore i wanted to build this portfolio</p>

<p>The purpose of this repo, is to showcase my skills in Data science,Engineering as well as Analytics Field.
I am constantly updating it with projects that tackle a specfic problem category of Machine learning.
You can see that the repo is divided into 6 different  Probelm Categories: Classification, Deep_learning, NLP, Recomender Systems, Regression and Time series.</p>

<p>My Strategy is to start with simple projects that tackle all the 6 different problems categories. After that, increase complexity as i move on. That is because, i want to showcase my skills in the shortest time possible.</p>

# CI/CD:
- In this repo, I wanted also to highlight my knowledge using CI/CD.
- You will find that every project has a seperate branch, that is merged with the main branch when the project is complete.
- Inside the project branch, different commits, that represents editing or adding a new part for the project.

# Completed Projects

- Regression problems:
  - Housing prices problems:
    - Dealing with different ways to handle missing data, filling missing data, gaining insights, dropping unwanted features and trying different models and choosing one. In addtion, different visualizations that helps us to gain more insight about the data.
   
- Classification problems
  - Music genre classification problem

- NLP and LLM projects
  - Country Info LLM
    - Built a simple application using Langchain and streamlit. With the help of An openAI model i built an application, where you put the name of the country. It then returns info about that country, borders info and the three unique things that a typical person from that person do in a typical day.
    - Used LLMchain, PromptTemplate, ConversationBufferMemory, SequentialChain, streamlit, OpenAI
  - RAG_LLM
    - Built a simple Pdf querying system using rag system and llamaindex. With the help of the system i am able to query different questions about scientific papers which i store in the data directory of the system.
    - The data is read using the SimpleDirectoryReader, converted into indicies using the VectorStoreIndex
    - A query engine is setup using a VectorIndexRetriver,SimilarityPostProcessor
    - The indices are stored on the harddisk using the StorageContext
    - The different results are showed using pprint_response
- Recommender Systems
    - Movie Recommender System
      - Built a simple movie recommender system, using the 2 types
        - First type is using Callobrative filtering
        - Second type is using content baseed filtering
      - Callobrative Filtering
          - used NearestNeighbors model as well as a pivot_table in the form of dataframe, where the index is the title and the columsn are the users and the values are different ratings to compute different distances based on cosine similarity matrix and recommend based on that
       - Content baseed filtering
         - used the TfidfVectorizer as well as sigmoid_kernel to compare similarties between summaries of different movies and recommend based on that
- Time series
   - Intelligent Defrosting:
     Created synthetic data, preformed time series segmentation and extract features from each segment.
     
      
  
    



