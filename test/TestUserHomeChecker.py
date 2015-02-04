from checkers import UserHomeChecker
from parameterizedtestcase import ParameterizedTestCase


class TestUserHomeChecker(ParameterizedTestCase):
    test_list = [
        # Nothing wrong
        ({
            "directory": "/usr/local",
            "filepath": "fizzbuzz.js",
            "changes": "Hello",
            "user": "bob"
        }, False),
        # Code with a home/ but not for that user
        ({
            "directory": "/usr/local",
            "filepath": "fizzbuzz.js",
            "changes": "cd /home/fred",
            "user": "bob"
        }, False),
        # Code with a /home/(user)
        ({
            "directory": "/usr/local",
            "filepath": "fizzbuzz.js",
            "changes": "cd /home/bob/.emacs.d",
            "user": "bob"
        }, True),
        # Code with a /Users/(user)
        ({
            "directory": "/usr/local",
            "filepath": "fizzbuzz.js",
            "changes": "cd /Users/bob",
            "user": "bob"
        }, True),
        # Code with a /export/home/(user)
        ({
            "directory": "/usr/local",
            "filepath": "fizzbuzz.js",
            "changes": "cd /export/home/bob",
            "user": "bob"
        }, True),
        # Code with two copies of the same error
        ({
            "directory": "/usr/local",
            "filepath": "fizzbuzz.js",
            "changes": "/home/bob there\n and here's /Users/bob",
            "user": "bob"
        }, True)
    ]

    @ParameterizedTestCase.parameterize(("opts", "expected"), test_list)
    def test_user_home_checker(self, opts, expected):
        checker = UserHomeChecker(opts)
        self.assertEqual(checker.has_errors, expected)
        self.assertEqual(bool(checker.messages), expected)

    def test_warning_message(self):
        opts = {
            "directory": "/usr/local",
            "filepath": "fizzbuzz.js",
            "changes": "cd /home/bob/.emacs.d",
            "user": "bob"
        }
        checker = UserHomeChecker(opts)
        self.assertEqual(checker.messages[0], (
            "{}\n"
            "git-patrol won't commit hard-coded home "
            "dir (home/bob) to {}\n"
        ).format(checker.ERROR, checker.file))
