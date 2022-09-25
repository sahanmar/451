# 451 Corporate Risk Miner

## Team Members
Elena Dulskyte [linkedin](https://www.linkedin.com/in/elena-dulskyte-50b83aa2/), Senior Data Scientist at ComplyAdvantage

Marko Sahan [github](http://github.com/sahanmar) [linkedin](https://www.linkedin.com/in/msahan/), Machine Learning Engineer at ComplyAdvantage

Peter Zatka-Haas [github](http://github.com/peterzh) [linkedin](https://www.linkedin.com/in/peterzatkahaas), Data Scientist at ComplyAdvantage

## Tool Description

Financial crime journalists need to dig through complex corporate ownership databases (i.e. databases of companies and the people/companies that control those companies) in order to find associations to criminal activity. They face several problems along the way:
1. It is difficult to search across multiple publicly-available databases (UK Companies House, Sanction lists, ICIJ Leaks, VK)
2. There are multiple ‘risk signatures’ associated with criminal activity (e.g. Cyclical or long-chain ownership, links to sanctions, etc) and different journalists prioritise different kinds of signatures in their investigation
3. The number of corporate networks is overwhelming, and so it is hard to prioritise which corporate ownership structures are more ‘risky’ than others

451 Corporate Risk Miner allows a user to navigate over different corporate ownership networks extracted from UK Companies House (UKCH) to identify and visualise those exhibiting risk signatures associated with financial crime. Example risk signatures include:
* Cyclic ownership: Circular company ownership (e.g. Company A owns Company B which owns Company C which owns Company A)
* Long-chain ownership: Long chains of corporate ownership (e.g. Person A controls company A. Company A is an officer for Company B. Company B is an officer of company C. etc)
* Links to tax havens: Corporate networks which involve companies/people associated with tax haven or secrecy jurisdictions
* Presence of proxy directors: Proxy directors are individual people who are registered as a company director on paper but who are likely never involved in the running of the business.
* Links to sanctioned entities: Official sanctioned people or companies, from sources such as the UN Sanctions List.
* Links to politically-exposed persons (PEPs)
* Links to disqualified directors

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

4. Download dataset from XXXX to `<root dir>/data`

5. Start the streamlit app
```
streamlit run app/app.py
```

6. On your web browser, load [http://localhost:8501](http://localhost:8501)

## Usage

TBD

## Additional Information
This section includes any additional information that you want to mention about the tool, including:
- Potential next steps for the tool (i.e. what you would implement if you had more time)
- Any limitations of the current implementation of the tool
- Motivation for design/architecture decisions

### Limitations
* Limited to cliques of ??? hop distance owing to space limitation
* Cyclicity calculation assumes an undirected graph to save computational time. This could be improved by taking into account specific directions of ownership.
* Entity resolution for company/people entities could be improved
* Graph visualisation for large corporate networks can be too cluttered to be useful. 

### Potential next steps
* Expand to corporate ownership databases outside of the UK, for example using OpenCorporates data.
* Incorporate more external data sources identifying criminal or potentially-criminal activity for companies and people.
* Add an ability to filter based on a custom list of people/companies, explain.......
