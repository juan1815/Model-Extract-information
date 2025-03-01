# Model-Extract-information
This project is Architec's, we develop a model with lengauage python to extract information of files PDF with format A3.

This PDF are 'Gacetas', This Document content information of proyects, entities, dates, etc. The purpose is extract the presentation and proyects with a next range: From 2000 to 2025. 

 
## Create a space-Enviroment
- conda create -m Extraction
- conda activate Extraction

## Install the next libreries
- pip install transformers torch
- python -m spacy dowload es_core_news_sm
- pip install re