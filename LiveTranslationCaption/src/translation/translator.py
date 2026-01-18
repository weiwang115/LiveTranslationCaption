from googletrans import Translator as GoogleTranslator
import time


class Translator:
    """Translates text from Japanese to English."""
    
    def __init__(self, source_lang='ja', target_lang='en'):
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.translator = GoogleTranslator()
        self.last_translation = ""
        self.translation_cache = {}
        
    def translate(self, text):
        """
        Translate text from source language to target language.
        
        Args:
            text: Text to translate
            
        Returns:
            Translated text or original text if translation fails
        """
        if not text or text.strip() == "":
            return ""
        
        # Check cache first
        if text in self.translation_cache:
            return self.translation_cache[text]
        
        try:
            result = self.translator.translate(text, src=self.source_lang, dest=self.target_lang)
            translated_text = result.text
            
            # Cache the translation
            self.translation_cache[text] = translated_text
            
            # Limit cache size
            if len(self.translation_cache) > 100:
                # Remove oldest entries
                items = list(self.translation_cache.items())
                self.translation_cache = dict(items[50:])
            
            self.last_translation = translated_text
            print(f"Translated to English: {translated_text}")
            return translated_text
            
        except Exception as e:
            print(f"Translation error: {e}")
            return text  # Return original text if translation fails
    
    def translate_batch(self, texts):
        """Translate multiple texts."""
        results = []
        for text in texts:
            results.append(self.translate(text))
            time.sleep(0.1)  # Small delay to avoid rate limiting
        return results
    
    def set_languages(self, source_lang, target_lang):
        """Change source and target languages."""
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.translation_cache.clear()  # Clear cache when languages change