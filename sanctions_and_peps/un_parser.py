import argparse
import csv

from lxml import etree

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True)
    parser.add_argument("-o", "--out", type=str, required=True)
    return parser.parse_args()

def to_str(s):
    if isinstance(s, bytes):
        return s.decode()
    return s


def extract_value_elems(element):
    if (element.text or "").strip():
        raise Exception("Value field should not contain any text")
    for c in element:
        if c.tag != "VALUE":
            raise Exception(f"Invalid tag for value {c.tag}")
    return list(element)

def extract_values(element):
    values = extract_value_elems(element)
    return [x for x in (to_str(value.text) for value in values) if x is not None]


def extract_values_from_single_element(elements):
    return extract_values(elements[0])

def single_optional_text_element(items):
    text = (items[0].text or "").strip()
    if text:
        return to_str(text)
    return None

def non_empty_text(element):
    text = (element.text or "").strip()
    if isinstance(text, bytes):
        return text.decode()
    return text

def element_to_dict(item):
    d = {}
    for c in item.iterchildren():
        d.setdefault(c.tag, []).append(c)
    return d

def single_text_element(items):
    return non_empty_text(items[0])

def process_person(individual):
    names = [None, None, None, None]
    nationalities = [None, None]
    occupation = None
    for tag, items in element_to_dict(individual).items():
        if tag == "FIRST_NAME":
            names[0] = single_text_element(items)
        elif tag == "SECOND_NAME":
            names[1] = single_optional_text_element(items)
        elif tag == "THIRD_NAME":
            names[2] = single_optional_text_element(items)
        elif tag == "FOURTH_NAME":
            names[3] = single_optional_text_element(items)
        elif tag == "UN_LIST_TYPE":
                un_list_type = single_text_element(items)
        elif tag == "NATIONALITY":
                nationalities[0] = extract_values_from_single_element(items)[0]
        elif tag == "NATIONALITY2":
            nationalities[1] = extract_values_from_single_element(items)[0]
        elif tag == "DESIGNATION":
                occupation = extract_values_from_single_element(items)[0]
        elif tag == "REFERENCE_NUMBER":
                ref_num = single_text_element(items)
    return [ref_num, "INDIVIDUAL"] + names + [un_list_type, occupation] + nationalities


def process_entity(entity):
    names = [None, None, None, None]
    for tag, items in element_to_dict(entity).items():
        if tag == "FIRST_NAME":
            for item in items:
                names[0] = to_str(item.text).strip()
        elif tag == "UN_LIST_TYPE":
                un_list_type = single_text_element(items)
        elif tag == "REFERENCE_NUMBER":
                ref_num = single_text_element(items)
    return [ref_num, "ENTITY"] + names + [un_list_type, None, None, None,]


def main():
    args = parse_args()
    entities = []
    with open(args.input, "rb") as f:
        xml: etree._Element = etree.fromstring(f.read())
    for items in xml:
        for item in items:
            tag = item.tag
            if tag == "INDIVIDUAL":
                entities.append(process_person(item))
            elif tag == "ENTITY":
                entities.append(process_entity(item))
    with open(args.out, "w") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "REFERENCE_NUMBER", 
                "ENTITY_TYPE", 
                "FIRST_NAME", 
                "SECOND_NAME", 
                "THIRD_NAME", 
                "FOURTH_NAME",
                "UN_LIST_TYPE",
                "DESIGNATION",
                "NATIONALITY",
                "NATIONALITY2"
            ]
        )
        for row in entities:
            writer.writerow(row)

if __name__=="__main__":
    main()