from checkers import StrictParenSpacingChecker
from subprocess import call
from subprocess import check_output
from subprocess import CalledProcessError
from parameterizedtestcase import ParameterizedTestCase


class TestStrictParenSpacingChecker(ParameterizedTestCase):
    HOOK_VAL = ""
    test_list = [
        # No parentheses, pref on
        ({
            "filepath": "fizzbuzz.js",
            "changes": "Hello",
            "directory": "/usr/local"
        }, True, False),
        # Contains good parentheses, pref on
        ({
            "filepath": "fizzbuzz.js",
            "changes": " (Hello) ",
            "directory": "/usr/local"
        }, True, False),
        # Contains bad left paren, pref on
        ({
            "filepath": "fizzbuzz.js",
            "changes": " ( Hello) ",
            "directory": "/usr/local"
        }, True, True),
        # Contains bad right paren, pref on
        ({
            "filepath": "fizzbuzz.js",
            "changes": " (Hello ) ",
            "directory": "/usr/local"
        }, True, True),
        # No parentheses, pref off
        ({
            "filepath": "fizzbuzz.js",
            "changes": "Hello",
            "directory": "/usr/local"
        }, False, False),
        # Contains good parentheses, pref off
        ({
            "filepath": "fizzbuzz.js",
            "changes": " (Hello) ",
            "directory": "/usr/local"
        }, False, False),
        # Contains bad left paren, pref off
        ({
            "filepath": "fizzbuzz.js",
            "changes": " ( Hello) ",
            "directory": "/usr/local"
        }, False, False),
        # Contains bad right paren, pref off
        ({
            "filepath": "fizzbuzz.js",
            "changes": " (Hello ) ",
            "directory": "/usr/local"
        }, False, False),
        # Contains good brackets, pref on
        ({
            "filepath": "fizzbuzz.js",
            "changes": " [Hello] ",
            "directory": "/usr/local"
        }, True, False),
        # Contains bad left bracket, pref on
        ({
            "filepath": "fizzbuzz.js",
            "changes": " [ Hello] ",
            "directory": "/usr/local"
        }, True, True),
        # Contains bad right bracket, pref on
        ({
            "filepath": "fizzbuzz.js",
            "changes": " [Hello ] ",
            "directory": "/usr/local"
        }, True, True),
        # No brackets, pref off
        ({
            "filepath": "fizzbuzz.js",
            "changes": "Hello",
            "directory": "/usr/local"
        }, False, False),
        # Contains good brackets, pref off
        ({
            "filepath": "fizzbuzz.js",
            "changes": " [Hello] ",
            "directory": "/usr/local"
        }, False, False),
        # Contains bad left bracket, pref off
        ({
            "filepath": "fizzbuzz.js",
            "changes": " [ Hello] ",
            "directory": "/usr/local"
        }, False, False),
        # Contains bad right bracket, pref off
        ({
            "filepath": "fizzbuzz.js",
            "changes": " [Hello ] ",
            "directory": "/usr/local"
        }, False, False),
        # Excluded directory, pref on
        ({
            "filepath": "fizzbuzz.js",
            "changes": "( Hello )",
            "directory": "assets/vendor/usr/local"
        }, True, False),

    ]

    def setUp(self):
        cmd = "git config --get gitpatrol.requirestrictparenspacing"
        try:
            self.HOOK_VAL = check_output(cmd.split()).strip()
        except CalledProcessError:
            self.HOOK_VAL = ""
        cmd = "git config gitpatrol.requirestrictparenspacing true"
        call(cmd.split())

    def tearDown(self):
        cmd = "git config gitpatrol.requirestrictparenspacing {}"
        call(cmd.format(self.HOOK_VAL).split())

    @ParameterizedTestCase.parameterize(
        ("opts", "pref_on", "expected"),
        test_list
    )
    def test_strict_paren_spacing_checker(self, opts, pref_on, expected):
        checker = StrictParenSpacingChecker(opts)
        checker.pref_on = pref_on
        self.assertEqual(checker.has_errors, expected)
        self.assertEqual(bool(checker.messages), expected)

    def test_warning_message(self):
        opts = {
            "filepath": "fizzbuzz.js",
            "changes": " ( Hello) ",
            "directory": "/usr/local"
        }
        checker = StrictParenSpacingChecker(opts)
        checker.pref_on = True
        self.assertEqual(checker.messages[0], (
            "{}\n"
            "git-patrol won't commit lines"
            "with \"( \" to {}"
        ).format(checker.WARNING, checker.file))
