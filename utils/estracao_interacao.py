import re


class ExtracaoInteracao:
    def __init__(self, df):
        self.df = df
        self.patterns = {
            'quantProfile': re.compile(r'updated (?:his|her) profile picture', re.IGNORECASE),
            'quantCover': re.compile(r'updated (?:his|her) cover photo', re.IGNORECASE),
            'quantAddPhotoWithOthers': re.compile(
                r'added (?:a new photo|new photos)(?: to the album:)?(?: —)? with .+(?: and .+)*(?: and \d+ others)?',
                re.IGNORECASE),
            'quantAddPhotoWith': re.compile(
                r'added (?:a new photo|new photos)(?: to the album:)?(?: —)? with',
                re.IGNORECASE),
            'quantAddPhoto': re.compile(
                r'(added (?:a new photo|new photos)|photo to the album:)',
                re.IGNORECASE),
            'quantSharedPhoto': re.compile(r'shared (?:.+\'s )?photo', re.IGNORECASE),
            'quantSharedVideo': re.compile(r'shared (?:.+\'s )?video', re.IGNORECASE),
            'quantSharedLink': re.compile(r'shared a link', re.IGNORECASE),
            'quantSharedPost': re.compile(r'shared (?:.+\'s )?post', re.IGNORECASE),
            'quantSharedEvent': re.compile(r'shared (?:.+\'s )?event', re.IGNORECASE),
            'quantSharedMemory': re.compile(r'shared a memory', re.IGNORECASE),
            'quantStatus': re.compile(r'updated (?:his|her) status', re.IGNORECASE)
        }

    @staticmethod
    def count_occurrences(text, pattern):
        if isinstance(text, str):
            return len(pattern.findall(text))
        return 0

    def extract_interactions(self):
        for key, pattern in self.patterns.items():
            self.df[key] = self.df['postStory'].apply(lambda x: self.count_occurrences(x, pattern))
        return self.df
