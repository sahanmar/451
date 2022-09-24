## Folder with Sanctions lists parsers

`source` directory has raw sanction lists (e.g UN and OFAC)
`parsed` directory contains parced data

### How to use

UN sanctions

```
python sanctions/un_parser.py -i "/sanctions/source/un.xml" -o "/sanctions/parsed/un_parsed.csv"
```
If doesnt work, try the absolute path