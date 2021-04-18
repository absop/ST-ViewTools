import sublime_plugin


class InitialInputHandler(sublime_plugin.TextInputHandler):
    def placeholder(self):
        return 'Number From'

    def initial_text(self):
        return '1'

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
            numstr = '{:0>{}}'.format(i + int(initial), lmn)
            self.view.insert(edit, sels[i].end(), numstr)

    def input(self, args):
        return InitialInputHandler()
