import requests


def download_lesson(url: str) -> str:
    """
    Downloads the HTML for a lesson page.

    Parameters
    ----------
    url : str
        Full lesson URL.

    Returns
    -------
    str
        HTML contents.

    Raises
    ------
    Exception
        If the page cannot be downloaded.
    """

    try:
        response = requests.get(url, timeout=15)

        response.raise_for_status()

        response.encoding = "utf-8"
        return response.text

    except requests.RequestException as e:
        raise Exception(f"Unable to download lesson page.\n{e}")