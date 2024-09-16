import unittest
from app import translate

class TestTranslationFunction(unittest.TestCase):
    
    def setUp(self):
        # Default model type to Local-Based for testing purposes
        self.model_type = "Local-Based"

    def test_translate_to_french(self):
        # Test translation to French using the Local-Based model
        result = translate("Hello", "French", self.model_type)
        self.assertEqual(result, "Bonjour")

    def test_translate_to_german(self):
        # Test translation to German using the Local-Based model
        result = translate("Hello", "German", self.model_type)
        self.assertEqual(result, "Hallo")

    def test_translate_to_romanian(self):
        # Test translation to Romanian using the Local-Based model
        result = translate("Hello", "Romanian", self.model_type)
        self.assertTrue(result in ["Salut", "Bună ziua"])  # Accept both "Salut" and "Bună ziua"

    def test_unsupported_language(self):
        # Test translation to unsupported language using the Local-Based model
        result = translate("Hello", "Spanish", self.model_type)
        self.assertEqual(result, "Sorry, this language is not supported.")

if __name__ == '__main__':
    unittest.main()
