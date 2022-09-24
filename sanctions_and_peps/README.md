## Folder with Sanctions and PEP lists parsers

`source` directory has raw sanction lists (e.g UN and OFAC)

`parsed` directory contains parced data

### How to use

UN sanctions:

```
python sanctions/un_parser.py -i "/sanctions_and_peps/source/un.xml" -o "/sanctions_and_peps/parsed/un_parsed.csv"
```

RU BL PEPs:

The data are scraped from [RuPEP](https://rupep.org/en/persons_list/)

```
python sanctions_and_peps/ru_bl_peps_parser.py -o /sanctions_and_peps/parsed/ru_bl_peps_parsed.csv
```

Navalny list:

The parsed data are taken from [OCCRP](https://www.occrp.org/en/daily/16253-navalny-s-foundation-lists-putin-s-6-000-bribe-takers-and-warmongers)

PS! If doesnt work, try the absolute path