import os
import pre_commit_helper as PreCommitHelper
import re


class StrictParenSpacingChecker:
    HOOK_KEY = "require_strict_paren_spacing"

    SHELL_SCRIPT_EXTS = [".sh", ".bash", ""]

    LPAREN_SPACE = "( "
    SPACE_RPAREN = " )"
    LBRACKET_SPACE = "[ "
    SPACE_RBRACKET = " ]"

    LPAREN_SPACE_REGEX = "\([ \t]+"
    SPACE_RPAREN_REGEX = "[ \t]+\)"
    LBRACKET_SPACE_REGEX = "\[[ \t]+"
    SPACE_RBRACKET_REGEX = "[ \t]+\]"

    def __init__(self, opts):
        self.dir = opts["dir"]
        self.file = opts["file"]
        self.changed_code = opts["changed_code"]
        self.pref_on = str(opts["pref_on"]).lower() == "true"
        self.messages = self.examine_code()

    def deactivate_message(self):
        return PreCommitHelper.deactivation_message(
            "allow", self.HOOK_KEY, False)

    def has_errors(self):
        return bool(self.messages)

    def examine_code(self):
        if not self.__use_for_project():
            return []
        mess = []
        is_script = os.path.splittext(self.file)[1] in self.SHELL_SCRIPT_EXTS
        excluded_dir = PreCommitHelper.directory_excluded_from_checks(self.dir)
        if not is_script and not excluded_dir:
            if re.search(LPAREN_SPACE_REGEX, self.changed_code):
                mess.append(self.__warning_message(LPAREN_SPACE))
            if re.search(SPACE_RPAREN_REGEX, self.changed_code):
                mess.append(self.__warning_message(SPACE_RPAREN))
            if re.search(LBRACKET_SPACE_REGEX, self.changed_code):
                mess.append(self.__warning_message(LBRACKET_SPACE))
            if re.search(SPACE_RBRACKET_REGEX, self.changed_code):
                mess.append(self.__warning_message(SPACE_RBRACKET))
        return mess

    def __use_for_project(self):
        val = PreCommitHelper.git_config_hook_val(self.HOOK_KEY).lower()
        return val == "true" or self.pref_on

    def __warning_message(self, expr):
        return """\
            WARNING:
            git pre-commit hook won't commit lines with "{}" to {}
            This may be OK, or not, depending on your project requirements.
            --------------
        """.format(expr, self.file)
