import unittest
import language_mapping

class TestLanguageMapping(unittest.TestCase):

    def test_get_language_code(self):
        self.assertEqual("de", language_mapping.get_language_code("German"))
        self.assertEqual("de", language_mapping.get_language_code("german"))
        self.assertEqual("de", language_mapping.get_language_code("German (sausage)"))
