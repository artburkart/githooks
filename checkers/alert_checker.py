import pre_commit_helper as PreCommitHelper
import re


class AlertChecker:
    FLASH = r"flash\s*\[\s*:alert\s*\]"
    ALERT = r"alert"

    def __init__(self, opts):
        self.dir = opts["dir"]
        self.file = opts["file"]
        self.changed_code_array = opts["changes"]
        self.messages = self.examine_code()

    def has_errors(self):
        return bool(self.messages)

    def examine_code(self):
        """
            TODO(arthurb): This snippet is pretty useless unless it knows
            what type of file we're looking at. For example, Bootstrap
            uses alert as an HTML class type
        """
        mess = []
        if not PreCommitHelper.dir_excluded_from_hook(self.dir):
            for line in self.changed_code_array:
                if re.search(self.ALERT, line) and re.search(self.FLASH, line):
                    mess.append(self.__warning_message())
        return mess

    def __warning_message(self):
        return """\
            WARNING:
            git pre-commit hook won't commit lines with "alert" to {}
            --------------
        """.format(self.file)
