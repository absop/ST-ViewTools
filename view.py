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


class FindToCommand(sublime_plugin.TextCommand):
    def run(self, edit, to='eof'):
        if not self.view.has_non_empty_selection_region():
            self.view.run_command('find_under_expand')
        selected = self.view.sel()[0]
        pattern = self.view.substr(selected)

        if to == 'eof':
            compare = lambda r: r.begin() > selected.end()
        elif to == 'bof':
            compare = lambda r: r.end() < selected.begin()

        regions = filter(compare, self.view.find_all(pattern))
        self.view.sel().add_all(regions)


class FindAllUnderAllCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        words = set(view.substr(view.word(r)) for r in view.sel())
        if words:
            pattern = "|".join(words)
            regions = view.find_all(pattern)
            view.sel().add_all(regions)


# To find whether a symbol is referenced in this view or not
# Consider to show info by popup menu
class CountOccurrenceCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        view = self.view
        if view.sel():
            word = view.substr(view.word(view.sel()[0]))
            occu = len(view.find_all(word))
            show = "Occur{%s: %d}" % (word, occu)
            view.window().status_message(show)
