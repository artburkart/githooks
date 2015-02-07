from gitpatrol.checkers import PrivateKeyChecker
from parameterizedtestcase import ParameterizedTestCase


class TestPrivateKeyChecker(ParameterizedTestCase):
    test_list = [
        # Nothing wrong
        ({
            "filepath": "fizzbuzz.js",
            "changes": "Hello",
            "pref_on": True
        }, False),
        # PRIVATE KEY
        ({
            "filepath": "fizzbuzz.js",
            "changes": "foo; PRIVATE KEY is there!",
            "pref_on": True
        }, True),
        # ssh-rsa
        ({
            "filepath": "fizzbuzz.js",
            "changes": "ssh-rsa follows...",
            "pref_on": True
        }, True)
    ]

    @ParameterizedTestCase.parameterize(("opts", "expected"), test_list)
    def test_private_key_checker(self, opts, expected):
        checker = PrivateKeyChecker(opts)
        self.assertEqual(checker.has_errors, expected)
        self.assertEqual(bool(checker.err_messages), expected)

    def test_warning_message(self):
        opts = {
            "filepath": "fizzbuzz.js",
            "changes": "foo; PRIVATE KEY is there!",
            "pref_on": True
        }
        checker = PrivateKeyChecker(opts)
        self.assertTrue(len(checker.err_messages) == 1)
        self.assertEqual(
            checker.err_messages[0],
            "\"PRIVATE KEY\" found, but not allowed (privatekey).\n"
        )
