class CheckerResults:
    def __init__(self):
        self.checkers = []

    def __str__(self):
        out = ""
        for checker in self.checkers:
            """
                TODO(arthurb): I'm not convinced yet that this `has_errors`
                method call is even necessary. I might remove it.
            """
            if checker.has_errors():
                for msg in checker.messages:
                    out += "{}\n".format(msg)
            try:
                checker.deactivate_message()
            except AttributeError:
                out += "{}\n".format(checker.deactivate_message())
        return out

    def record(self, checker):
        self.checkers.append(checker)

    def has_errors(self):
        return any(map(lambda c: c.has_errors(), self.checkers))

    def checkers(self):
        return self.checkers
