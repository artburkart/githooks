from checker import Checker


class CheckerResults:
    def __init__(self):
        self.checkers = []

    def __str__(self):
        end_holder = "\n\n\t\t---------------------GIT-PATROL-----------------\n\n"
        out = ""
        for checker in self.checkers:
            if checker.messages:
                out = "{}{}".format(out, end_holder)
            for msg in checker.messages:
                out = "{}{}\n".format(out, msg)
            if checker.messages:
                try:
                    dmsg = checker.deactivation_message
                    out = "{}{}".format(out, dmsg)
                except AttributeError:
                    pass
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
