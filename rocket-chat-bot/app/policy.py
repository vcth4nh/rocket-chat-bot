import re
from repository import PolicyRepository

class PolicyController:
    def __init__(self, db_uri):
        self.policy_repo = PolicyRepository(db_uri)

    def run(self, string):
        return self.check_string_length(string)
            
    def check_string_length(self, string):
        max_length = self.policy_repo.get_length_limit()["value"]
        print(len(string))
        print(max_length)

        if max_length is not None and len(string) > max_length:
            print("String length exceeded")
            return False
        return True

    def detect_word(self, string, word, case_sensitive=False):
        if not case_sensitive:
            string = string.lower()
            word = word.lower()
        return word in string

    def detect_regex(self, string, pattern):
        return bool(re.search(pattern, string))
