from gitpatrol.checker import Checker
from parameterizedtestcase import ParameterizedTestCase
from subprocess import call
from subprocess import check_output
from subprocess import CalledProcessError


class TestChecker(ParameterizedTestCase):
    excluded_dirs = [
        # Random* directory
        ({"directory": "/home/foo/bar"}, False),
        # assets directory
        ({"directory": "/my/dir/assets/foo"}, False),
        # vendor directory
        ({"directory": "/my/dir/vendor/foo"}, False),
        # assets/**/vendor
        ({"directory": "/my/dir/assets/images/vendor/foo"}, True),
    ]

    @ParameterizedTestCase.parameterize(("opts", "expected"), excluded_dirs)
    def test_checker(self, opts, expected):
        checker = Checker(opts)
        self.assertEqual(checker.excluded_dir, expected)

    def test_messages(self):
        checker = Checker()
        self.assertEqual(checker.err_messages, [])

    def test_excluded_dir(self):
        checker = Checker()
        self.assertEqual(checker.excluded_dir, False)

    def test_warning_message(self):
        checker = Checker()
        expected = "\"ham\" found, but not allowed (basechecker).\n"
        self.assertEqual(checker.warning_message("ham"), expected)

    def test_print_messages(self):
        checker = Checker()
        self.assertEqual(checker.print_error_messages(), None)

    def test_pref_on_without_opts(self):
        checker = Checker()
        self.pref_on_helper(checker, False)

    def test_pref_on_with_opts(self):
        checker = Checker({"pref_on": True})
        self.pref_on_helper(checker, True)

    def pref_on_helper(self, checker, pref_set):
        key = checker.HOOK_KEY
        cmd = "git config --get gitpatrol.{}".format(key)
        try:
            orig = check_output(cmd.split()).strip().lower()
        except CalledProcessError:
            orig = None

        # Checker without any preference set
        if orig is not None:
            cmd = "git config --unset-all gitpatrol.{}".format(key)
            call(cmd.split())
        self.assertEqual(checker.pref_on, False or pref_set)

        # Checker with preference set to true
        cmd = "git config gitpatrol.{} true".format(checker.HOOK_KEY)
        call(cmd.split())
        self.assertEqual(checker.pref_on, True or pref_set)

        # Checker with preference set to false
        cmd = "git config gitpatrol.{} false".format(checker.HOOK_KEY)
        call(cmd.split())
        self.assertEqual(checker.pref_on, False or pref_set)

        # Reset git to original state
        if orig is None:
            cmd = "git config --unset-all gitpatrol.{}".format(key)
        else:
            cmd = "git config gitpatrol.{} {}".format(key, orig)
        call(cmd.split())
