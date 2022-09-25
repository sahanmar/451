# 451 Corporate Risk Miner Datasets used:

## Datasets/Data Sources Used:

UKCH Company House Datasets

- UKCH Company Dataset, downloaded from: http://download.companieshouse.gov.uk/en_output.html 
- UKCH PSC Company Dataset, downloaded from: http://download.companieshouse.gov.uk/en_pscdata.html
- UKCH Officers Dataset, scraped from: https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/reference/officers/list
- Every politician, downloaded from: https://everypolitician.org/countries.html
- Russian peps, downloaded from: https://rupep.org/ru/persons_list/

## Input Schema:
Every entry in every dataset, gets assigned a unique `mention_id` that is a concatenation of a dataset and a row.

### UK CH Company Dataset is consumed as company_df with following columns: 
#### `company_df`
- company_number
- company_name
- country
- industry_code
- address

### UK CH PSC Company Dataset is consumed by splitting people and company owners apart:

#### `psc_company_df`:
- name
- combined_address 
- kind
- company_number
- psc_derived_company_number (this is the company_house id of the owning entity)

#### `psc_company_df`:
- name 
- name_elements_middle_name 
- name_elements_forename 
- name_elements_surname
- nationality 
- address_postal_code 
- date_of_birth_year 
- date_of_birth_month
- company_number

### UK CH Company Officers:
#### `officer_df`:
- forenames 
- surname 
- nationality
- yob 
- mob
- appointment_role
- post_town
- postal_code
- country
