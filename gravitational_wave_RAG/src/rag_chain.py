import os

from dotenv import load_dotenv

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings
)
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_pinecone import PineconeVectorStore

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2"
)

vectorstore = PineconeVectorStore(
    index_name=os.getenv("INDEX_NAME"),
    embedding=embeddings
)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 4}
)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)

from langchain_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from_template(
"""
You are a Gravitational Wave Research Assistant specializing in gravitational wave astronomy, black hole mergers, neutron star collisions, and LIGO observations.

Use ONLY the information provided in the context to answer the user's question.

Instructions:
- Provide detailed explanations between 100 and 200 words whenever sufficient information is available.
- Explain concepts in a clear and educational manner.
- Include important scientific details, causes, significance, and implications when relevant.
- If the context contains partial information, use all relevant details from the context to construct a complete explanation.
- Do not make up facts that are not supported by the context.
- Do not mention that you are using context.
- Structure the answer in 1-3 well-written paragraphs.

If the answer cannot be determined from the provided context, respond exactly with:

"I could not find that information in my knowledge base."


Context:
{context}

Question:
{question}
"""
)

def format_docs(docs):
    return "\n\n".join(
        doc.page_content
        for doc in docs
    )

rag_chain = (
    {
        "context": retriever | format_docs,
        "question": RunnablePassthrough()
    }
    | prompt
    | llm
    | StrOutputParser()
)