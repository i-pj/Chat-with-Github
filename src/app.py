import streamlit as st
import repo_fetcher
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

MODEL = "llama3:8b"


@st.cache_resource
def create_qa_chain(repo_url):
    documents = repo_fetcher.main(repo_url)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000, chunk_overlap=200, separators=["\n\n", "\n", " ", ""]
    )
    chunks = []
    for document in documents:
        if document["metadata"]["file_name"].endswith(
            (".txt", ".md", ".py", ".java", ".cpp", ".js", ".html", ".css", ".c", ".h")
        ):
            file_chunks = text_splitter.create_documents(
                [document["content"]], metadatas=[document["metadata"]]
            )
            chunks.extend(file_chunks)

    embeddings = OllamaEmbeddings(model=MODEL)
    vectorstore = Chroma.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
    llm = Ollama(model=MODEL)
    prompt_template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:
{context}

Question: {question}
Answer: """
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=True,
        chain_type_kwargs={"prompt": PROMPT},
    )


def main():
    st.title("Chat with Github Repo")

    repo_url = st.text_input("Enter the GitHub repository URL:")

    if repo_url:
        with st.spinner("Loading repository and creating QA chain..."):
            qa_chain = create_qa_chain(repo_url)
        st.success("Repository loaded and QA chain created!")

        user_input = st.text_input("Ask a question about the repository:")

        if user_input:
            if user_input.lower().startswith("print "):
                file_name = user_input.split(" ", 1)[1]
                for document in repo_fetcher.main(repo_url):
                    if document["metadata"]["file_name"].endswith(file_name):
                        st.code(document["content"], language="python")
                        break
                else:
                    st.warning(
                        f"File {file_name} not found in the extracted documents."
                    )
            else:
                with st.spinner("Generating answer..."):
                    result = qa_chain.invoke({"query": user_input})
                st.write("Answer:", result["result"])
                if result.get("source_documents"):
                    sources = set(
                        [
                            doc.metadata.get("file_name", "Unknown")
                            for doc in result["source_documents"]
                        ]
                    )
                    st.write("Sources:", ", ".join(sources))
                else:
                    st.write("No relevant sources found.")


if __name__ == "__main__":
    main()
