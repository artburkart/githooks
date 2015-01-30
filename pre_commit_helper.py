import re
from subprocess import check_output


def output_error_messages(self, messages):
    for m in messages:
        print m


def deactivation_message(self, verb, key, value):
    return """\
        To permanently {} for this repo, run
        git config hooks.{} {}
        and try again.

        To permanently {} it for *all* repos, run
        git config --global hooks.{} {}
        and try again.
        --------------
    """.format(verb, key, value, verb, key, value)


def dir_excluded_from_hook(self, exdir):
    return re.match(r"assets\/", exdir) and re.match(r"\/vendor", exdir)


def git_config_hook_val(self, hook_name):
    cmd = ["git", "config", "hooks.{}".format(hook_name)]
    return check_output(cmd).strip()


def run_checker(err, checker):
    ret = err
    if checker.errors:
        ret = True
        PreCommitHelper.output_error_messages(checker.messages)
        try:
            checker.deactivation_message()
        except AttributeError:
            return ret
    return ret
