import sublime, sublime_plugin
import time
import subprocess
import os
import codecs
import re

process=None

file_head_template="""---
--
-- ${date}
-- @author ${author}
--
"""

new_class_template=file_head_template+"""
local ${short_file_name} = class("${short_file_name}")

function ${short_file_name}:ctor()
end

return ${short_file_name}
"""

new_layer_template=file_head_template+"""
local ${short_file_name} = class("${short_file_name}",BaseLayer)

function ${short_file_name}:ctor()
	${short_file_name}.super.ctor(self)
end

function ${short_file_name}:onEnter()
end

function ${short_file_name}:onExit()
end

return ${short_file_name}
"""

new_function_template="""
function ${short_file_name}:name()
end
"""

file_separator = "/"
if sublime.platform() == "windows":
	file_separator = "\\"

def getConfig(config,key):
	if os.path.exists(config):
		f=codecs.open(config,"r","utf-8")
		while True:
			line=f.readline()
			if line:
				sps=line.split("=")
				if sps[0].strip() == key:
					return sps[1].strip().replace("\"","")
			else:
				break

def generateCode(self,template):
	file_name = self.view.file_name()
	sp_start = file_name.rfind(file_separator) + 1
	sp_end = file_name.rfind(".")
	settings=sublime.load_settings("LuaTemplate.sublime-settings")
	author = settings.get("author","Your name")
	#短文件名
	short_file_name = file_name[sp_start:sp_end]
	code = template
	code = code.replace("${date}",time.strftime("%Y-%m-%d %X", time.localtime()))
	code = code.replace("${short_file_name}",short_file_name)
	code = code.replace("${author}",author)
	return code

# ltnewclass 新建一个类的模板
class LtnewclassCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		code = generateCode(self,new_class_template)
		(row,col) = self.view.rowcol(self.view.sel()[0].begin())
		self.view.insert(edit,self.view.text_point(row,col),code)

#ltnewlayer 新建一个层的模板
class LtnewlayerCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		code = generateCode(self,new_layer_template)
		(row,col) = self.view.rowcol(self.view.sel()[0].begin())
		self.view.insert(edit,self.view.text_point(row,col),code)

#ltnewfunction 新建一个函数的模板
class LtnewfunctionCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		code = generateCode(self,new_function_template)
		(row,col) = self.view.rowcol(self.view.sel()[0].begin())
		self.view.insert(edit,self.view.text_point(row,col),code)

#ltrunwithplayer 跑起来
class LtrunwithplayerCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		settings=sublime.load_settings("LuaTemplate.sublime-settings")
		quickroot = settings.get("quick_v3_root","")
		if sublime.platform() == "windows":
			playerPath = quickroot+"/quick/player/win32/player3.exe"
		if sublime.platform() == "osx":
			playerPath = quickroot+"/player3.app/Contents/MacOS/player3"

		file_name = self.view.file_name()
		workdir=file_name[0:file_name.rfind("src")]
		srcDirName=workdir+"/src"
		args=[playerPath]
		args.append("-workdir")
		args.append(workdir)
		args.append("-file")
		args.append(srcDirName+"/main.lua")
		global process
		if process:
			try:
				process.terminate()
			except Exception:
				pass
		if sublime.platform()=="osx":
			process=subprocess.Popen(args)
		elif sublime.platform()=="windows":
			process=subprocess.Popen(args)

#ltrunwithsimulator 跑起来2
class LtrunwithsimulatorCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		file_name = self.view.file_name()
		workdir=file_name[0:file_name.rfind("src")]

		if sublime.platform() == "windows":
			simulatorPath = workdir+"/runtime/win32/PrebuiltRuntimeLua.exe"
		if sublime.platform() == "osx":
			simulatorPath = workdir+"/runtime/mac/PrebuiltRuntimeLua.app/Contents/MacOS/PrebuiltRuntimeLua Mac"

		args=[simulatorPath]
		args.append("-workdir")
		args.append(workdir)

		global process
		if process:
			try:
				process.terminate()
			except Exception:
				pass
		if sublime.platform()=="osx":
			process=subprocess.Popen(args)
		elif sublime.platform()=="windows":
			process=subprocess.Popen(args)









		