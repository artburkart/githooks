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
    WARNING = Colors.FAIL + "{}" + Colors.ENDC

    def __init__(self, opts=None):
        if opts is None:
            opts = {}
        self.file = opts.get("filepath")
        self.changed_code = opts.get("changes")
        self.dir = opts.get("directory")
        self.user = opts.get("user") or os.environ.get("USER")
        if opts.get("pref_on"):
            self.pref_on = opts.get("pref_on")

    @property
    def has_errors(self):
        return bool(self.err_messages)

    @property
    def excluded_dir(self):
        in_assets = re.search(r"assets\/", self.dir or "")
        in_vendor = re.search(r"\/vendor", self.dir or "")
        return bool(in_assets and in_vendor)

    @property
    def pref_on(self):
        cmd = "git config --get gitpatrol.{}".format(self.HOOK_KEY)
        try:
            print check_output(cmd.split()).strip().lower() == "true"
            return check_output(cmd.split()).strip().lower() == "true"
        except CalledProcessError as e:
            return False

    @property
    def err_messages(self):
        return []

    def print_error_messages(self):
        for m in self.err_messages:
            print m

    def warning_message(self, string):
        msg = "\"{}\" found, but not allowed ({}).\n"
        return msg.format(string, self.HOOK_KEY)
