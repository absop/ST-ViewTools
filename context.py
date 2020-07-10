import os
import re
import subprocess
import webbrowser

import sublime
import sublime_plugin


class DeleteToCommand(sublime_plugin.TextCommand):
    def run(self, edit, to="eof"):
        region, selected = None, self.view.sel()[0]
        if to == "eof":
            region = sublime.Region(selected.end(), self.view.size())
        elif to == "bof":
            region = sublime.Region(0, selected.begin())
        self.view.erase(edit, region)


class FindToCommand(sublime_plugin.TextCommand):
    def run(self, edit, to="eof"):
        selected = self.view.sel()[0]
        pattern = self.view.substr(selected)

        if to == "eof":
            compare = lambda r: r.begin() > selected.end()
        elif to == "bof":
            compare = lambda r: r.end() < selected.begin()

        regions = filter(compare, self.view.find_all(pattern))
        self.view.sel().add_all(regions)


class SystemOpenWith(sublime_plugin.TextCommand):
    def is_visible(self):
        return self.view.file_name() is not None and (
            os.path.isfile(self.view.file_name()))

    def is_enabled(self):
        return self.view.file_name() is not None and (
            os.path.isfile(self.view.file_name()))


class OpenTerminalHereCommand(SystemOpenWith):
    def run(self, edit):
        directory = os.path.dirname(self.view.file_name())
        if sublime.platform() == "linux":
            args = "--working-directory={}".format(directory)
            commands = ["gnome-terminal", args]
            subprocess.call(commands)


class SystemOpenWithCommand(SystemOpenWith):
    def run(self, edit):
        if sublime.platform() == "windows":
            command = "%%SystemRoot%%\\system32\\OpenWith.exe %s"
            os.popen(command % self.view.file_name())
        elif sublime.platform() == "osx":
            subprocess.call(["open", self.view.file_name()])
        elif sublime.platform() == "linux":
            subprocess.call(["xdg-open", self.view.file_name()])


class SystemOpenWithDefaultApplicationCommand(SystemOpenWith):
    def run(self, edit):
        webbrowser.open_new_tab(self.view.file_name())
        # if sublime.platform() == "windows":
        #     os.startfile(self.view.file_name())
        # elif sublime.platform() == "linux":
        #     subprocess.call(["xdg-open", self.view.file_name()])
        # elif sublime.platform() == "osx":
        #     subprocess.call(["open", self.view.file_name()])


class InitialInputHandler(sublime_plugin.TextInputHandler):
    def placeholder(self):
        return "First Number"

    def initial_text(self):
        return "1"

    def validate(self, numstr):
        try:
            int(numstr)
            return True
        except:
            return False


class NumberSelectionsCommand(sublime_plugin.TextCommand):
    def run(self, edit, initial):
        sels = self.view.sel()
        lmn = len(str(len(sels)))
        for i in range(len(sels) - 1, -1, -1):
            numstr = "{:0>{}}".format(i + int(initial), lmn)
            self.view.insert(edit, sels[i].end(), numstr)

    def input(self, args):
        return InitialInputHandler()


class RemoveCommentCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        inline_comments = self.view.find_by_selector("comment.line")
        inline_comments.reverse()
        for comment in inline_comments:
            if self.view.classify(comment.a) & sublime.CLASS_LINE_START:
                self.view.erase(edit, comment)
            else:
                full_line = self.view.full_line(comment.a)
                region = sublime.Region(full_line.a, comment.a)
                if self.view.substr(region).isspace():
                    self.view.erase(edit, full_line)
                else:
                    comment.b = comment.b - 1
                    self.view.erase(edit, comment)

        block_comments = self.view.find_by_selector("comment.block")
        block_comments.reverse()
        for comment in block_comments:
            if self.view.classify(comment.a) & sublime.CLASS_LINE_START:
                self.view.erase(edit, comment)
            elif self.view.classify(comment.a) & sublime.CLASS_LINE_END:
                self.view.replace(edit, comment, "\n")
            else:
                full_lines = self.view.full_line(comment)
                region = sublime.Region(full_lines.a, comment.a)
                if self.view.substr(region).isspace():
                    comment.a = full_lines.a
                self.view.erase(edit, comment)

        trailing_white_space = self.view.find_all("[\t ]+$")
        trailing_white_space.reverse()
        for r in trailing_white_space:
            self.view.erase(edit, r)
