import sublime
import sublime_plugin


class RemoveCommentCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        inline_comments = self.view.find_by_selector('comment.line')
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

        block_comments = self.view.find_by_selector('comment.block')
        block_comments.reverse()
        for comment in block_comments:
            if self.view.classify(comment.a) & sublime.CLASS_LINE_START:
                self.view.erase(edit, comment)
            elif self.view.classify(comment.a) & sublime.CLASS_LINE_END:
                self.view.replace(edit, comment, '\n')
            else:
                full_lines = self.view.full_line(comment)
                region = sublime.Region(full_lines.a, comment.a)
                if self.view.substr(region).isspace():
                    comment.a = full_lines.a
                self.view.erase(edit, comment)

        trailing_white_space = self.view.find_all('[\t ]+$')
        trailing_white_space.reverse()
        for r in trailing_white_space:
            self.view.erase(edit, r)
