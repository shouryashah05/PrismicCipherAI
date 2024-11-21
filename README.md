# **_PrismicCipherAI📑✨_**

This project is a multi-PDF AI chatbot that enables seamless interaction with multiple PDFs. It is ideal for students, researchers, and professionals needing to manage large volumes of information. Additionally, the open-source nature of the project promotes transparency and encourages community-driven development.

# Contents
-[Description](#Descripton)

-[How to Install and Run the Project](#How-to-Install-and-Run-the-Project)

-[Usage and Explanation](#Usage-and-Explanation)

-[License](#License)

# Description 

An AI-powered chatbot that enables seamless interaction with multiple PDFs, leveraging advanced technologies like Langchain, FAISS, and Llama 3.2 LLM. It extracts and analyzes document content efficiently, providing accurate responses to user queries. 

The chatbot ensures privacy by processing data into vector embeddings without storing or using the actual document text. 

PrismicCipherAI - The name reflects the values and ideation behind this project. _Prismic_ or simply _Prism_ signifies transparency and clarity existing within project. _Cipher_ means security and safety of user data


# How to Insall and Run the Project

To install the PrismicCipherAI chatbot, please follow these steps:

**1. Clone the repository to your local machine.**
* Create a new folder in your vs code.
* Then,Open your vs code terminal and paste ``` git clone https://github.com/shouryashah05/PrismicCipherAI.git ```
* Or else read the [Cloning a Github repo](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) document from github.


  

**2. Setting Up virtual Environment:**
* We need to setup virtual environment for us to install dependencies and also able to run the web app.
* To activate virtual environment, Open vs code terminal of your project directory and run ```python -m venv .venv``` for windows and ```python3 -m venv .venv``` for mac
* After this run ```.venv\Scripts\Activate```
  * If it shows any error to you while above step run this script-
  
    ```Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted -Force;Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted -Force;```.

    SKIP THESE IF NO ERROR IS FOUND AND VENV IS ACTIVATED
  * And then run ```.venv\Scripts\Activate``` again
-Now, you have succesfully installed and setup virtual environment and you are ready to install dependencies




**3. Installing Dependencies:**
* Open your vs code terminal and run this command to install all dependencies
  
     
     ```pip install streamlit pypdf2 langchain python-dotenv faiss-cpu huggingface_hub```
     
     ```pip install InstructorEmbedding sentence_transformers```
* Install [Ollama Setup](https://ollama.com/download) from Ollama official website
* Now lets install llama 3.2 Model, Open command prompt on windows or terminal in mac and run ```ollama pull llama3.2``` and then run ```ollama list``` to check if installed correctly
* Go back to vs code terminal and run ```pip install langchain langchain-ollama``` to finally run llama 3.2 model locally in your machine
  * **OPTIONAL** - You will run Ollama LLM model locallly and it will be slow when generating response depending upon your gpu. You can also run Openai instead but it will be paid.
    
    * If you wish to use chatgpts Openai LLM you can do that by installing ```pip install openai langchain-openai``` and make changes in code by referring to [Langchain document](https://python.langchain.com/docs/integrations/llms/openai/) for openai
    * If you dont wish to use llama 3.2 but dont want to pay openai either you can check out other LLM models on [Langchain 🦜🔗 documentation](https://python.langchain.com/docs/integrations/llms/) and [Huggingface 🤗 Documentation](https://huggingface.co/models?other=LLM)


# Usage and Explanation

Let's Now actually understand the logic behind this project and how truly the backend is working through theory and flowcharts. There are multiple steps involved in implementation let's understand them one by one:


**1. PDF Upload and Text Extraction:**

   Users upload PDFs via a Streamlit interface, and the text is extracted using the PyPDF2 library. The extracted text is then divided into smaller chunks for easier processing, and tokenization is applied to prepare the text for further steps.


**2. Vector Embedding and FAISS Storage:**

   The tokenized chunks are converted into vector embeddings using Sentence Transformers. These embeddings are stored in FAISS (Facebook AI Similarity Search), which efficiently indexes and stores vectors for fast similarity search.
   

![4aa1b4b3-7838-4ae6-8961-26203e6f85ca](https://github.com/user-attachments/assets/34e878ae-5f1a-4fa8-9858-4804147c064b)

**3. Query Processing and Retrieval:**
   
   When a user submits a query, it is tokenized and converted into an embedding. FAISS then compares this query embedding with the stored document embeddings to retrieve the most relevant sections based on cosine similarity.

   
**4. Response Generation:**

   The relevant document sections are passed to Ollama Llama 3.2 LLM, which processes the retrieved content and generates contextually appropriate responses. The output is then decoded into human-readable text using T5 for natural language generation.
   
**5. Privacy Considerations:**

   At no point is raw document text stored, only vector embeddings are retained for document retrieval. This ensures that no sensitive data is exposed or used for training.
   
![fbdb8ef5-92bb-48a8-bc77-e08f9fc7ff46](https://github.com/user-attachments/assets/cda164c0-a72a-4006-9878-8655ea3af383)

**6. User Interface:**
   
   The entire system is integrated into a user-friendly Streamlit interface, where users can upload PDFs, enter queries, and view results effortlessly. This ensures that the system is easy to use, even for individuals with limited technical expertise.


# License

[MIT License](https://opensource.org/license/MIT)

Copyright (c) 2024 Shourya Shah 


Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
