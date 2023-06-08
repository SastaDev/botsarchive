from dataclasses import dataclass

__all__ = ["Bot"]

@dataclass
class Bot:
    id: int
    name: str
    username: str
    description: str
    warn: bool
    msg: str
    category: list
    groups: bool
    inline: bool
    developer_id: int
    stars: int
    votes: int
    vote: float
    tags: list
    languages: str
    offline: bool
    photo: bool
    photo_url: str = None