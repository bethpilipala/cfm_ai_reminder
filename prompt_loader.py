from pathlib import Path


PROMPTS_DIRECTORY = Path("prompts")


def load_prompt(name: str) -> str:
    """
    Loads a prompt from the prompts directory.
    """

    prompt_path = PROMPTS_DIRECTORY / f"{name}.txt"

    with open(prompt_path, encoding="utf-8") as file:
        return file.read()