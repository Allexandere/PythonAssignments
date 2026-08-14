from pathlib import Path


def init():    
    BASE_DIR = Path(__file__).parent
    text_file = BASE_DIR / "junk.txt"

    junk_text = text_file.read_text(encoding="utf-8")
    
    print("Total number of lines: " + str(len(junk_text.splitlines())))
    
    junk_text += "text file nanalyssis"
    junk_text = junk_text.upper()
    
    new_text_file = BASE_DIR / "junk2.txt"
    new_text_file.write_text(junk_text, encoding="utf-8")

if __name__ == "__main__":
    init()