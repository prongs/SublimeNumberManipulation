import sublime, sublime_plugin
import re
import itertools
class SelectNextNumberCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		nums=list(str(i) for i in xrange(10))
		sels=self.view.sel()
		new_sels=[]
		for sel in sels:
			found=False
			start_ind,end_ind=0,0
			for i in itertools.count(sel.begin()):				
				s=self.view.substr(i)
				if s==u'\x00':
					break
				elif s in nums:
					found=True
					start_ind=i
					for i in itertools.count(start_ind):
						if self.view.substr(i) not in nums:
							end_ind=i;
							break
					new_sels.append(sublime.Region(start_ind,end_ind))
					break
		sels.clear()
		for sel in new_sels:
			sels.add(sel)

class ModifyNumbersCommand(sublime_plugin.TextCommand):
	"""docstring for ModifyNumberCommand"""
	modifiers={'increment': (lambda x: x+1), 'decrement':(lambda x: x-1), 'double':(lambda x: x*2), 'squared':(lambda x: x*x)}
	def run(self,edit, args):
		if args.has_key('modifier_function'):
			self.modifier=args['modifier_function']
		elif args.has_key('modifier_name'):
			if not self.modifiers.has_key(args['modifier_name']):
				self.view.set_status('SublimeNumberManipulation','SublimeNumberManipulation plugin could not understand the value of the parameter modifier_name')
				return
			self.modifier=self.modifiers[args['modifier_name']]
		self.view.run_command('select_next_number')
		sels=self.view.sel()
		for sel in sels:
			self.view.replace(edit, sel, str(self.modifier(int(self.view.substr(sel)))))
