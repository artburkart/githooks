from lib.checker import Checker
from lib.checker_results import CheckerResults
from lib.styles import ENDC, FAIL, OKBLUE
from unittest import TestCase


# TODO(arthurb): Cover more scenarios
class TestCheckerResults(TestCase):
    UNSETTABLE = [
        "has_errors",
        "disabled"
    ]

    def setUp(self):
        self.res = CheckerResults()

    def test_without_checker(self):
        self.res.record(None)
        self.assertEqual(self.res.checkers, [])

    def test_recording_single_checker(self):
        checker1 = Checker()
        self.res.record(checker1)
        self.assertEqual(self.res.checkers, [checker1])

    def test_default_checker_has_no_errors(self):
        self.assertFalse(self.res.has_errors)

    def test_cannot_set_properties(self):
        val = "beep"
        for attr in self.UNSETTABLE:
            setattr(self.res, attr, val)
            self.assertNotEqual(getattr(self.res, attr), val)

    def test_str_output_with_non_erroring_checker(self):
        self.res.record(Checker())
        expected = (
            "{0}\n\t\t---------------------------{1}"
            "{2}\n\t\t GIT PATROL IS WATCHING YOU{1}"
            "{0}\n\t\t---------------------------{1}"
            "\n\n"
            "No files were checked.\nEither no gitpatrol.toml config "
            "file was specified,\n or none of the checkers were enabled.\n\n"
            "You can disable the checkers in the gitpatrol.toml file, or you\n"
            "can completely disable Git Patrol for this commit by running \n"
            "`git commit --no-verify`.\n\n"
        ).format(FAIL, ENDC, OKBLUE)
        self.assertEqual(str(self.res), expected)

    def test_str_output_with_erroring_checker(self):
        checker = Checker({
            "key": "alert",
            "forbidden": ["alert"],
            "check": [".js"],
            "directory": "/usr/local",
            "filepath": "fizzbuzz.js",
            "changes": "var x = 3; alert(x);",
            "enabled": True
        })
        self.res.record(checker)
        expected = (
            "{0}\n\t\t---------------------------{1}"
            "{2}\n\t\t GIT PATROL IS WATCHING YOU{1}"
            "{0}\n\t\t---------------------------{1}"
            "\n"
            "\n\x1b[91m****\x1b[0m \x1b[1mfizzbuzz.js"
            "\x1b[0m \x1b[91m****\x1b[0m"
            "\n\"alert\" found, but not allowed (alert).\n\n"
            "You can disable the checkers in the gitpatrol.toml file, or you\n"
            "can completely disable Git Patrol for this commit by running \n"
            "`git commit --no-verify`.\n\n"
        ).format(FAIL, ENDC, OKBLUE)
        self.assertTrue(self.res.has_errors)
        self.assertEqual(str(self.res), expected)

    def test_str_output_with_multiple_erroring_checkers(self):
        # Record first checker
        checker1 = Checker({
            "key": "alert",
            "forbidden": ["alert"],
            "check": [".js"],
            "directory": "/usr/local",
            "filepath": "fizzbuzz.js",
            "changes": "var x = 3; alert(x);",
            "enabled": True
        })
        self.res.record(checker1)

        # Record second checker
        checker2 = Checker({
            "key": "whatever",
            "forbidden": ["whatever"],
            "check": [".js"],
            "directory": "/usr/local",
            "filepath": "fizzbuzz.js",
            "changes": "console(5); var whatever = 'yummy';",
            "enabled": True
        })
        self.res.record(checker2)

        expected = (
            "{0}\n\t\t---------------------------{1}"
            "{2}\n\t\t GIT PATROL IS WATCHING YOU{1}"
            "{0}\n\t\t---------------------------{1}"
            "\n"
            "\n\x1b[91m****\x1b[0m \x1b[1mfizzbuzz.js"
            "\x1b[0m \x1b[91m****\x1b[0m"
            "\n\"alert\" found, but not allowed (alert)."
            "\n\"whatever\" found, but not allowed (whatever).\n\n"
            "You can disable the checkers in the gitpatrol.toml file, or you\n"
            "can completely disable Git Patrol for this commit by running \n"
            "`git commit --no-verify`.\n\n"
        ).format(FAIL, ENDC, OKBLUE)
        self.assertTrue(self.res.has_errors)
        self.assertEqual(str(self.res), expected)
