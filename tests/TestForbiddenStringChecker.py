from lib.checker import Checker
from parameterizedtestcase import ParameterizedTestCase


class TestForbiddenStringChecker(ParameterizedTestCase):
    def test_provider(self):
        err1 = "\">>>>>>\" found, but not allowed (forbiddenstring)."
        err2 = "\"<<<<<<\" found, but not allowed (forbiddenstring)."
        err3 = "\"====\" found, but not allowed (forbiddenstring)."
        return [
            # left git alligators
            ({
                "filepath": "fizzbuzz.js",
                "changes": "+Hello >>>>>>>> there",
                "enabled": True
            }, [err1]),
            # right git alligators
            ({
                "filepath": "fizzbuzz.js",
                "changes": "+Hello <<<<<<<< there",
                "enabled": True
            }, [err2]),
            # git equals chain
            ({
                "filepath": "fizzbuzz.js",
                "changes": "+Hello ======== there",
                "enabled": True
            }, [err3]),
            # Nothing
            ({
                "filepath": "fizzbuzz.js",
                "changes": "+Hello there",
                "enabled": True
            }, [])
        ]

    @ParameterizedTestCase.parameterize(
        ("opts", "expected"),
        test_provider(Checker)
    )
    def test_forbidden_string_checker(self, opts, expected):
        opts.update({
            "key": "forbiddenstring",
            "forbidden": [">>>>>>", "<<<<<<", "===="]
        })
        checker = Checker(opts)
        self.assertEqual(checker.err_messages, expected)
