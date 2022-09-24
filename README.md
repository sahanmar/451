# 451 Corporate Risk Miner

## Team Members
Elena Dulskyte [linkedin](https://www.linkedin.com/in/elena-dulskyte-50b83aa2/)

Marko Sahan [github](http://github.com/sahanmar) [linkedin](https://www.linkedin.com/in/msahan/)

Peter Zatka-Haas [github](http://github.com/peterzh) [linkedin](https://www.linkedin.com/in/peterzatkahaas)

## Tool Description

Financial crime journalists need to dig through complex corporate ownership databases (i.e. databases of companies and the people/companies that control those companies) in order to find potentially interesting people/companies related to financial crime. They face several problems along the way:
1. It is difficult to search across multiple publicly-available databases (UK Companies House, ICIJ Leaks, VK)
2. There are multiple ‘risk signatures’ associated with criminal activity (e.g. Cyclical or long-chain ownership, links to sanctions, etc) and different journalists prioritise different kinds of signatures in their investigation.
3. It is hard to prioritise which corporate ownership structures are more ‘risky’ than others
4. It is hard to see the visualise corporate ownership with different risk signals

Corporate Risk Miner is a web app which evaluates different risk signatures of financial crime applied to the UK Companies House (UKCH) corporate ownership networks. These risk signatures include:
* Cyclic ownership: (to explain.....)
* Long-chain ownership: Long chains of corporate ownership (e.g. Person A controls company A. Company A is an officer for Company B. Company B is an officer of company C. etc)
* Links to tax havens: Corporate networks which involve companies/people associated with tax haven jurisdictions
* Multi-jurisdictionness: Corporate networsk which span many jurisdictions
* Presence of proxy directors: Proxy directors are individual people who are registered as a company director but who are likely never involved in the running of the business. These people are often directors for many companies.
* Links to sanctioned entities: Official sanctioned people or companies, from sources such as the UN Sanctions List.
* Links to politically-exposed persons (PEPs)
* Links to disqualified directors

The user can customise the relative 'importance' of each risk signature for their search. For example one user may rate 'cyclic ownership' as a less important feature than 'association with tax havens' in flagging up potentially dodgy corporate networks. One the user chooses their signature preferences, the app generates a **risk score** associated with each corporate network and displays the structure of those networks with the highest risk scores.

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

TBD

## Additional Information
This section includes any additional information that you want to mention about the tool, including:
- Potential next steps for the tool (i.e. what you would implement if you had more time)
- Any limitations of the current implementation of the tool
- Motivation for design/architecture decisions
