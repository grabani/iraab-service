import json
import os

from scripts.scrap import extract_text_from_path, process_text

if __name__ == '__main__':
    collected = {}
    for root, dirs, files in os.walk("out"):
        for file in files:
            with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                text = ''.join(f.readlines())
                loaded = json.loads(text)
                collected.update(loaded)

    with open('out.json', 'w', encoding='utf-8') as f:
        json.dump(collected, f, ensure_ascii=False)
