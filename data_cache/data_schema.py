schema = {
    "every_politician": "/sanctions_and_peps/parsed/politicians_parsed.csv",
    "russian_politician": "/sanctions_and_peps/parsed/ru_bl_peps_parsed.csv",
# Source: UKCH Company house, see schema readme for more details:
    "ukch_company": "/insert_download_folder/ukch_companies.parquet",
    "ukch_officers": "/insert_download_folder/ukch_officers.parquet",
    "ukch_psc_company": "/insert_download_folder/psc_company.parquet",
    "ukch_psc_people": "/insert_download_folder/psc_person.parquet",
# Output locations for stream lit to consume:
    "output_nodes": "/data/networks.parquet",
    "output_edges":  "./data/edges.parque",
    "output_networks": "/data/networks.parquet"
}