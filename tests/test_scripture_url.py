from models import Passage
from scripture_url import build_scripture_url


tests = [
    Passage("Genesis", 37, 1, 24),
    Passage("Matthew", 5, 1, 12),
    Passage("1 Nephi", 3, 1, 10),
    Passage("Doctrine and Covenants", 76, 1, 10),
    Passage("Articles of Faith", 1, 1, 13),
    Passage("Joseph Smith—History", 1, 1, 20),
]


for passage in tests:
    print(
        passage.book,
        "=>",
        build_scripture_url([passage])
    )