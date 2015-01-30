import re


class PrivateKeyChecker:
    PRIVATE_KEY_INDICATORS = [
        r"PRIVATE KEY",
        r"ssh-rsa"
    ]

    def __init__(self, opts):
        self.dir = opts["dir"]
        self.file = opts["file"]
        self.changed_code = opts["changes"]
        self.messages = self.examine_code()

    def has_errors(self):
        return bool(self.messages)

    def examine_code(self):
        mess = []
        for indicator in PRIVATE_KEY_INDICATORS:
            m = re.search(indicator, self.changed_code)
            if m:
                mess.append(self.__warning_message(m.first() or m.last()))
        return mess

    def __warning_message(self, string):
        return """\
            Error:
            git pre-commit hook found private key in commit: "{}" to {}
            --------------
        """.format(string, self.file)
