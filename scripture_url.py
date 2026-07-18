from models import Passage


BASE_URL = (
    "https://www.churchofjesuschrist.org/"
    "study/scriptures"
)


SCRIPTURE_BOOKS = {
    # Old Testament
    "Genesis": ("ot", "gen"),
    "Exodus": ("ot", "ex"),
    "Leviticus": ("ot", "lev"),
    "Numbers": ("ot", "num"),
    "Deuteronomy": ("ot", "deut"),
    "Joshua": ("ot", "josh"),
    "Judges": ("ot", "judg"),
    "Ruth": ("ot", "ruth"),
    "1 Samuel": ("ot", "1-sam"),
    "2 Samuel": ("ot", "2-sam"),
    "1 Kings": ("ot", "1-kgs"),
    "2 Kings": ("ot", "2-kgs"),
    "1 Chronicles": ("ot", "1-chr"),
    "2 Chronicles": ("ot", "2-chr"),
    "Ezra": ("ot", "ezra"),
    "Nehemiah": ("ot", "neh"),
    "Esther": ("ot", "esth"),
    "Job": ("ot", "job"),
    "Psalms": ("ot", "ps"),
    "Proverbs": ("ot", "prov"),
    "Ecclesiastes": ("ot", "eccl"),
    "Song of Solomon": ("ot", "song"),
    "Isaiah": ("ot", "isa"),
    "Jeremiah": ("ot", "jer"),
    "Lamentations": ("ot", "lam"),
    "Ezekiel": ("ot", "ezek"),
    "Daniel": ("ot", "dan"),
    "Hosea": ("ot", "hosea"),
    "Joel": ("ot", "joel"),
    "Amos": ("ot", "amos"),
    "Obadiah": ("ot", "obad"),
    "Jonah": ("ot", "jonah"),
    "Micah": ("ot", "micah"),
    "Nahum": ("ot", "nahum"),
    "Habakkuk": ("ot", "hab"),
    "Zephaniah": ("ot", "zeph"),
    "Haggai": ("ot", "hag"),
    "Zechariah": ("ot", "zech"),
    "Malachi": ("ot", "mal"),

    # New Testament
    "Matthew": ("nt", "matt"),
    "Mark": ("nt", "mark"),
    "Luke": ("nt", "luke"),
    "John": ("nt", "john"),
    "Acts": ("nt", "acts"),
    "Romans": ("nt", "rom"),
    "1 Corinthians": ("nt", "1-cor"),
    "2 Corinthians": ("nt", "2-cor"),
    "Galatians": ("nt", "gal"),
    "Ephesians": ("nt", "eph"),
    "Philippians": ("nt", "phil"),
    "Colossians": ("nt", "col"),
    "1 Thessalonians": ("nt", "1-thes"),
    "2 Thessalonians": ("nt", "2-thes"),
    "1 Timothy": ("nt", "1-tim"),
    "2 Timothy": ("nt", "2-tim"),
    "Titus": ("nt", "titus"),
    "Philemon": ("nt", "philem"),
    "Hebrews": ("nt", "heb"),
    "James": ("nt", "james"),
    "1 Peter": ("nt", "1-pet"),
    "2 Peter": ("nt", "2-pet"),
    "1 John": ("nt", "1-jn"),
    "2 John": ("nt", "2-jn"),
    "3 John": ("nt", "3-jn"),
    "Jude": ("nt", "jude"),
    "Revelation": ("nt", "rev"),

    # Book of Mormon
    "1 Nephi": ("bofm", "1-ne"),
    "2 Nephi": ("bofm", "2-ne"),
    "Jacob": ("bofm", "jacob"),
    "Enos": ("bofm", "enos"),
    "Jarom": ("bofm", "jarom"),
    "Omni": ("bofm", "omni"),
    "Words of Mormon": ("bofm", "w-of-m"),
    "Mosiah": ("bofm", "mosiah"),
    "Alma": ("bofm", "alma"),
    "Helaman": ("bofm", "hel"),
    "3 Nephi": ("bofm", "3-ne"),
    "4 Nephi": ("bofm", "4-ne"),
    "Mormon": ("bofm", "morm"),
    "Ether": ("bofm", "ether"),
    "Moroni": ("bofm", "moro"),

    # Doctrine and Covenants
    "Doctrine and Covenants": ("dc-testament", "dc"),

    # Pearl of Great Price
    "Moses": ("pgp", "moses"),
    "Abraham": ("pgp", "abr"),
    "Joseph Smith—Matthew": ("pgp", "js-m"),
    "Joseph Smith—History": ("pgp", "js-h"),
    "Articles of Faith": ("pgp", "a-of-f"),
}


def build_scripture_url(
    passages: list[Passage],
) -> str:
    """
    Builds a Church scripture URL from the first passage.

    If the reading has no passages or the book is unsupported,
    an empty string is returned.
    """

    if not passages:
        return ""

    first = passages[0]

    scripture_info = SCRIPTURE_BOOKS.get(
        first.book
    )

    if scripture_info is None:
        return ""

    collection, slug = scripture_info

    return (
        f"{BASE_URL}/"
        f"{collection}/"
        f"{slug}/"
        f"{first.chapter}"
        "?lang=eng"
    )