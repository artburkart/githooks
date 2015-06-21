from lib.checker import Checker
from subprocess import call
from subprocess import check_output
from subprocess import CalledProcessError
from parameterizedtestcase import ParameterizedTestCase


class TestStrictParenSpacingChecker(ParameterizedTestCase):
    def test_provider(self):
        err1 = '"( H" found, but not allowed (strictparenspacing).'
        err2 = '"o )" found, but not allowed (strictparenspacing).'
        err3 = '"[ H" found, but not allowed (strictparenspacing).'
        err4 = '"o ]" found, but not allowed (strictparenspacing).'

        return (
            # No parens, no brackets
            ({"changes": "Hello"}, ".js", []),
            # Okay parens
            ({"changes": " (Hello) "}, ".js", []),
            # Okay brackets
            ({"changes": " [Hello] "}, ".js", []),
            # Bad right bracket in bash script
            ({"changes": " [Hello ] "}, ".sh", []),
            # Bad right bracket in file with no extension
            ({"changes": " [Hello ] "}, "", []),
            # Bad left paren
            ({"changes": "( Hello)"}, ".js", [err1]),
            # Bad right paren
            ({"changes": " (Hello )"}, ".js", [err2]),
            # Bad left bracket
            ({"changes": "[ Hello] "}, ".js", [err3]),
            # Bad right bracket
            ({"changes": " [Hello ] "}, ".js", [err4])
        )

    @ParameterizedTestCase.parameterize(
        ("opts", "expected"),
        test_provider(Checker)
    )
    def test_strict_paren_spacing_checker(self, opts, file_ext, expected):
        opts.update({
            "key": "strictparenspacing",
            "ignore": [".sh", ".bash", ""],
            "forbidden": [
                '\([ \t]+[^\s]',
                '[^\s][ \t]+\)',
                '\[[ \t]+[^\s]',
                '[^\s][ \t]+\]'],
            "filepath": "fizzbuzz" + file_ext,
            "enabled": True
        })
        checker = Checker(opts)
        self.assertEqual(checker.err_messages, expected)
