import unittest
from app import translate

class TestTranslationFunction(unittest.TestCase):
    
    def test_translate_to_french(self):
        result = translate("Hello", "French")
        self.assertIn("Bonjour", result, "Translation to French failed")
    
    def test_translate_to_german(self):
        result = translate("Hello", "German")
        self.assertIn("Hallo", result, "Translation to German failed")
    
    def test_translate_to_romanian(self):
        result = translate("Hello", "Romanian")
        self.assertTrue("Bună" in result or "Salut" in result, "Translation to Romanian failed")

    def test_unsupported_language(self):
        result = translate("Hello", "Spanish")
        self.assertEqual(result, "Sorry, this language is not supported.", "Unsupported language test failed")

if __name__ == "__main__":
    unittest.main()
