from pathlib import Path

BASE_DIR = Path(__file__).parent

def init():
    text_file = BASE_DIR / "junk.txt"

    junk_text = text_file.read_text(encoding="utf-8")

    print("Total number of lines: " + str(len(junk_text.splitlines())))

    junk_text += "text file nanalyssis"

    new_text_file = BASE_DIR / "junk2.txt"
    new_text_file.write_text(junk_text.upper(), encoding="utf-8")


if __name__ == "__main__":
    init()
