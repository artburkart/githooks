from lib.checker import Checker
from parameterizedtestcase import ParameterizedTestCase


class TestPrivateKeyChecker(ParameterizedTestCase):
    def test_provider(self):
        err1 = "\"PRIVATE KEY\" found, but not allowed (privatekey)."
        err2 = "\"ssh-rsa\" found, but not allowed (privatekey)."

        return (
            # Nothing wrong here
            ({"changes": "Hello"}, []),
            # PRIVATE KEY
            ({"changes": "foo; PRIVATE KEY is there!"}, [err1]),
            # ssh-rsa
            ({"changes": "ssh-rsa follows..."}, [err2])
        )

    @ParameterizedTestCase.parameterize(
        ("opts", "expected"),
        test_provider(Checker)
    )
    def test_private_key_checker(self, opts, expected):
        opts.update({
            "key": "privatekey",
            "forbidden": ["PRIVATE KEY", "ssh-rsa"],
            "filepath": "fizzbuzz.js",
            "enabled": True
        })
        checker = Checker(opts)
        self.assertEqual(checker.err_messages, expected)
