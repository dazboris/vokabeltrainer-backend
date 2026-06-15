from pydantic import BaseModel


class TopicRead(BaseModel):
    name: str
    learned_count: int
    total_count: int
