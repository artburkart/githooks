from lib.checker import Checker
from parameterizedtestcase import ParameterizedTestCase


class TestAlertChecker(ParameterizedTestCase):
    def test_provider(self):
        err = "\"alert\" found, but not allowed (alert)."
        return [
            # js code with alert
            ({
                "filepath": "fizzbuzz.js",
                "changes": "var x = 3; alert(x);"
            }, [err]),
            # js code without alert
            ({
                "filepath": "fizzbuzz.js",
                "changes": "console.log('Hello, world!');"
            }, []),
            # py code without alert
            ({
                "filepath": "fizzbuzz.py",
                "changes": "console.log('Hello, world!');"
            }, []),
            # py code with alert
            ({
                "filepath": "fizzbuzz.py",
                "changes": "alert('Hello, world!');"
            }, [])
        ]

    @ParameterizedTestCase.parameterize(
        ("opts", "expected"),
        test_provider(Checker)
    )
    def test_alert_checker(self, opts, expected):
        opts.update({
            "key": "alert",
            "forbidden": ["alert"],
            "check": [".js"],
            "directory": "/usr/local",
            "enabled": True
        })
        checker = Checker(opts)
        self.assertEqual(checker.has_errors, bool(expected))
        self.assertEqual(len(checker.err_messages), len(expected))
        self.assertEqual(checker.err_messages, expected)
