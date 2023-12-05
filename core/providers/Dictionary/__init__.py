from .dictionary_provider import get_word_by_query
from . import dictionary_provider
from .schemas import WordDTO, ImageDTO, SenseDTO

__all__ = [
    "get_word_by_query",
    "WordDTO",
    "ImageDTO",
    "SenseDTO",
    "dictionary_provider",
]
