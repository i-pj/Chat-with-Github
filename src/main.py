from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory

with open("data/README.md", "r") as file:
    readme_content = file.read()

# break into chunks
text_splitter = CharacterTextSplitter(chunk_size=20000, chunk_overlap=200)
chunks = text_splitter.split_text(readme_content)

# ollama creates embedding
embeddings = OllamaEmbeddings(model="tinyllama")

# chroma uses OpenTelemetru
vectorstore = Chroma.from_texts(chunks, embeddings)

retriever = vectorstore.as_retriever()
llm = Ollama(model="tinyllama")

memory = ConversationBufferMemory(
    memory_key="chat_history", return_messages=True, output_key="result"
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    memory=memory,
    return_source_documents=True,
)

print("Type 'exit' to end the conversation.")

while True:
    user_input = input("\nYour question: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    result = qa_chain.invoke({"query": user_input})
    print("\nAnswer:", result["result"])
