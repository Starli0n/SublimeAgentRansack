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
		print 1
		if len(self.view.file_name()) > 0:
			cmd_line = ''
			if sublime.platform() == "windows":
				cmd_line = '%s -d "%s"' % (AgentRansack, os.path.dirname(os.path.realpath(self.view.file_name())))
			print "AgentRansack command: " + cmd_line
			Popen(cmd_line)


	def is_enabled(self):
		return sublime.platform() == "windows" and os.path.isfile(AgentRansack) and self.view.file_name() and len(self.view.file_name()) > 0
