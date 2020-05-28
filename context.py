#!/usr/bin/env python

from collections import namedtuple
import json

from bs4 import BeautifulSoup
import requests


HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json; charset=UTF-8"
}

LANG_NAMES = {"ar": "arabic",
              "de": "german",
              "en": "english",
              "es": "spanish",
              "fr": "french",
              }  # TODO: write for all available languages (if it would be necessary)

PARTS_OF_SPEECH = {"adj.": "adjective",
                   "adv.": "adverb",
                   "n.": "noun",
                   "v.": "verb",
                   None: None
                   }

WordUsageExample = namedtuple("WordUsageExample",
                              ("source_text", "target_text", "source_highlighted", "target_highlighted"))

Translation = namedtuple("Translation",
                         ("source_word", "translation", "frequency", "part_of_speech", "inflected_forms"))

InflectedForm = namedtuple("InflectedForm",
                           ("translation", "frequency"))


# TODO: improve explanation of the WordUsageExample in docstrings
# TODO: add docstrings for undocumented functions
# TODO: convert part of speech from short form to long (e.g. "v." -> "verb")
# TODO: maybe make a special object which contains both translation example and highlighted indexes

def find_highlighted_idxs(soup, tag):
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


class ReversoContextAPI(object):

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

    def __str__(self):
        return "A Reverso Context API instance\n" \
               "Source Text: {source_text}\n" \
               "Target Text: {target_text}\n" \
               "Source Language: {source_lang}\n" \
               "Target Language: {target_lang}\n" \
               "Total Page Count: {page_count}\n" \
               "HTML Parser: {parser}" \
            .format(page_count=self.page_count,
                    parser=self.parser,
                    **self.data)

    def __repr__(self):
        return "ReversoContextAPI({source_text!r}, {target_text!r}, {source_lang!r}, {target_lang!r}, {parser!r})" \
            .format(parser=self.parser, **self.data)

    def __eq__(self, other):
        def remove_npage(d):
            return {i: d[i] for i in d if i != "npage"}

        if isinstance(other, ReversoContextAPI):
            return remove_npage(self.data) == remove_npage(other.data) and self.parser == other.parser
        return False

    def get_translations(self):
        """Gets list of translations for the word (on the website you can find it just before the examples).

        Returns:
            A list of Translation namedtuples.
        """

        def fetch_inflected_forms(json):
            inflected_forms = []
            for form in json:
                inflected_forms.append(InflectedForm(form["term"], form["alignFreq"]))
            return inflected_forms

        translations_json = requests.post("https://context.reverso.net/bst-query-service", headers=HEADERS,
                                          data=json.dumps(self.data)).json()["dictionary_entry_list"]
        translations = []
        for translation in translations_json:
            translations.append(
                Translation(self.data["source_text"], translation["term"], translation["alignFreq"],
                            translation["pos"],
                            fetch_inflected_forms(translation["inflectedForms"])))

        return translations

    def get_examples_page_json(self, npage):
        """Gets examples from the specified page.

        Args:
            npage: Number of the page.

        Returns:
            JSON-based Python list of dicts, where every dict contains information about a particular
            word usage example.
        """

        self.data["npage"] = npage
        return requests.post("https://context.reverso.net/bst-query-service", headers=HEADERS,
                             data=json.dumps(self.data)).json()["list"]

    def get_examples_pair_by_pair(self):
        """A generator that gets words' pairs from server pair by pair.

        You should use this method if you need to get just some words, not all at once,
        but you want to get them immediately.

        Returns:
            A generator, which yields WordUsageExample namedtuples.
        """

        for npage in range(1, self.page_count + 1):
            for word in self.get_examples_page_json(npage):
                source = BeautifulSoup(word["s_text"], features=self.parser)
                target = BeautifulSoup(word["t_text"], features=self.parser)
                yield WordUsageExample(source.text, target.text,
                                       find_highlighted_idxs(source, "em"), find_highlighted_idxs(target, "em"))

    def get_examples(self):
        """Gets all words' pairs from the server at once returning them as a list.

        Because pretty big amount of time is necessary to get every page from the server,
        this method may take long time to finish, so use it only either if there are not
        so much usage examples for the particular word (<10 pages) or if you need to deal
        with all them at once.

        Returns:
            A list of words examples. Every element is a WordUsageExample namedtuple.
        """

        return [pair for pair in self.get_examples_pair_by_pair()]


# A simple usage example
if __name__ == "__main__":
    def insert_char(string, index, char):
        """Inserts character into a string.

        Example:
            string = "abc"
            index = 1
            char = "+"
            Returns: "a+bc"

        Args:
            string: Given string
            index: Index where to insert
            char: Which char to insert

        Return:
            String string with character char inserted at index index.
        """

        return string[:index] + char + string[index:]


    def highlight_string(string, start, end, shift):
        """'Highlights' the given string with * character.

        Example:
            string = "This is a sample string"
            start = 0
            end = 4
            shift = 0
            Returns: "*This* is a sample string"

        Args:
            string: The string to be highlighted
            start: The start index of the highlighted part
            end: The end index of the highlighted part

        Returns:
            The highlighted string.
        """

        s = insert_char(string, start + shift, "*")
        s = insert_char(s, end + shift + 1, "*")
        return s


    print("Reverso.Context API usage example")

    print()
    api = ReversoContextAPI(
        input("Enter the source text to search... "),
        input("Enter the target text to search (optional)... "),
        input("Enter the source language code... "),
        input("Enter the target language code... ")
    )

    print()
    print("Translations:")
    for source_word, translation, frequency, part_of_speech, inflected_forms in api.get_translations():
        print(source_word, "==", translation, frequency, part_of_speech, ("Inflected forms: " + ", ".join(
            map(lambda iform: str(iform.translation), inflected_forms)) if inflected_forms else None))

    print()
    print("Word Usage Examples:")
    results = api.get_examples_pair_by_pair()
    for source_text, target_text, source_highlighted, target_highlighted in results:
        shift = 0
        for start, end in source_highlighted:
            source_text = highlight_string(source_text, start, end, shift)
            shift += 2

        shift = 0
        for start, end in target_highlighted:
            target_text = highlight_string(target_text, start, end, shift)
            shift += 2

        print(source_text, "==", target_text)
