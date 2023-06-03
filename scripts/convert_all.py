import json
import os

from scripts.scrap import extract_text_from_path, process_text

if __name__ == '__main__':
    for root, dirs, files in os.walk("../data"):
        path = root.split(os.sep)
        out_path = os.path.join(os.path.dirname(__file__), 'out')
        os.makedirs(out_path, exist_ok= True)
        print("converting files")
        print((len(path) - 1) * '---', os.path.basename(root))
        for file in files:
            print(len(path) * '---', file)
            filepath = os.path.join(root, file)
            text = extract_text_from_path(filepath)

            parsed_text = process_text(text)

            json_out_file = os.path.join(out_path, f'{os.path.basename(file)}.json')
            with open(json_out_file, 'w', encoding='utf-8') as f:
                json.dump(parsed_text, f, ensure_ascii=False)
