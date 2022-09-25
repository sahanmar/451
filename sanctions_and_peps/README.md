# Folder with Sanctions and PEP lists parsers

`source` directory has raw sanction lists

`parsed` directory contains parsed data

## How to use

### UN sanctions:

[UN list](https://www.un.org/securitycouncil/content/un-sc-consolidated-list)

```
python sanctions/un_parser.py -i "/sanctions_and_peps/source/un.xml" -o "/sanctions_and_peps/parsed/un_parsed.csv"
```

### RU BL PEPs:

The data are scraped from [RuPEP](https://rupep.org/en/persons_list/)

```
python sanctions_and_peps/ru_bl_peps_parser.py -o /sanctions_and_peps/parsed/ru_bl_peps_parsed.csv
```

### All politicians:

The data are scraped from [GitHub](https://raw.githubusercontent.com/everypolitician/everypolitician-data/master/countries.json)

```
python sanctions_and_peps/every_politician_parser.py -i /sanctions_and_peps/source/every_politician.json -o sanctions_and_peps/parsed/
```

The script will automatically scrape the data from the links in the original file what will approximately take 150mb on your disk

### Navalny list:

The parsed data are taken from [OCCRP](https://www.occrp.org/en/daily/16253-navalny-s-foundation-lists-putin-s-6-000-bribe-takers-and-warmongers)

PS! If doesnt work, try the absolute path