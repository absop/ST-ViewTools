import os
import subprocess
import webbrowser

import sublime
import sublime_plugin


class OpenWithBase(sublime_plugin.TextCommand):
    def is_visible(self):
        return self.view.file_name() is not None and (
            os.path.isfile(self.view.file_name()))

    def is_enabled(self):
        return self.view.file_name() is not None and (
            os.path.isfile(self.view.file_name()))


class OpenTerminalHereCommand(OpenWithBase):
    def run(self, edit):
        directory = os.path.dirname(self.view.file_name())
        if sublime.platform() == 'linux':
            args = '--working-directory={}'.format(directory)
            commands = ['gnome-terminal', args]
            subprocess.call(commands)


class OpenWithCommand(OpenWithBase):
    def run(self, edit):
        if sublime.platform() == 'windows':
            os.popen('OpenWith.exe "%s"' % self.view.file_name())
        elif sublime.platform() == 'osx':
            subprocess.call(['open', self.view.file_name()])
        elif sublime.platform() == 'linux':
            subprocess.call(['xdg-open', self.view.file_name()])


class OpenWithDefaultApplicationCommand(OpenWithBase):
    def run(self, edit):
        """ code for learning
        if sublime.platform() == 'windows':
            os.startfile(self.view.file_name())
        """
        webbrowser.open_new_tab(self.view.file_name())
