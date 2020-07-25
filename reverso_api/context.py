"""Reverso Context (context.reverso.net) API for Python"""

from collections import namedtuple
import json

from bs4 import BeautifulSoup
import requests


__all__ = ["ReversoContextAPI", "WordUsageExample", "Translation", "InflectedForm"]

HEADERS = {"User-Agent": "Mozilla/5.0",
           "Content-Type": "application/json; charset=UTF-8"
           }

WordUsageExample = namedtuple("WordUsageExample",
                              ("text", "highlighted"))

Translation = namedtuple("Translation",
                         ("source_word", "translation", "frequency", "part_of_speech", "inflected_forms"))

InflectedForm = namedtuple("InflectedForm",
                           ("translation", "frequency"))


class ReversoContextAPI(object):
    """Class for Reverso Context API (https://voice.reverso.net/)

    Methods:
        get_translations()
        get_examples()

    """

    def __init__(self, source_text="я люблю кошек", target_text="", source_lang="ru", target_lang="en", parser="lxml"):
        self.data = {
            "source_text": source_text,
            "target_text": target_text,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "npage": 1,
        }
        self.parser = parser
        self.page_count = requests.post("https://context.reverso.net/bst-query-service", headers=HEADERS,
                                        data=json.dumps(self.data)).json()["npages"]

    def __repr__(self):
        return "ReversoContextAPI({source_text!r}, {target_text!r}, {source_lang!r}, {target_lang!r}, {parser!r})" \
            .format(parser=self.parser, **self.data)

    def __eq__(self, other):
        def remove_npage(d):
            """Removes the "npage" key from the given dict.

            Args:
                d: given dict

            Returns:
                the given dict without the "npage" key

            """
            return {i: d[i] for i in d if i != "npage"}

        if isinstance(other, ReversoContextAPI):
            return remove_npage(self.data) == remove_npage(other.data) and self.parser == other.parser
        return False

    @staticmethod
    def _find_highlighted_idxs(soup, tag="em"):
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

        cur, idxs = 0, []
        for t in soup.find_all(text=True):
            if t.parent.name == tag:
                idxs.append((cur, cur + len(t)))
            cur += len(t)
        return idxs

    def get_translations(self):
        """Yields all available translations for the word (on the website you can find it just before the examples).

        Yields:
             Translation namedtuples.

        """

        translations_json = requests.post("https://context.reverso.net/bst-query-service", headers=HEADERS,
                                          data=json.dumps(self.data)).json()["dictionary_entry_list"]
        for translation in translations_json:
            yield Translation(self.data["source_text"], translation["term"], translation["alignFreq"],
                              translation["pos"],
                              [InflectedForm(form["term"], form["alignFreq"]) for form in
                               translation["inflectedForms"]])

    def get_examples(self):
        """A generator that gets words' usage examples pairs from server pair by pair.

        You should use this method if you need to get just some words, not all at once,
        but you want to do that immediately.

        Yields:
            Tuples with two WordUsageExample namedtuples (for source and target text and highlighted indexes)

        """

        for npage in range(1, self.page_count + 1):
            self.data["npage"] = npage
            examples_json = requests.post("https://context.reverso.net/bst-query-service", headers=HEADERS,
                                          data=json.dumps(self.data)).json()["list"]
            for word in examples_json:
                source = BeautifulSoup(word["s_text"], features=self.parser)
                target = BeautifulSoup(word["t_text"], features=self.parser)
                yield (WordUsageExample(source.text, self._find_highlighted_idxs(source)),
                       WordUsageExample(target.text, self._find_highlighted_idxs(target)))
