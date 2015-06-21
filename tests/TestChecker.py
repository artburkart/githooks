from lib.checker import Checker
from parameterizedtestcase import ParameterizedTestCase
from subprocess import call
from subprocess import check_output
from subprocess import CalledProcessError


class TestChecker(ParameterizedTestCase):
    UNSETTABLE = [
        "err_messages",
        "has_errors",
        "enabled",
        "to_check",
        "to_ignore"
    ]

    def test_messages(self):
        checker = Checker()
        self.assertEqual(checker.err_messages, [])

    def test_str_messages(self):
        checker = Checker({
            "key": "alert",
            "forbidden": ["alert"],
            "check": [".js"],
            "directory": "/usr/local",
            "filepath": "fizzbuzz.js",
            "changes": "var x = 3; alert(x);",
            "enabled": True
        })
        err = "\"alert\" found, but not allowed (alert)."
        self.assertEqual(str(checker), err)

    def test_warning_message(self):
        checker = Checker()
        expected = "\"ham\" found, but not allowed (basechecker)."
        self.assertEqual(checker.warning_message("ham"), expected)

    def test_enabled_without_opts(self):
        checker = Checker()
        self.enabled_helper(checker, False)

    def test_enabled_with_opts(self):
        checker = Checker({"enabled": True})
        self.enabled_helper(checker, True)

    def test_cannot_set_properties(self):
        checker = Checker({"enabled": True})
        val = ""
        for attr in self.UNSETTABLE:
            setattr(checker, attr, val)
            self.assertNotEqual(getattr(checker, attr), val)

    def enabled_helper(self, checker, pref_set):
        key = checker.hook_key
        cmd = "git config --get gitpatrol.{}".format(key)
        try:
            orig = check_output(cmd.split()).strip().lower()
        except CalledProcessError:
            orig = None

        # Checker without any preference set
        if orig is not None:
            cmd = "git config --unset-all gitpatrol.{}".format(key)
            call(cmd.split())
        self.assertEqual(checker.enabled, pref_set)

        # Checker with preference set to true
        cmd = "git config gitpatrol.{} true".format(checker.hook_key)
        call(cmd.split())
        self.assertEqual(checker.enabled, True)

        # Checker with preference set to false
        cmd = "git config gitpatrol.{} false".format(checker.hook_key)
        call(cmd.split())
        self.assertEqual(checker.enabled, False)

        # Reset git to original state
        if orig is None:
            cmd = "git config --unset-all gitpatrol.{}".format(key)
        else:
            cmd = "git config gitpatrol.{} {}".format(key, orig)
        call(cmd.split())
