import re
from repository import PolicyRepository

class PolicyController:
    def __init__(self, db_uri):
        self.policy_repo = PolicyRepository(db_uri)

    def run(self, string):
        return self.check_string_length(string) and self.detect_word(string) and self.detect_regex(string)
            
    def check_string_length(self, string):
        max_length = self.policy_repo.get_length_limit()

        if max_length is not None and len(string) > max_length:
            print("String length exceeded")
            return False
        return True
    
    def detect_word_in_string(self, string, word):
        string = string.lower()
        word = word.lower()
        return word in string

    def detect_word(self, string):
        blacklist_words = self.policy_repo.get_blacklist_words()
        print(blacklist_words)
        for word in blacklist_words:
            if self.detect_word_in_string(string, word):
                print("Blacklist word detected")
                return False
        return True
    
    def detect_regex_in_string(self, string, pattern):
        return re.search(pattern, string)

    def detect_regex(self, string):
        regex_patterns = self.policy_repo.get_regex_patterns()
        for pattern in regex_patterns:
            if self.detect_regex_in_string(string, pattern):
                print("Regex pattern detected")
                return False
        return True
