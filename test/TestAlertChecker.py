from checkers import AlertChecker
from parameterizedtestcase import ParameterizedTestCase


class TestAlertChecker(ParameterizedTestCase):
    test_list = [
        # js code with alert
        ({
            "filepath": "fizzbuzz.js",
            "changes": "var x = 3; alert(x);",
            "directory": "/usr/local"
        }, True),
        # js code without alert
        ({
            "filepath": "fizzbuzz.js",
            "changes": "console.log('Hello, world!');",
            "directory": "/usr/local"
        }, False),
        # py code without alert
        ({
            "filepath": "fizzbuzz.py",
            "changes": "console.log('Hello, world!');",
            "directory": "/usr/local"
        }, False),
        # py code with alert
        ({
            "filepath": "fizzbuzz.py",
            "changes": "alert('Hello, world!');",
            "directory": "/usr/local"
        }, False),
    ]

    @ParameterizedTestCase.parameterize(("opts", "expected"), test_list)
    def test_alert_checker(self, opts, expected):
        checker = AlertChecker(opts)
        self.assertEqual(checker.has_errors, expected)
        self.assertEqual(bool(checker.messages), expected)

    def test_warning_message(self):
        opts = {
            "filepath": "fizzbuzz.js",
            "changes": "var x = 3; alert(x);",
            "directory": "/usr/local"
        }
        checker = AlertChecker(opts)
        self.assertEqual(checker.messages[0], (
            "{}\n"
            "git-patrol won't commit lines "
            "with \"alert\" to {}\n"
        ).format(checker.WARNING, checker.file))
