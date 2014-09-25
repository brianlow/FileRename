import sublime
import sublime_plugin
import os
import functools

class FileRenameCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        filename = self.view.file_name()
        branch, leaf = os.path.split(filename)

        panel = self.view.window().show_input_panel("New Name:", leaf, functools.partial(self.on_done, filename, branch), None, None)

        name, ext = os.path.splitext(leaf)
        panel.sel().clear()
        panel.sel().add(sublime.Region(0, len(name)))

    def on_done(self, old, branch, leaf):
            new = os.path.join(branch, leaf)

            try:
                if os.path.exists(new):
                    sublime.error_message(new + " already exists")
                    return;

                os.rename(old, new)

                v = self.view.window().find_open_file(old)
                if v:
                    v.retarget(new)
            except Exception as e :
                sublime.status_message("Unable to rename: " + str(e))

