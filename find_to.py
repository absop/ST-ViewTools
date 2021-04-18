import sublime_plugin


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
