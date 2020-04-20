import matplotlib.pyplot as plt
import numpy as np
import requests

url = "https://github.com/nytimes/covid-19-data/blob/master/us-states.csv"

with requests.Session() as s:
    download = s.get(url)

    decoded_content = download.content.decode('utf-8')

print(decoded_content)
