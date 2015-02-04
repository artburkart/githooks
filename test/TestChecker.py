from checker import Checker
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
        self.assertEqual(checker.messages, [])

    def test_excluded_dir(self):
        checker = Checker()
        self.assertEqual(checker.excluded_dir, False)

    def test_warning_message(self):
        checker = Checker()
        expected = "Generic warning message"
        self.assertEqual(checker.warning_message(), expected)

    def test_unset_pref_on(self):
        checker = Checker()
        cmd = "git config --get gitpatrol.{}".format(checker.HOOK_KEY)
        try:
            orig = check_output(cmd.split())
        except CalledProcessError:
            orig = None

        # Checker without any preference set
        cmd = "git config --unset gitpatrol.{}".format(checker.HOOK_KEY)
        call(cmd.split())
        self.assertEqual(checker.pref_on, False)

        # Checker with preference set to true
        cmd = "git config gitpatrol.{} true".format(checker.HOOK_KEY)
        call(cmd.split())
        self.assertEqual(checker.pref_on, True)

        # Checker with preference set to false
        cmd = "git config gitpatrol.{} false".format(checker.HOOK_KEY)
        call(cmd.split())
        self.assertEqual(checker.pref_on, False)

        # Reset git to original state
        if orig is None:
            cmd = "git config --unset gitpatrol.{}".format(checker.HOOK_KEY)
        else:
            cmd = "git config gitpatrol.{} {}".format(checker.HOOK_KEY, orig)
        call(cmd.split())

    def test_print_messages(self):
        checker = Checker()
        self.assertEqual(checker.print_error_messages(), None)

    def test_deactivation_message(self):
        checker = Checker({})
        expected = (
            "\nTo permanently allow for this repo, run\n"
            "\x1b[1mgit config gitpatrol.basechecker false\x1b[0m\n"
            "and try again.\n\n"
            "To permanently allow it for *all* repos, run\n"
            "\x1b[1mgit config --global gitpatrol.basechecker false\x1b[0m\n"
            "and try again."
        )
        self.assertEqual(checker.deactivation_message, expected)
