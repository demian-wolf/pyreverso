import unittest
import contextlib

from reverso_api.conjugation import ReversoConjugationAPI, Conjugation


class TestReversoConjugationAPI(unittest.TestCase):
    api = ReversoConjugationAPI("parler", "French")

    def test__get_conjugations(self):
        result = list(self.api.get_conjugations())
        

        for c in result:
            self.assertTrue(c.verb == 'parler')
        self.assertTrue(Conjugation(verb='parler', conjugation='parlé', extra='ayez', tense='Passé', mode='Impératif') in result)

