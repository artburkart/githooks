from checker import Checker
from checker_results import CheckerResults
from parameterizedtestcase import ParameterizedTestCase


class TestCheckerResults(ParameterizedTestCase):
    def setUp(self):
        self.res = CheckerResults()

    def test_without_checker(self):
        self.assertEqual(self.res.checkers, [])

    def test_with_checker(self):
        checker1 = Checker()
        checker2 = Checker()
        self.res.record([checker1, checker2])
        self.assertEqual(self.res.checkers, [checker1, checker2])

    def test_without_errors(self):
        self.assertFalse(self.res.has_errors)

    def test_with_erroring_checker(self):
        checker1 = Checker()
        checker1.has_errors = True
        self.res.record(checker1)
        self.assertTrue(self.res.has_errors)

    def test_with_non_erroring_checker(self):
        self.res.record(Checker())
        self.assertFalse(self.res.has_errors)

    def test_with_two_non_erroring_checkers(self):
        checker1 = Checker()
        checker2 = Checker()
        checker1.has_errors = False
        checker2.has_errors = False
        self.res.record([checker1, checker2])
        self.assertFalse(self.res.has_errors)

    def test_with_two_checkers_one_false_one_true(self):
        checker1 = Checker()
        checker2 = Checker()
        checker1.has_errors = True
        checker2.has_errors = False
        self.res.record([checker1, checker2])
        self.assertTrue(self.res.has_errors)

    def test_str_output_with_non_erroring_checker(self):
        self.res.record(Checker())
        self.assertEqual(str(self.res), "")

    def test_str_output_with_erroring_checker(self):
        checker = Checker()
        checker.has_errors = True
        checker.messages = ["a", "b"]
        self.res.record(checker)
        expected = (
            "\n\n\t\t---------------------GIT-PATROL-----------------\n\na\nb"
            "\n\nTo permanently allow for this repo, run\n"
            "\x1b[1mgit config gitpatrol.basechecker false\x1b[0m\n"
            "and try again.\n\n"
            "To permanently allow it for *all* repos, run\n"
            "\x1b[1mgit config --global gitpatrol.basechecker false\x1b[0m\n"
            "and try again.")
        self.assertEqual(str(self.res), expected)

    def test_str_output_without_deactivation_message(self):
        checker = Checker()
        checker.has_errors = True
        checker.messages = ["a", "b"]
        checker.deactivation_message = ""
        self.res.record(checker)
        expected = (
            "\n\n\t\t---------------------GIT-PATROL-----------------\n\n"
            "a\nb\n")
        self.assertEqual(str(self.res), expected)
