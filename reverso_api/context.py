"""Reverso Context (context.reverso.net) API for Python"""

import json
from collections import namedtuple
from typing import Generator

import requests
from bs4 import BeautifulSoup

__all__ = ["ReversoContextAPI", "WordUsageContext", "Translation", "InflectedForm"]

HEADERS = {"User-Agent": "Mozilla/5.0",
           "Content-Type": "application/json; charset=UTF-8"
           }

WordUsageContext = namedtuple("WordUsageContext",
                              ("text", "highlighted"))

Translation = namedtuple("Translation",
                         ("source_word", "translation", "frequency", "part_of_speech", "inflected_forms"))

InflectedForm = namedtuple("InflectedForm",
                           ("translation", "frequency"))


class ReversoContextAPI(object):
    """Class for Reverso Context API (https://context.reverso.net/)

    Attributes:
        supported_langs
        source_text
        target_text
        source_lang
        target_lang
        total_pages
    
    Methods:
        get_translations()
        get_examples()
        swap_langs()
    """

    def __init__(self,
                 source_text="пример",
                 target_text="",
                 source_lang="ru",
                 target_lang="en"):

        self.__data = dict.fromkeys(("source_text", "target_text", "source_lang", "target_lang"))
        self.__data_ismodified = True
        self.__total_pages = None

        # FIXME: make self.supported_langs read-only
        self.supported_langs = self.__fetch_supported_langs()

        self.source_text, self.target_text = source_text, target_text
        self.source_lang, self.target_lang = source_lang, target_lang

    def __repr__(self) -> str:
        return ("ReversoContextAPI({0.source_text!r}, {0.target_text!r}, "
                "{0.source_lang!r}, {0.target_lang!r})").format(self)

    def __eq__(self, other) -> bool:
        if isinstance(other, ReversoContextAPI):
            return self.__data == other._ReversoContextAPI__data
        return False

    def __fetch_supported_langs(self) -> dict:
        supported_langs = {}

        response = requests.get("https://context.reverso.net/translation/",
                                headers=HEADERS)

        soup = BeautifulSoup(response.content, features="lxml")

        src_selector = soup.find("div", id="src-selector")
        trg_selector = soup.find("div", id="trg-selector")

        for selector, attribute in ((src_selector, "source_lang"),
                                    (trg_selector, "target_lang")):
            dd_spans = selector.find(class_="drop-down").find_all("span")
            langs = [span.get("data-value") for span in dd_spans]
            langs = [lang for lang in langs
                     if isinstance(lang, str) and len(lang) == 2]

            supported_langs[attribute] = tuple(langs)

        return supported_langs

    @property
    def source_text(self) -> str:
        return self.__data["source_text"]

    @property
    def target_text(self) -> str:
        return self.__data["target_text"]

    @property
    def source_lang(self) -> str:
        return self.__data["source_lang"]

    @property
    def target_lang(self) -> str:
        return self.__data["target_lang"]

    @property
    def total_pages(self) -> int:
        if self.__data_ismodified:
            response = requests.post("https://context.reverso.net/bst-query-service",
                                     headers=HEADERS,
                                     data=json.dumps(self.__data))

            total_pages = response.json()["npages"]

            if not isinstance(total_pages, int):
                try:
                    total_pages = int(total_pages)
                except ValueError:
                    raise ValueError('"npages" in the response cannot be interpreted as an integer')
                if total_pages < 0:
                    raise ValueError('"npages" in the response is a negative number')

            self.__total_pages = total_pages
            self.__data_ismodified = False

        return self.__total_pages

    def get_translations(self) -> Generator[Translation, None, None]:
        """Yields all available translations for the word
        On the Reverso.Context website, it looks like a row
        with words/short phrases just before the examples.

        Yields:
             Translation namedtuples.

        """

        response = requests.post("https://context.reverso.net/bst-query-service",
                                 headers=HEADERS,
                                 data=json.dumps(self.__data))
        translations_json = response.json()["dictionary_entry_list"]

        for translation_json in translations_json:
            translation = translation_json["term"]
            frequency = translation_json["alignFreq"]
            part_of_speech = translation_json["pos"]

            inflected_forms = tuple(InflectedForm(form["term"], form["alignFreq"])
                                    for form in translation_json["inflectedForms"])

            yield Translation(self.__data["source_text"],
                              translation, frequency, part_of_speech,
                              inflected_forms)

    def get_examples(self) -> Generator[tuple, None, None]:
        """A generator that gets words' usage examples pairs from server pair by pair.

        Note:
            Don't try to get all usage examples at one time if there are more than 5 pages (see the total_pages attribute). It
            may take a long time to complete because it will be necessary to connect to the server as many times as there are pages exist.
            Just get the usage examples one by one as they are being fetched.

        Yields:
            Tuples with two WordUsageContext namedtuples (for source and target text and highlighted indexes)

        """

        def find_highlighted_idxs(soup, tag="em") -> tuple:
            """Finds indexes of the parts of the soup surrounded by a particular HTML tag
            relatively to the soup without the tag.

            Example:
                soup = BeautifulSoup("<em>This</em> is <em>a sample</em> string")
                tag = "em"
                Returns: [(0, 4), (8, 16)]

            Args:
                soup: The BeautifulSoup's soup.
                tag: The HTML tag, which surrounds the parts of the soup.

            Returns:
                  A list of the tuples, which contain start and end indexes of the soup parts,
                  surrounded by tags.

            """

            # source: https://stackoverflow.com/a/62027247/8661764

            cur, idxs = 0, []
            for t in soup.find_all(text=True):
                if t.parent.name == tag:
                    idxs.append((cur, cur + len(t)))
                cur += len(t)
            return tuple(idxs)

        for npage in range(1, self.total_pages + 1):
            self.__data["npage"] = npage

            response = requests.post("https://context.reverso.net/bst-query-service",
                                     headers=HEADERS,
                                     data=json.dumps(self.__data))
            examples_json = response.json()["list"]

            for example in examples_json:
                source = BeautifulSoup(example["s_text"], features="lxml")
                target = BeautifulSoup(example["t_text"], features="lxml")
                yield (WordUsageContext(source.text, find_highlighted_idxs(source)),
                       WordUsageContext(target.text, find_highlighted_idxs(target)))

    @source_text.setter
    def source_text(self, value) -> None:
        self.__data["source_text"] = str(value)
        self.__data_ismodified = True

    @target_text.setter
    def target_text(self, value) -> None:
        self.__data["target_text"] = str(value)
        self.__data_ismodified = True

    @source_lang.setter
    def source_lang(self, value) -> None:
        value = str(value)

        if value not in self.supported_langs["source_lang"]:
            raise ValueError(f'"{value}" source language is not supported')

        if value == self.source_lang:
            raise ValueError(f"source language cannot be equal to the target language")

        self.__data["source_lang"] = value
        self.__data_ismodified = True

    @target_lang.setter
    def target_lang(self, value) -> None:
        value = str(value)

        if value not in self.supported_langs["target_lang"]:
            raise ValueError(f'"{value}" target language is not supported')

        if value == self.source_lang:
            raise ValueError(f"target language cannot be equal to the source language")

        self.__data["target_lang"] = value
        self.__data_ismodified = True

    def swap_langs(self) -> None:
        self.__data["source_lang"], self.__data["target_lang"] = self.__data["target_lang"], \
                                                                 self.__data["source_lang"]
        self.__data_ismodified = True
