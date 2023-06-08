from enum import Enum

__all__ = ["Category"]

class Category(Enum):
    MUSIC: str = "music"
    UTILITY: str = "utility"
    GAMES: str = "games"
    STATISTICS: str = "stats"
    POLL: str = "poll"
    TELEGRAM: str = "Telegram"
    FILES: str = "file"
    FUN: str = "entertainment"
    INFO: str = "info"
    NOTIFICATION: str = "notifications"
    MANAGING: str = "manager"
    MEDIA: str = "media"