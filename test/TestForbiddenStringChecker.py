from checkers import ForbiddenStringChecker
from parameterizedtestcase import ParameterizedTestCase


class TestForbiddenStringChecker(ParameterizedTestCase):
    test_list = [
        # left git alligators
        ({
            "filepath": "fizzbuzz.js",
            "changes": "Hello >>>>>>>> there"
        }, True),
        # right git alligators
        ({
            "filepath": "fizzbuzz.js",
            "changes": "Hello <<<<<<<< there"
        }, True),
        # git equals chain
        ({
            "filepath": "fizzbuzz.js",
            "changes": "Hello ======== there"
        }, True),
        # Nothing
        ({
            "filepath": "fizzbuzz.js",
            "changes": "Hello there"
        }, False),
    ]

    @ParameterizedTestCase.parameterize(("opts", "expected"), test_list)
    def test_forbidden_string_checker(self, opts, expected):
        checker = ForbiddenStringChecker(opts)
        self.assertEqual(checker.has_errors, expected)
        self.assertEqual(bool(checker.messages), expected)

    def test_warning_message(self):
        opts = {
            "filepath": "fizzbuzz.js",
            "changes": "Hello >>>>>>>> there"
        }
        checker = ForbiddenStringChecker(opts)
        self.assertEqual(checker.messages[0], (
            "{}\n"
            "git-patrol forbids committing "
            "\"{}\" to {}\n"
        ).format(checker.ERROR, ">>>>>>", checker.file))
