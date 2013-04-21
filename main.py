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


def sequence_modifier(i, x):
    global basis
    if i == 0:
        basis = x
    return basis + i


class ModifyNumbersCommand(sublime_plugin.TextCommand):
    """docstring for ModifyNumberCommand"""
    modifiers = {'increment': (lambda i, x: x + 1),
                 'decrement': (lambda i, x: x - 1),
                 'double': (lambda i, x: x * 2),
                 'squared': (lambda i, x: x * x),
                 'sequence': sequence_modifier}

    def run(self, edit, args):
        if 'modifier_function' in args:
            modifier = args['modifier_function']
        elif 'modifier_name' in args:
            if args['modifier_name'] not in self.modifiers:
                self.view.set_status(
                    'SublimeNumberManipulation', 'SublimeNumberManipulation '
                    'plugin could not understand the  value of the parameter '
                    'modifier_name')
                return
            modifier = self.modifiers[args['modifier_name']]
        self.view.run_command('select_next_number')
        sels = self.view.sel()
        for i, sel in enumerate(sels):
            self.view.replace(edit, sel,
                              str(modifier(i, int(self.view.substr(sel)))))
