from pydantic import BaseModel


class TopicRead(BaseModel):
    id: int
    name: str
    learned_count: int
    total_count: int
