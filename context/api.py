from pprint import pprint
import requests
import json

from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json; charset=UTF-8"
}

class ReversoContextAPI(object):
    
    def __init__(self, source_text="я люблю кошек", target_text="", source_lang="ru", target_lang="en"):
        self.data = {
            "source_text": source_text,
            "target_text": target_text,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "npage": 1,
            "mode": 0
            }
        self.page_count = requests.post("https://context.reverso.net/bst-query-service", headers=HEADERS, data=json.dumps(self.data)).json()["npages"]

    def get_page(self, npage):
        data = self.data.copy()
        data["npage"] = npage
        return requests.post("https://context.reverso.net/bst-query-service", headers=HEADERS, data=json.dumps(data)).json()["list"]

    def get_results_pair_by_pair(self):
        for npage in range(1, self.page_count + 1):
            for word in self.get_page(npage):
                yield (BeautifulSoup(word["s_text"]).text, BeautifulSoup(word["t_text"]).text)

    def get_results(self):
        return [pair for pair in self.get_results_pair_by_pair()]
        
if __name__ == "__main__":
    api = ReversoContextAPI(
           input("Enter the source text to search... "),
           input("Enter the target text to search (optional)... "),
           input("Enter the source language code... "),
           input("Enter the target language code... ")
           )
    results = api.get_results_pair_by_pair()
    for pair in results:
        print(pair[0], "=", pair[1])
