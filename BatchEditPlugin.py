# -*- coding: utf-8 -*-

import sublime, sublime_plugin

import re

class BatchEditCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self._edit = edit
        self._replace_all(u"interface ", r"protocol ")
        self._replace_all(u" implements ", r" : ")
        # Interface method 
        self._replace_all(u"(\w*) (\w*)\(([\w, ]*)\);", r"func \2(\3) -> \1;")
        self._replace_all(u"public class", r"class")
        self._replace_all(u"public static final (String) (\S*)", r"static var \2 : \1")
        self._replace_all(u"DateTime", r"NSDate")
        self._replace_all(u"private (\w*) (\w*);", r"var \2 : \1")
        self._replace_all(u"public (\w*)\(([\w, ]*)\) \{", r"func init(\2) {")
        self._replace_all(u"public (\w*) (\w*)\(([\w, ]*)\) \{", r"func \2(\3) -> \1 {")
        

 
 
    def _get_file_content(self):
        return self.view.substr(sublime.Region(0, self.view.size()))

    def _update_file(self, doc):
        self.view.replace(self._edit, sublime.Region(0, self.view.size()), doc)

    def _replace_all(self, regex, replacement):
        doc = self._get_file_content()
        p = re.compile(regex, re.UNICODE)
        doc = re.sub(p, replacement, doc)
        self._update_file(doc)

    def _delete_line_with(self, regex):
        doc = self._get_file_content()
        lines = doc.splitlines()
        result = []
        for line in lines:
            if re.search(regex, line, re.UNICODE):
                continue
            result.append(line)
        line_ending = {
            "Windows" : "\r\n",
            "Unix"    : "\n",
            "CR"      : "\r"
        }[self.view.line_endings()]
        doc = line_ending.join(result)
        self._update_file(doc)