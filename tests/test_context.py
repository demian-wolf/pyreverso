import unittest
import types

from reverso_api.context import *


# TODO: refactor

class TestReversoContextAPI(unittest.TestCase):
    """TestCase for ReversoContextAPI

    Includes tests for:
    -- .get_examples()
    -- .get_translations()
    """

    api = ReversoContextAPI(source_text="Github",
                            source_lang="en",
                            target_lang="ru")

    def test__properties(self):
        """Tests the ReversoContextAPI properties:

        -- supported_langs
        -- source_text
        -- target_text
        -- source_lang
        -- target_lang
        -- total_pages
        """

        pass

    def test__get_examples(self):
        """Tests the ReversoContextAPI.get_examples() method.

        -- tests the correctness of types
        -- tests attributes of related classes (WordUsageContext)
        -- tests the length of examples: must be 2 (one for source, and one for target text)
        -- tests the length of pairs of indexes (items of the context.highlighted)
        -- tests if 0 <= index <= len(context.text) is True for all indexes
        """

        examples = self.api.get_examples()
        self.assertTrue(isinstance(examples, types.GeneratorType))

        for example in examples:
            self.assertTrue(isinstance(example, tuple))
            self.assertTrue(len(example) == 2)
            for context in example:
                # Tests the WordUsageContext class
                self.assertTrue(isinstance(context, WordUsageContext))
                for attr in ("text", "highlighted"):
                    self.assertTrue(hasattr(context, attr))
                self.assertTrue(isinstance(context.text, str))
                self.assertTrue(isinstance(context.highlighted, tuple))

                for indexes in context.highlighted:
                    self.assertTrue(isinstance(indexes, tuple))
                    self.assertTrue(len(indexes) == 2)
                    for index in indexes:
                        self.assertTrue(isinstance(index, int))
                        self.assertTrue(0 <= index <= len(context.text))

    def test__get_translations(self):
        """Tests the ReversoContextAPI.get_translations()

        -- tests the correctness of types
        -- tests attributes of related classes (Translation, InflectedForm)
        """

        translations = self.api.get_translations()
        self.assertTrue(isinstance(translations, types.GeneratorType))

        for translation in translations:
            self.assertTrue(isinstance(translation, Translation))
            self.assertTrue(len(translation) == 5)

            # Tests the Translation class
            for attr in ("source_word", "translation",
                         "frequency", "part_of_speech",
                         "inflected_forms"):
                self.assertTrue(hasattr(Translation, attr))
            self.assertTrue(translation.source_word == self.api.source_text)
            self.assertTrue(isinstance(translation.translation, str))
            self.assertTrue(isinstance(translation.frequency, int))
            self.assertTrue(isinstance(translation.part_of_speech, str) \
                            or translation.part_of_speech is None)
            self.assertTrue(isinstance(translation.inflected_forms, tuple))

            # Tests the InflectedForms class
            for inflected_form in translation.inflected_forms:
                self.assertTrue(isinstance(inflected_form, InflectedForm))
                for attr in ("translation", "frequency"):
                    self.assertTrue(hasattr(inflected_form, attr))
                self.assertTrue(isinstance(inflected_form.translation, str))
                self.assertTrue(isinstance(inflected_form.frequency, int))
