import sublime
import sublime_plugin
import itertools


class SelectNextNumberCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        nums = list(str(i) for i in xrange(10))
        sels = self.view.sel()
        new_sels = []
        for sel in sels:
            start_ind, end_ind = 0, 0
            for i in itertools.count(sel.begin()):
                s = self.view.substr(i)
                if s == u'\x00':
                    break
                elif s in nums:
                    start_ind = i
                    for i in itertools.count(start_ind):
                        if self.view.substr(i) not in nums:
                            end_ind = i
                            break
                    new_sels.append(sublime.Region(start_ind, end_ind))
                    break
        sels.clear()
        for sel in new_sels:
            sels.add(sel)


class ModifyNumbersCommand(sublime_plugin.TextCommand):
    """docstring for ModifyNumberCommand"""

    def increment(self, x):
        return x + 1

    def decrement(self, x):
        return x - 1

    def double(self, x):
        return x * 2

    def squared(self, x):
        return x * x

    def sequence(self, x):
        if self.position == 0:
            self.basis = x
        return self.basis + self.position

    def run(self, edit, args):
        if 'modifier_function' in args:
            modifier = args['modifier_function']
        elif 'modifier_name' in args:
            modifier = getattr(self, args['modifier_name'], None)
            if not modifier:
                self.view.set_status(
                    'SublimeNumberManipulation', 'SublimeNumberManipulation '
                    'plugin could not understand the  value of the parameter '
                    'modifier_name')
                return
        self.view.run_command('select_next_number')
        sels = self.view.sel()
        for self.position, sel in enumerate(sels):
            self.view.replace(edit, sel,
                              str(modifier(int(self.view.substr(sel)))))
