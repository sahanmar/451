import requests
import re
import csv
import argparse

from bs4 import BeautifulSoup


NAME_PARSER = re.compile(r"\((.*?)\)")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--out", type=str, required=True)
    return parser.parse_args()


def parse_name(compound_name):
    found_name_en = NAME_PARSER.findall(compound_name)
    if found_name_en:
        name_en = found_name_en[0].strip()
    else:
        name_en = None
    name_ru = compound_name.split("(")[0].strip()
    return name_en, name_ru


def main():
    args = parse_args()

    url = "https://rupep.org/en/persons_list/"
    
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, "html.parser")
    
    data = soup.find("table", "everything quicksilver_target").findAll("tr")

    header  = [
        "NAME_EN",
        "NAME_RU", 
        "DOB", 
        "TAXPAYER_NUM", 
        "CATEGORY", 
        "LAST_POSITION_EN"
        "LAST_POSITION_RU"
    ]

    output = []
    for record in data[1:]:
        parsed_row = [None, None, None, None, None, None, ]
        for i, column in enumerate(record.findAll("td")):
            column = column.text.strip()
            # parsed names
            if i == 0:
                name_en, name_ru = parse_name(column)
                parsed_row[0] = name_en
                parsed_row[1] = name_ru
            # DOB
            elif i == 1:
                if column:
                    parsed_row[2] = column
            # taxpayer num
            elif i == 2:
                if column:
                    parsed_row[3] = column
            # category
            elif i == 3:
                parsed_row[4] = column
            # parsed position names
            elif i == 4:
                if column:
                    name_en, name_ru = parse_name(column)
                    parsed_row[4] = name_en
                    parsed_row[5] = name_ru

        output.append(parsed_row)

    with open(args.out, "w") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in output:
            writer.writerow(row)


if __name__=="__main__":
    main()