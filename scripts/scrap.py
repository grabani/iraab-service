import json
import re
from urllib.request import urlopen

import convert_numbers
from bs4 import BeautifulSoup


def convert_arabic_to_english_numbers(number):
    return int(convert_numbers.arabic_to_english(number))


def convert_english_to_arabic_numbers(number):
    return str(convert_numbers.english_to_arabic(number))


def process_text(text):
    parsed_text = {}

    splitted_text = text.split('[سورة')[1:]
    remove_rx1 = re.compile(r'الإعراب المفصل لكتاب الله المرتل - جـ \d*\(ص: \d*\)')
    remove_rx2 = re.compile(r'\n ‌‌إعراب سورة ([\u0621-\u064A0-9 ]*)')
    for ayah in splitted_text:
        ayah = re.sub(remove_rx1, '', ayah.strip())  # removing the title
        ayah = re.sub(remove_rx2, '', ayah.strip())  # removing the title
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

    print(parsed_text)
    return parsed_text


def process_005(text):
    parsed_text = {}

    rx = re.compile(
        r'\(*[\u0621-\u064A0-9 \u064B-\u0652 \u0660-\u0669]+\)* *\** \{ *[\u0621-\u064A0-9 \u064B-\u0652 \u0660-\u0669]+ \(*[\u0621-\u064A0-9 \u064B-\u0652 \u0660-\u0669]+\)* *\} *\**')
    splitted_text = re.split(rx, text)[1:]
    ayat_text = re.findall(rx, text)
    remove_rx1 = re.compile(r'الإعراب المفصل لكتاب الله المرتل - جـ \d*\(ص: \d*\)')
    remove_rx2 = re.compile(r'\n ‌‌إعراب سورة ([\u0621-\u064A0-9 ]*)')
    surah_number = 10
    for i,ayah in enumerate(splitted_text):
        ayah = re.sub(remove_rx1, '', ayah.strip())  # removing the title
        ayah = re.sub(remove_rx2, '', ayah.strip())  # removing the title
        rx = re.compile(r'[\u0660-\u0669]+')
        ayah_text = ayat_text[i]
        num = re.findall(rx, ayah_text)
        ayah_number = num[0]
        iraabs = ayah.split('•')
        iraabs = iraabs[1:]
        ayah_irab = {}
        for irab in iraabs:
            irab_head = irab.split(':')[0]
            irab_body = irab[irab.find(':') + 1:]
            ayah_irab.update({irab_head: irab_body})
        surah_num = convert_english_to_arabic_numbers(surah_number)
        parsed_text.setdefault(surah_num, {}).setdefault(ayah_number, [])
        parsed_text[surah_num][ayah_number].append(ayah_text)
        parsed_text[surah_num][ayah_number].append(ayah_irab)
        if (surah_number == 10 and ayah_number == convert_english_to_arabic_numbers(109)) or (
                surah_number == 11 and ayah_number == convert_english_to_arabic_numbers(123)) or (
                surah_number == 12 and ayah_number == convert_english_to_arabic_numbers(111)) or (
                surah_number == 13 and ayah_number == convert_english_to_arabic_numbers(43)):
            surah_number = surah_number + 1

    print(parsed_text)
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
    print(text)
    return text


if __name__ == '__main__':
    htm_path = '../data/005.htm'

    text = extract_text_from_path(htm_path)

    parsed_text = process_005(text)

    json_out_file = 'out/005.htm.json'
    with open(json_out_file, 'w', encoding='utf-8') as f:
        json.dump(parsed_text, f, ensure_ascii=False)
