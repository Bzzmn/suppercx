import os
from datetime import datetime, timezone
from typing import List, Type

import requests
from crewai_tools.tools.base_tool import BaseTool
from pydantic.v1 import BaseModel, Field

class FetchLatestVideosFromYouTubeSearchInput(BaseModel):
    """Input for FetchLatestVideosFromYouTubeSearch."""

    search_query: str = Field(
        ..., description="The search query to find relevant YouTube videos."
    )
    max_results: int = Field(5, description="The maximum number of results to return.")

class VideoInfo(BaseModel):
    video_id: str
    title: str
    publish_date: datetime
    video_url: str

class FetchLatestVideosFromYouTubeSearchOutput(BaseModel):
    videos: List[VideoInfo]

class FetchLatestVideosFromYouTubeSearchTool(BaseTool):
    name: str = "Fetch Latest Videos for Search Query"
    description: str = (
        "Fetches the most relevant videos to a specified search query from YouTube."
    )
    args_schema: Type[BaseModel] = FetchLatestVideosFromYouTubeSearchInput
    return_schema: Type[BaseModel] = FetchLatestVideosFromYouTubeSearchOutput

    def _run(
        self,
        search_query: str,
        max_results: int = 5,
    ) -> FetchLatestVideosFromYouTubeSearchOutput:
        api_key = os.getenv("YOUTUBE_API_KEY")

        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": search_query,
            "maxResults": max_results,
            "order": "relevance",
            "type": "video",
            "key": api_key,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        items = response.json().get("items", [])

        videos = []
        for item in items:
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
            publish_date = datetime.fromisoformat(
                item["snippet"]["publishedAt"].replace("Z", "+00:00")
            ).astimezone(timezone.utc)
            videos.append(
                VideoInfo(
                    video_id=video_id,
                    title=title,
                    publish_date=publish_date,
                    video_url=f"https://www.youtube.com/watch?v={video_id}",
                )
            )

        return FetchLatestVideosFromYouTubeSearchOutput(videos=videos)