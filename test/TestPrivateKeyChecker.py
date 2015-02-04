from checkers import PrivateKeyChecker
from parameterizedtestcase import ParameterizedTestCase


class TestForbiddenStringChecker(ParameterizedTestCase):
    test_list = [
        # Nothing wrong
        ({
            "filepath": "fizzbuzz.js",
            "changes": "Hello"
        }, False),
        # PRIVATE KEY
        ({
            "filepath": "fizzbuzz.js",
            "changes": "foo; PRIVATE KEY is there!"
        }, True),
        # ssh-rsa
        ({
            "filepath": "fizzbuzz.js",
            "changes": "ssh-rsa follows..."
        }, True)
    ]

    @ParameterizedTestCase.parameterize(("opts", "expected"), test_list)
    def test_private_key_checker(self, opts, expected):
        checker = PrivateKeyChecker(opts)
        self.assertEqual(checker.has_errors, expected)
        self.assertEqual(bool(checker.messages), expected)

    def test_warning_message(self):
        opts = {
            "filepath": "fizzbuzz.js",
            "changes": "foo; PRIVATE KEY is there!"
        }
        checker = PrivateKeyChecker(opts)
        self.assertEqual(checker.messages[0], (
            "{}\ngit-patrol forbids committing "
            "\"PRIVATE KEY\" to {}"
        ).format(checker.ERROR, checker.file))
