from gitpatrol.checkers import UserHomeChecker
from parameterizedtestcase import ParameterizedTestCase


class TestUserHomeChecker(ParameterizedTestCase):
    test_list = [
        # Nothing wrong
        ({
            "directory": "/usr/local",
            "filepath": "fizzbuzz.js",
            "changes": "Hello",
            "user": "bob",
            "pref_on": True
        }, False),
        # Code with a home/ but not for that user
        ({
            "directory": "/usr/local",
            "filepath": "fizzbuzz.js",
            "changes": "cd /home/fred",
            "user": "bob",
            "pref_on": True
        }, False),
        # Code with a /home/(user)
        ({
            "directory": "/usr/local",
            "filepath": "fizzbuzz.js",
            "changes": "cd /home/bob/.emacs.d",
            "user": "bob",
            "pref_on": True
        }, True),
        # Code with a /Users/(user)
        ({
            "directory": "/usr/local",
            "filepath": "fizzbuzz.js",
            "changes": "cd /Users/bob",
            "user": "bob",
            "pref_on": True
        }, True),
        # Code with a /export/home/(user)
        ({
            "directory": "/usr/local",
            "filepath": "fizzbuzz.js",
            "changes": "cd /export/home/bob",
            "user": "bob",
            "pref_on": True
        }, True),
        # Code with two copies of the same error
        ({
            "directory": "/usr/local",
            "filepath": "fizzbuzz.js",
            "changes": "/home/bob there\n and here's /Users/bob",
            "user": "bob",
            "pref_on": True
        }, True)
    ]

    @ParameterizedTestCase.parameterize(("opts", "expected"), test_list)
    def test_user_home_checker(self, opts, expected):
        checker = UserHomeChecker(opts)
        self.assertEqual(checker.has_errors, expected)
        self.assertEqual(bool(checker.err_messages), expected)

    def test_warning_message(self):
        opts = {
            "directory": "/usr/local",
            "filepath": "fizzbuzz.js",
            "changes": "cd /home/bob/.emacs.d",
            "user": "bob",
            "pref_on": True
        }
        checker = UserHomeChecker(opts)
        self.assertTrue(len(checker.err_messages) == 1)
        self.assertEqual(
            checker.err_messages[0],
            "\"home/bob\" found, but not allowed (userhome).\n"
        )
