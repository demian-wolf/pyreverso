import json

from bs4 import BeautifulSoup
import requests


HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json; charset=UTF-8"
}

LANG_NAMES = {"en": "english",
              "ru": "russian", }  # TODO: write for all available languages


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

    def get_page(self, npage):
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

    def get_results_pair_by_pair(self):
        """A generator that gets words' pairs from server pair by pair.

        You should use this method if you need to get just some words, not all at once,
        but you want to get them immediately.

        Returns:
            A generator, which yields a tuple with two subtuples on every iteration.
            The first subtuple contains two elements: source and target text.
            The second one contains two lists with subtuples which contain
            start and end indexes of highlighted parts of the examples;
            first list is for the source text, while the second one is
            for the target text:
            ((source text, target text), ([(start, end), ...], [(start, end), ...], ...)
        """

        for npage in range(1, self.page_count + 1):
            for word in self.get_page(npage):
                source = BeautifulSoup(word["s_text"], features=self.parser)
                target = BeautifulSoup(word["t_text"], features=self.parser)
                yield ((source.text, target.text),
                       (find_highlighted_idxs(source, "em"), find_highlighted_idxs(target, "em")))

    def get_results(self):
        """Gets all words' pairs from the server at once returning them as a list.

        Because pretty big amount of time is necessary to get every page from the server,
        this method may take long time to finish, so use it only either if there are not
        so much usage examples for the particular word (<10 pages) or if you need to deal
        with all them at once.

        Returns:
            A list of words examples. Every element is a tuple with two subtuples.
            The first subtuple contains two elements: source and target text.
            The second one contains two lists with subtuples which contain
            start and end indexes of highlighted parts of the examples;
            first list is for the source text, while the second one is
            for the target text:
            ((source text, target text), ([(start, end), ...], [(start, end), ...], ...)
        """

        return [pair for pair in self.get_results_pair_by_pair()]


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


    api = ReversoContextAPI(
        input("Enter the source text to search... "),
        input("Enter the target text to search (optional)... "),
        input("Enter the source language code... "),
        input("Enter the target language code... ")
    )

    print()
    results = api.get_results_pair_by_pair()
    for pair, idxs in results:
        source_text, target_text = pair
        source_idxs, target_idxs = idxs

        shift = 0
        for start, end in source_idxs:
            source_text = highlight_string(source_text, start, end, shift)
            shift += 2

        shift = 0
        for start, end in target_idxs:
            target_text = highlight_string(target_text, start, end, shift)
            shift += 2

        print(source_text, "=", target_text)
