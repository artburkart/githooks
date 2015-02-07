from checker import Checker
from colors import Colors


class CheckerResults:
    def __init__(self):
        self.checkers = []

    def __str__(self):
        filenames = []
        endholder = "{}*****{}".format(Colors.FAIL, Colors.ENDC)
        blocktitle = "\n{0} {1}{2}{3} {0}\n\n".format(
            endholder, Colors.BOLD, "{}", Colors.ENDC)
        out = ""
        for checker in self.checkers:
            if checker.err_messages:
                if checker.file not in filenames:
                    filenames.append(checker.file)
                    out = "{}{}".format(out, blocktitle.format(checker.file))
            for msg in checker.err_messages:
                out = "{}{}\n".format(out, msg)
        return out

    @property
    def has_errors(self):
        return any(map(lambda c: c.has_errors, self.checkers))

    def record(self, checker):
        if isinstance(checker, Checker):
            self.checkers.append(checker)
        elif isinstance(checker, list):
            for c in checker:
                if c not in self.checkers:
                    self.checkers.append(c)
