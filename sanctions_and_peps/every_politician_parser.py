import argparse
import csv
import json
import urllib.request as request
import pathlib

POLITICIANS_JSON_DIR = "politicians_raw_jsons"
POLITICIANS_PARSED_CSV = "politicians_parsed.csv"

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True)
    parser.add_argument("-o", "--out", type=str, required=True)
    return parser.parse_args()


def download_data(input_path, out_path):
    path_w_jsons = out_path / POLITICIANS_JSON_DIR
    if not path_w_jsons.exists():
        path_w_jsons.mkdir()
    with open(input_path, "r") as f:
        data = json.load(f)
        for country in data:
            country_name = country["name"].lower()
            for i, legislature in enumerate(country["legislatures"]):
                with request.urlopen(legislature["popolo_url"]) as url:
                    names = json.loads(url.read())
                    file_name = f"{country_name}_{i}.json"
                    with open(path_w_jsons / file_name, "w") as json_2_write:
                        json.dump(names, json_2_write)


def parse_person(person_dict):
    return [person_dict["id"], person_dict["name"], person_dict.get("birth_date")]


def extract_entites(path):
    path_w_jsons = path / POLITICIANS_JSON_DIR
    all_politicians = []
    for json_path in path_w_jsons.iterdir():
        with open(json_path, "r") as f:
            data = json.load(f)
        country = json_path.name.split("_")[0]
        persons = [parse_person(person) + [country] for person in data["persons"]]
        # we do not extract data["organizations"] 
        all_politicians.extend(persons)
    return all_politicians

def main():
    args = parse_args()

    path_out = pathlib.Path(args.out)
    if not (path_out / POLITICIANS_JSON_DIR).exists():
        print("Downloading jsons...")
        download_data(pathlib.Path(args.input), pathlib.Path(args.out))

    entities = extract_entites(path_out)

    header = ["ID", "NAME", "DOB", "COUNTRY"]

    with open(path_out / POLITICIANS_PARSED_CSV, "w") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in entities:
            writer.writerow(row)

if __name__=="__main__":
    main()