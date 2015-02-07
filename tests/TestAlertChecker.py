from gitpatrol.checkers import AlertChecker
from parameterizedtestcase import ParameterizedTestCase


class TestAlertChecker(ParameterizedTestCase):
    test_list = [
        # js code with alert
        ({
            "filepath": "fizzbuzz.js",
            "changes": "var x = 3; alert(x);",
            "directory": "/usr/local",
            "pref_on": True
        }, True),
        # js code without alert
        ({
            "filepath": "fizzbuzz.js",
            "changes": "console.log('Hello, world!');",
            "directory": "/usr/local",
            "pref_on": True
        }, False),
        # py code without alert
        ({
            "filepath": "fizzbuzz.py",
            "changes": "console.log('Hello, world!');",
            "directory": "/usr/local",
            "pref_on": True
        }, False),
        # py code with alert
        ({
            "filepath": "fizzbuzz.py",
            "changes": "alert('Hello, world!');",
            "directory": "/usr/local",
            "pref_on": True
        }, False)
    ]

    @ParameterizedTestCase.parameterize(("opts", "expected"), test_list)
    def test_alert_checker(self, opts, expected):
        checker = AlertChecker(opts)
        self.assertEqual(checker.has_errors, expected)
        self.assertEqual(bool(checker.err_messages), expected)

    def test_warning_message(self):
        opts = {
            "filepath": "fizzbuzz.js",
            "changes": "var x = 3; alert(x);",
            "directory": "/usr/local",
            "pref_on": True
        }
        checker = AlertChecker(opts)
        self.assertTrue(len(checker.err_messages) == 1)
        self.assertEqual(
            checker.err_messages[0],
            "\"alert\" found, but not allowed (alert).\n"
        )
