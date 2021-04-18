import sublime
import sublime_plugin


class DeleteToCommand(sublime_plugin.TextCommand):
    def run(self, edit, to='eof'):
        region, selected = None, self.view.sel()[0]
        if to == 'eof':
            region = sublime.Region(selected.end(), self.view.size())
        elif to == 'bof':
            region = sublime.Region(0, selected.begin())
        self.view.erase(edit, region)
