"""Reverso Conjugation (conjugator.reverso.net) API for Python"""

import json
from collections import namedtuple
from typing import Generator

import requests
from bs4 import BeautifulSoup
import re

__all__ = ["ReversoConjugationAPI"]

HEADERS = {"User-Agent": "Mozilla/5.0",
           "Content-Type": "application/json; charset=UTF-8"
           }

Conjugation = namedtuple("Conjugation", ("verb", "conjugation", "extra", "tense", "mode"))

class ReversoConjugationAPI(object):
    """Class for Reverso Conjugation API (https://conjugator.reverso.net/)

    Attributes:
        supported_langs
        verb
        lang

    Methods:
        get_conjugations()
    """
    def __init__(self, verb="parler", lang="French"):
        self.supported_langs = self.__get_supported_langs()
        self.verb = verb
        self.lang = lang
    
    def __repr__(self) -> str:
        return ("ReversoConjugationAPI({0.verb!r}, {0.lang!r})").format(self)

    def __eq__(self, other) -> bool:
        if not isinstance(other, ReversoConjugationAPI):
            return False

        for attr in ("verb", "lang"):
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True

    @staticmethod
    def __get_supported_langs() -> dict:
        supported_langs = {}

        response = requests.get("https://conjugator.reverso.net/conjugation-english.html",
                                headers=HEADERS)

        soup = BeautifulSoup(response.content, features="lxml")

        selector = soup.find("div", class_="select-wrap")
        
        dd_lis = selector.find(class_="dropdown").find_all("li")
        langs = [li.string for li in dd_lis]
        langs = [lang for lang in langs if isinstance(lang, str)]
        attribute = "lang"
        supported_langs[attribute] = tuple(langs)
        return supported_langs

    @property
    def verb(self) -> str:
        return self._verb

    @property
    def lang(self) -> str:
        return self._lang


    def get_conjugations(self) -> Generator[Conjugation, None, None]:
        """
        Yields all available conjugations for the word.

        Yields:
             Conjugation namedtuples.
        """
        url = 'https://conjugator.reverso.net/conjugation-%s-verb-%s.html' % (self._lang, self._verb)
        response = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(response.content, features="lxml")
        verb = soup.find(class_='targetted-word-transl').string
        tenses = soup.find_all(class_='wrap-verbs-listing')

        for t in tenses:
            mode = t.find_previous(class_='word-wrap-title').find('h4').string
            tense = t.previous_sibling.string
            forms = t.find_all('li')
            for li in forms:
                i = li.find('i', class_='verbtxt')
                conjugation = i.string
                extras = []
                i = i.previous_sibling
                while i is not None:
                    extras.append(i.string.strip())
                    i = i.previous_sibling
                extra = ' '.join(reversed(extras))
                extra = re.sub('\' ([aeiou])','\'\\1', extra)
                yield Conjugation(verb, conjugation, extra, tense, mode)


    @verb.setter
    def verb(self, value) -> None:
        self._verb = str(value)


    @lang.setter
    def lang(self, value) -> None:
        value = str(value)

        if value not in self.supported_langs["lang"]:
            raise ValueError(f"{value!r} language is not supported")

        self._lang = value
