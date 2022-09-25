# 451 Corporate Risk Miner

## Team Members
Elena Dulskyte [github](https://github.com/ElenaDulskyte) [linkedin](https://www.linkedin.com/in/elena-dulskyte-50b83aa2/)

Marko Sahan [github](http://github.com/sahanmar) [linkedin](https://www.linkedin.com/in/msahan/)

Peter Zatka-Haas [github](http://github.com/peterzh) [linkedin](https://www.linkedin.com/in/peterzatkahaas)

## Tool Description

Financial crime journalists need to dig through complex corporate ownership databases (i.e. databases of companies and the people/companies that control those companies) in order to find associations to criminal activity. They face several problems along the way:
1. It is difficult to search across multiple publicly-available databases (UK Companies House, Sanction lists, ICIJ Leaks, VK)
2. There are multiple ‘risk signatures’ associated with criminal activity (e.g. Cyclical or long-chain ownership, links to sanctions, etc) and different journalists prioritise different kinds of signatures in their investigation
3. The number of corporate networks is overwhelming, and so it is hard to prioritise which corporate ownership structures are more ‘risky’ than others

451 Corporate Risk Miner allows a user to navigate over different corporate ownership networks extracted from UK Companies House (UKCH) to identify and visualise those exhibiting risk signatures associated with financial crime. Example risk signatures include:
* Cyclic ownership: measure of network interconnectedness (e.g. Company A owns Company B which owns Company C which owns Company A, or case when the same people direct multiple companies.)
* Links to tax havens: Corporate networks which involve companies/people associated with tax haven or secrecy jurisdictions
* Presence of proxy directors: Proxy directors are entities that have links to more than 50 companies.
* Links to politically-exposed persons (PEPs)
* Links to russian politicians


The user can customise the relative importance of each risk signature for their search. The app then computes a **total risk score** for each corporate network in UKCH, and outlines the details of the most high-risk networks. The user can export these network results as a .csv file for later viewing. 

## Installation

1. Make sure you have Python version 3.8 or greater installed

2. Download the tool's repository using the command:
```
git clone https://github.com/sahanmar/451
```

3. Move to the tool's directory and install the tool
```
cd 451
pip install -r requirements.txt
```

4. Start the streamlit app
```
streamlit run app/app.py
```

5. On your web browser, load [http://localhost:8501](http://localhost:8501)

## Usage

- Access the app online.

Data cache can either be:

- Downloaded from <a href="https://drive.google.com/drive/folders/15I2-spww_5ZG6tzslLyU4gGwb3zDNZU-?usp=sharing" target="_blank">GoogleDrive.</a>
  (Then unzipped and stored in `/data` folder.)

- Recomputed with fresh UK Company House Downloads. Follow README and notebook in `/data_cache/` folder.

## Additional Information

### Data

In this project we used UK Company House Datasets. All information regarding the dataset, input schema and data processing can be found in [data_cache](https://github.com/sahanmar/451/tree/main/data_cache).

#### Data enrichment
The original UKCH data did not provide pep information. Hence, the data wes enriched with the additional information from the publicly available external datasets. We have scraped [UN sanctions](https://www.un.org/securitycouncil/content/un-sc-consolidated-list), [Russian and Belorussian PEPs](https://rupep.org/en/persons_list/) and [all politicians dataset](https://raw.githubusercontent.com/everypolitician/everypolitician-data/master/countries.json). The scrapers, parsers and README can be found in [sanctions_and_peps](https://github.com/sahanmar/451/tree/main/sanctions_and_peps) directory.
In the final version of the app, Russian rupep.org and EveryPolitician.org were used.

### Limitations
* If a user wants to refresh the cached data with the latest UKCH datasets, it would need to be downloaded from UKCH company house and formatted as per data_schema/README instructions.
* Limited to neighbourhood of 2 hop distance, when network is parto of a Giant Ownership component.
* Cyclicity calculation assumes an undirected graph to save computational time. This could be improved by taking into account specific directions of ownership.
* Entity resolution for company/people entities could be improved. Currently linking is done on name+yob+mob.
* Graph visualisation for large corporate networks can be too cluttered to be useful. 

### Potential next steps
* Expand to corporate ownership databases outside of the UK, for example using OpenCorporates data.
* Incorporate more external data sources identifying criminal or potentially-criminal activity for companies and people.
* Allow user to input custom lists.
