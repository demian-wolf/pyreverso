from pprint import pprint
import requests
import json

from bs4 import BeautifulSoup


HEADERS = {
    "Connection": "keep-alive",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    "Content-Type": "application/json; charset=UTF-8",
    "Content-Length": "96",
    "Origin": "https://context.reverso.net",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Referer": "https://context.reverso.net/^%^D0^%^BF^%^D0^%^B5^%^D1^%^80^%^D0^%^B5^%^D0^%^B2^%^D0^%^BE^%^D0^%^B4/^%^D0^%^B0^%^D0^%^BD^%^D0^%^B3^%^D0^%^BB^%^D0^%^B8^%^D0^%^B9^%^D1^%^81^%^D0^%^BA^%^D0^%^B8^%^D0^%^B9-^%^D1^%^80^%^D1^%^83^%^D1^%^81^%^D1^%^81^%^D0^%^BA^%^D0^%^B8^%^D0^%^B9/cat",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
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

    def get_results_page_by_page(self):
        for npage in range(1, self.page_count + 1):
            page = self.get_page(npage)
            for word in page:
                yield (BeautifulSoup(word["s_text"]).text, BeautifulSoup(word["t_text"]).text)

    def get_results(self):
        return [pair for pair in self.get_results_page_by_page()]
        
if __name__ == "__main__":
    api = ReversoContextAPI(
           input("Enter the source text to search... "),
           input("Enter the target text to search (optional)... "),
           input("Enter the source language code... "),
           input("Enter the target language code... ")
           )
    results = api.get_results_page_by_page()
    for pair in results:
        print(pair[0], "=", pair[1])
