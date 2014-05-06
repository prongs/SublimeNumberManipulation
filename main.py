import sublime
import sublime_plugin
import itertools
from ast import NodeTransformer, Load, Num, Call, Name, Attribute, copy_location, parse, dump


settings = sublime.load_settings("Number Manipulation.sublime-settings")

class SelectNextNumberCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        nums = list(str(i) for i in range(10))
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


class Calculator(object):
    class CalculatorTransformer(NodeTransformer):
        def __init__(self, x):
            self.x = x

        # def visit_Call(self, node):
        #     if node.func.id == "sin":
        #         math = Name(id='math', ctx=Load(), lineno=0, col_offset=0)
        #         sin = Attribute(value=math, attr='sin', ctx=Load(), lineno=0, col_offset=0)
        #         call = Call(func=sin, args=node.args, keywords=[], lineno=0, col_offset=0)
        #         return copy_location(call, node)
        #     else:
        #         return None # block all other strange identifier

        def visit_Name(self, node):
            if node.id == "x":
                num = Num(self.x, lineno=0, col_offset=0)
                return copy_location(num, node)
            # else if node.id == "pi":
            #     num = Num(self.x, lineno=0, col_offset=0)
            #     return copy_location(num, node)
            # else if node.id == "e":
            #     num = Num(math.e, lineno=0, col_offset=0)
            #     return copy_location(num, node)
            elif node.id in ("sin", "cos", "tan", "log", "e", "pi"):
                return node
            else:
                return None # block all other strange identifier

    def __init__(self, formula):
        self.formula = formula

    def calculate(self, x):
        tree = parse(self.formula, '<string>', 'eval')
        tree = Calculator.CalculatorTransformer(x).visit(tree)
        code = compile(tree, '<ast_tree>', 'eval')
        import math
        ns = vars(math).copy()
        ns['__builtins__'] = None
        return eval(code, ns)


class BatchModifyNumbersCommand(sublime_plugin.WindowCommand):
    def calculate(self, x):
        return self.calculator.calculate(x)

    def onDone(self, text):
        self.setLastUsedFormula(text)
        self.calculator = Calculator(text)
        active_view = self.window.active_view()
        active_view.run_command('select_next_number')
        sels = active_view.sel()
        try:
            edit = active_view.begin_edit()
            for self.position, sel in enumerate(sels):
                result = self.calculate(int(active_view.substr(sel)))
                print "result: ", result
                active_view.replace(edit, sel, str(result))
        finally:
            active_view.end_edit(edit)

    def getLastUsedFormula(self):
        return settings.get("LastUsedFormula") or "x"

    def setLastUsedFormula(self, formula):
        settings.set("LastUsedFormula", formula)

    def askFormula(self):
        self.window.show_input_panel("Please enter the batch formula. The variable 'x' will be substituted.",
                                     self.getLastUsedFormula(),
                                     self.onDone,
                                     None,
                                     None)

    def run(self):
        self.askFormula()


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
