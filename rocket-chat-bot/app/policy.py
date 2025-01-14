import re
from repository import PolicyRepository
from detect_secrets import SecretsCollection
from detect_secrets.settings import default_settings
from detect_secrets.main import scan_adhoc_string

class PolicyController:
    def __init__(self, db_uri):
        self.policy_repo = PolicyRepository(db_uri)
        # self.secrets = SecretsCollection()
        self.settings = default_settings

    def run(self, string):
        self.check_string_length(string)
        self.detect_word(string)
        self.detect_regex(string)
        self.detect_secrets_in_string(string)

    def check_string_length(self, string):
        max_length = self.policy_repo.get_length_limit()

        if max_length==0:
            return

        if max_length is not None and len(string.split()) > max_length:
            raise PolicyException(f"Prompt length exceeds limit: maximum {max_length}, got {len(string)}")

    def detect_word(self, string):
        blacklist_words = self.policy_repo.get_blacklist_words()
        for word in blacklist_words:
            found = detect_word_in_string(string, word)
            if found:
                raise PolicyException(f"Blacklist word detected: {word}")

    def detect_regex(self, string):
        regex_patterns = self.policy_repo.get_regex_patterns()
        for pattern in regex_patterns:
            found = detect_regex_in_string(string, pattern)
            if found:
                raise PolicyException(f"Regex pattern detected: {pattern}\nString: {found}")

    # TODO: Return matched detected secrets
    def detect_secrets_in_string(self, string):
        if not self.policy_repo.get_detect_secrets():
            return

        with self.settings():
            result = scan_adhoc_string(string)
            repr(result)
            if ": True" in result:
                result = re.sub(r".*: False\s*(:?\([\d.]+\))?\n?", "", result)
                raise PolicyException(result)

class PolicyException(Exception):
    def __str__(self):
        return "# Policy violation:\n" + super().__str__()

def detect_word_in_string(string, word):
    string = string.lower()
    word = word.lower()
    return word in string

def detect_regex_in_string(string, pattern):
    return re.findall(pattern, string)