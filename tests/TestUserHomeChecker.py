"""TODO(arthurb): Figure out a strategy to accommodate use cases like this"""
# from lib.checkers import UserHomeChecker
# from parameterizedtestcase import ParameterizedTestCase

# class TestUserHomeChecker(ParameterizedTestCase):
#     def test_provider(self):
#         err1 = "\"home/bob\" found, but not allowed (userhome).\n"
#         err2 = "\"Users/bob\" found, but not allowed (userhome).\n"
#         err3 = "\"exports/home/bob\" found, but not allowed (userhome).\n"

#         return [
#             # Nothing wrong
#             ({
#                 "directory": "/usr/local",
#                 "filepath": "fizzbuzz.js",
#                 "changes": "Hello",
#                 "user": "bob",
#                 "enabled": True
#             }, []),
#             # Code with a home/ but not for that user
#             ({
#                 "directory": "/usr/local",
#                 "filepath": "fizzbuzz.js",
#                 "changes": "cd /home/fred",
#                 "user": "bob",
#                 "enabled": True
#             }, []),
#             # Code with a /home/(user)
#             ({
#                 "directory": "/usr/local",
#                 "filepath": "fizzbuzz.js",
#                 "changes": "cd /home/bob/.emacs.d",
#                 "user": "bob",
#                 "enabled": True
#             }, [err1]),
#             # Code with a /Users/(user)
#             ({
#                 "directory": "/usr/local",
#                 "filepath": "fizzbuzz.js",
#                 "changes": "cd /Users/bob",
#                 "user": "bob",
#                 "enabled": True
#             }, [err2]),
#             # Code with a /exports/home/(user)
#             ({
#                 "directory": "/usr/local",
#                 "filepath": "fizzbuzz.js",
#                 "changes": "cd /exports/home/bob",
#                 "user": "bob",
#                 "enabled": True
#             }, [err1, err3]),
#             # Code with two copies of the same error
#             ({
#                 "directory": "/usr/local",
#                 "filepath": "fizzbuzz.js",
#                 "changes": "/home/bob there\n and here's /Users/bob",
#                 "user": "bob",
#                 "enabled": True
#             }, [err1, err2])
#         ]

#     @ParameterizedTestCase.parameterize(
#         ("opts", "expected"),
#         test_provider(UserHomeChecker)
#     )
#     def test_user_home_checker(self, opts, expected):
#         opts.update({
#             "key": "userhome"
#         })
#         checker = UserHomeChecker(opts)
#         self.assertEqual(checker.has_errors, bool(expected))
#         self.assertEqual(len(checker.err_messages), len(expected))
#         self.assertEqual(checker.err_messages, expected)
