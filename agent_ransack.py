import sublime, sublime_plugin
import os
from subprocess import Popen

AgentRansack = ""
if sublime.platform() == "windows":
	import _winreg

	AgentRansack =_winreg.QueryValue(_winreg.HKEY_LOCAL_MACHINE, 'SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\AgentRansack.exe')

	if not AgentRansack:
		if os.path.exists("%s\Mythicsoft\Agent Ransack\AgentRansack.exe" % os.environ['ProgramFiles(x86)']):
			AgentRansack = '"%s\Mythicsoft\Agent Ransack\AgentRansack.exe"' % os.environ['ProgramFiles(x86)']
		else:
			AgentRansack = '"%s\Mythicsoft\Agent Ransack\AgentRansack.exe"' % os.environ['ProgramFiles']


class AgentRansackCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		d_param = ''

		directories = []
		for region in self.view.sel():
			directory = self.view.substr(region)
			if os.path.isdir(directory):
				directories.append(os.path.realpath(directory))
		d_param = ';'.join(directories)

		if d_param == '' and len(self.view.file_name()) > 0:
			d_param = os.path.dirname(os.path.realpath(self.view.file_name()))

		if d_param != '':
			cmd_line = ''
			if sublime.platform() == "windows":
				cmd_line = '%s -d "%s"' % (AgentRansack, d_param)
			print "AgentRansack command: " + cmd_line
			Popen(cmd_line)


	def is_enabled(self):
		if not os.path.isfile(AgentRansack):
			return false
		is_enabled_file_name = self.view.file_name() and len(self.view.file_name()) > 0
		non_empty_regions = [region for region in self.view.sel() if not region.empty()]
		is_enabled_selection = len(non_empty_regions) > 0
		return is_enabled_file_name or is_enabled_selection
