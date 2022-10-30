import os, re


class SubtitleHandler:
    def __init__(self) -> None:
        pass

    def parse_subtitle_file(file):
        pass


def read_subs_file(path):
    ##!! need saved encoding mappings (sig for spanish friends because '\ufeff' at start)
    with open(file=path, encoding="utf-8-sig") as f:
        file = [line.strip() for line in f.readlines()]


def parse_subs_file(subs_file_raw):
    parsed_subs = []

    for line in subs_file_raw:
        if not re.match(r"(^\d+$)|(\n)|(\d.*--> \d.*)", line):
            parsed_subs.append(line)

    return parsed_subs


def output_text_file(subtitle_lines, output_path):
    ##!! also need encoded output
    number_of_lines = len(subtitle_lines)

    for line_number in range(number_of_lines):
        this_line = subtitle_lines[line_number]
        if line_number < number_of_lines - 1:
            next_line = subtitle_lines[line_number + 1]

        else:
            print(this_line)


if __name__ == "__main__":
    test_path = "C:\Stuff\LanguageRepo\Subs Study\Subtitles\Friends - season 1.es subtitulos\Friends - 1x01 - The One Where Monica Gets A Roommate.es.srt"
    subs_file_raw = read_subs_file(test_path)

    parsed_subs = parse_subs_file(subs_file_raw)

    output_path = "./1x01 Spanish.txt"
    output_text_file(parsed_subs, output_path)
