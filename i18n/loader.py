# multi-language loader implementation

class LanguageLoader:
    def __init__(self, language_files):
        self.language_files = language_files

    def load(self, language):
        try:
            with open(self.language_files[language], 'r') as f:
                return f.read()
        except KeyError:
            raise ValueError(f'Language file for {language} not found.')
