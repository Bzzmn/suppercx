import os
from langchain_community.document_loaders import YoutubeLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from dotenv import load_dotenv
from app.cx_crew.utils.voyageaiEmbeddingModel import VoyageAIEmbeddings
from app.cx_crew.utils import get_project_root


project_root = get_project_root()
load_dotenv()

def add_video_to_vector_db(video_url):
    embeddings = VoyageAIEmbeddings()
    db_dir = project_root + "/db"
    loader = YoutubeLoader.from_youtube_url(video_url, add_video_info=False)
    documents = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)   
    docs = splitter.split_documents(documents)

    def create_vector_db(docs, embeddings, store_name):
        vector_store_dir = os.path.join(db_dir, store_name)
        if not os.path.exists(vector_store_dir):
            Chroma.from_documents(
            docs, embeddings, persist_directory=vector_store_dir
            )
        
    try:
        create_vector_db(docs, embeddings, "chroma_db_youtube")
        print("Vector database created successfully")
    except Exception as e:
        print(f"Error creating vector database: {e}")


def query_vector_db(store_name, query, embeddings):
    db_dir = project_root + "/db"
    vector_store_dir = os.path.join(db_dir, store_name)
    if os.path.exists(vector_store_dir):
        vector_store = Chroma(persist_directory=vector_store_dir, embedding_function=embeddings)
        retriever = vector_store.as_retriever(
            search_type = "similarity_score_threshold",
            search_kwargs = {"k": 5, "score_threshold": 0.2}
        )
        relevant_docs = retriever.invoke(query)
        return relevant_docs
    else:
        raise ValueError(f"Vector database not found in {vector_store_dir}")