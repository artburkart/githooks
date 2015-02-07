from gitpatrol.checkers import ForbiddenStringChecker
from parameterizedtestcase import ParameterizedTestCase


class TestForbiddenStringChecker(ParameterizedTestCase):
    test_list = [
        # left git alligators
        ({
            "filepath": "fizzbuzz.js",
            "changes": "Hello >>>>>>>> there",
            "pref_on": True
        }, True),
        # right git alligators
        ({
            "filepath": "fizzbuzz.js",
            "changes": "Hello <<<<<<<< there",
            "pref_on": True
        }, True),
        # git equals chain
        ({
            "filepath": "fizzbuzz.js",
            "changes": "Hello ======== there",
            "pref_on": True
        }, True),
        # Nothing
        ({
            "filepath": "fizzbuzz.js",
            "changes": "Hello there",
            "pref_on": True
        }, False)
    ]

    @ParameterizedTestCase.parameterize(("opts", "expected"), test_list)
    def test_forbidden_string_checker(self, opts, expected):
        checker = ForbiddenStringChecker(opts)
        self.assertEqual(checker.has_errors, expected)
        self.assertEqual(bool(checker.err_messages), expected)

    def test_warning_message(self):
        opts = {
            "filepath": "fizzbuzz.js",
            "changes": "Hello >>>>>>>> there",
            "pref_on": True
        }
        checker = ForbiddenStringChecker(opts)
        self.assertTrue(len(checker.err_messages) == 1)
        self.assertEqual(
            checker.err_messages[0],
            "\">>>>>>\" found, but not allowed (forbiddenstring).\n"
        )
