import json
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup


def process_text(text):
    parsed_text = {}

    # first up, clean the introductory text
    # while(text.find('[سورة')):
    #     first_sura_idx = text.find('[سورة')
    #     if first_sura_idx == -1: # not found
    #         return parsed_text
    #     else:
    #         text = text[first_sura_idx:]
    #         sura_number = 0
    #         verse_number = 0
    #
    splitted_text = text.split('[سورة')[1:]
    remove_rx = re.compile(r'الإعراب المفصل لكتاب الله المرتل - جـ 1\(ص: \d*\)')
    for ayah in splitted_text:
        re.sub(remove_rx, '', ayah)  # removing the title
        rx = re.compile(r'(\d+)')
        num = re.findall(rx, ayah)
        surah_number = num[0]
        ayah_number = num[1]
        iraabs = ayah.split('•')
        ayah_text = iraabs[0].split(']')[1]
        iraabs = iraabs[1:]
        ayah_irab = {}
        for irab in iraabs:
            irab_head = irab.split(':')[0]
            irab_body = irab[irab.find(':') + 1:]
            ayah_irab.update({irab_head: irab_body})
        parsed_text.setdefault(surah_number, {}).setdefault(ayah_number, [])
        parsed_text[surah_number][ayah_number].append(ayah_text)
        parsed_text[surah_number][ayah_number].append(ayah_irab)

    return parsed_text


def extract_text_from_path(htm_path):
    with open(htm_path, 'r') as file:
        html = file.readlines()
    soup = BeautifulSoup(''.join(html), features="html.parser")
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    # print(text)
    return text


if __name__ == '__main__':
    htm_path = '../data/001.htm'

    text = extract_text_from_path(htm_path)

    parsed_text = process_text(text)

    json_out_file = '../data/001.json'
    with open(json_out_file, 'w', encoding='utf-8') as f:
        json.dump(parsed_text, f, ensure_ascii=False)
