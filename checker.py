from colors import Colors
import os
import re
from subprocess import check_output
from subprocess import CalledProcessError


class Checker:
    """This is the base class from which all the checkers inherit. The only
    thing of interest in here is the deactivation message. Everything else is
    overridden in the inheriting checker classes.
    """
    HOOK_KEY = "basechecker"
    WARNING = Colors.WARNING + "WARNING:" + Colors.ENDC
    ERROR = Colors.FAIL + "ERROR:" + Colors.ENDC

    def __init__(self, opts=None):
        if opts is None:
            opts = {}
        self.file = opts.get("filepath")
        self.changed_code = opts.get("changes")
        self.dir = opts.get("directory")
        self.user = opts.get("user") or os.environ.get("USER")

    def warning_message(self):
        return "Generic warning message"

    @property
    def has_errors(self):
        return bool(self.messages)

    @property
    def excluded_dir(self):
        in_assets = re.search(r"assets\/", self.dir or "")
        in_vendor = re.search(r"\/vendor", self.dir or "")
        return bool(in_assets and in_vendor)

    @property
    def pref_on(self):
        cmd = "git config --get gitpatrol.{}".format(self.HOOK_KEY)
        try:
            return check_output(cmd.split()).strip().lower() == "true"
        except CalledProcessError as e:
            return False

    @property
    def messages(self):
        return []

    @property
    def deactivation_message(self):
        return (
            "\nTo permanently allow for this repo, run\n"
            "\033[1mgit config gitpatrol.{} false\033[0m\n"
            "and try again.\n\n"
            "To permanently allow it for *all* repos, run\n"
            "\033[1mgit config --global gitpatrol.{} false\033[0m\n"
            "and try again.").format(self.HOOK_KEY, self.HOOK_KEY)

    def print_error_messages(self):
        for m in self.messages:
            print m
