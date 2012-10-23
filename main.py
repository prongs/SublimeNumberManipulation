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
				print s
				if s==u'\x00':
					break
				elif s in nums:
					found=True
					start_ind=i
					break
			for i in itertools.count(start_ind):
				if self.view.substr(i) not in nums:
					end_ind=i;
					break
			new_sels.append(sublime.Region(start_ind,end_ind))
		sels.clear()
		for sel in new_sels:
			sels.add(sel)

