import os
import re


class UserHomeChecker:
    def __init__(self, opts):
        self.dir = opts["dir"]
        self.file = opts["file"]
        self.changed_code = opts["changes"]
        self.user = opts["user"] or os.environ["USER"]
        self.user_home = [
            r"home\/{}".format(self.user),
            r"Users\/{}".format(self.user),
            r"\/exports\/home\/{}".format(self.user)
        ]
        self.messages = self.examine_code()

    def has_errors(self):
        return bool(self.messages)

    def examine_code(self):
        mess = []
        for home in self.user_home:
            m = re.search(home, self.changed_code)

    def __warning_message(self, string):
        return """\
            ERROR:
            git pre-commit hook won't commit hard-coded home dir ({}) to {}
            --------------
        """.format(string, self.file)
