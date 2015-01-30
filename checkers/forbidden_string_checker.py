import re


class ForbiddenStringChecker:
    """
        TODO(arthurb): This is great to stop commits with merge annotations,
        but there could be other strings that would be useful to check against
    """
    FORBIDDEN_STRINGS = [
        r">>>>>>",
        r"<<<<<<",
        r"====",
        r"console\.\w*"
    ]

    def __init__(self, opts):
        self.file = opts["file"]
        self.changed_code = opts["changes"]
        self.messages = self.examine_code()

    def has_errors(self):
        return bool(self.messages)

    def examine_code(self):
        mess = []
        for forbidden in FORBIDDEN_STRINGS:
            m = re.search(forbidden)
            if m:
                mess.append(self.__warning_message(m.first() or m.last()))

    def __warning_message(self, string):
        return """\
            ERROR:
            git pre-commit hook forbids committing "{}" to {}
            --------------
        """.format(string, self.file)
