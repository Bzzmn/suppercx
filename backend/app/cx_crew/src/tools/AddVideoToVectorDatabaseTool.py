from typing import Type
from crewai_tools.tools.base_tool import BaseTool
from dotenv import load_dotenv
from app.cx_crew.utils.youtubeRagUtility import add_video_to_vector_db, query_vector_db
from pydantic.v1 import BaseModel, Field
from app.cx_crew.utils.voyageaiEmbeddingModel import VoyageAIEmbeddings

load_dotenv()

embeddings = VoyageAIEmbeddings()

class AddVideoToVectorDBInput(BaseModel):
    """Input for FetchLatestVideosForChannel."""

    video_url: str = Field(
        ..., description="The URL of the YouTube video to add to the vector DB."
    )


class AddVideoToVectorDBOutput(BaseModel):
    success: bool = Field(
        ..., description="Whether the video was successfully added to the vector DB."
    )


class AddVideoToVectorDBTool(BaseTool):
    name: str = "Add Video to Vector DB"
    description: str = "Adds a YouTube video to the vector database."
    args_schema: Type[BaseModel] = AddVideoToVectorDBInput
    return_schema: Type[BaseModel] = AddVideoToVectorDBOutput

    def _run(self, video_url: str) -> AddVideoToVectorDBOutput:
        try:
            add_video_to_vector_db(video_url)
            return AddVideoToVectorDBOutput(success=True)
        except Exception as e:
            print(f"An error occurred: {e}")
            return AddVideoToVectorDBOutput(success=False)
        

class QueryVectorDBInput(BaseModel):
    query: str = Field(..., description="The query to search the vector database with.")

class QueryVectorDBOutput(BaseModel):
    result: str = Field(..., description="The result of the query.")

class QueryVectorDBTool(BaseTool):
    name: str = "Query Vector DB"
    description: str = "Queries the vector database."
    args_schema: Type[BaseModel] = QueryVectorDBInput
    return_schema: Type[BaseModel] = QueryVectorDBOutput


    def _run(self, 
             query: str,
             store_name: str = "chroma_db_youtube", 
             embeddings=embeddings) -> QueryVectorDBOutput:
        try:
            query_vector_db(store_name, query, embeddings)
            return QueryVectorDBOutput(success=True)
        except Exception as e:
            print(f"An error occurred: {e}")
            return QueryVectorDBOutput(success=False)