# Copyright (c) 2012, Christoph Frick
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the <organization> nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import xml.dom.minidom

class Navigation(object):

	def __init__(self, filename):
		self.dom = xml.dom.minidom.parse(filename)
		self.root = Section(None, self.dom.getElementsByTagName('section')[0])

class Section(object):
	def __init__(self, parent, node):
		self.parent = parent
		self.childs = []
		self.name = None
		self.title = None
		self.template = None

		for attribute in ('name', 'title', 'template', ):
			if node.hasAttribute(attribute):
				setattr(self, attribute, node.getAttribute(attribute))

		assert self.name is not None, "name missing within %s: %s" % (self.url_path, node.toxml())

		if self.title is None:
			self.title = self.name

		self.path = []
		p = self
		while p:
			self.path.append(p)
			p = p.parent
		self.path.pop() # drop root
		self.path.reverse()

		self.path_names = [s.name for s in self.path]

		self.url_path = '/'+'/'.join(self.path_names)

		self.parents = self.path[:-1]

		if self.template is None and self.parent is not None:
			self.template = self.parent.template
		if self.template is None:
			self.template = "default"

		for childNode in node.childNodes:
			if childNode.nodeType==childNode.ELEMENT_NODE and childNode.tagName=='section':
				self.childs.append(Section(self, childNode))

		self.child_by_name = {}
		for child in self.childs:
			self.child_by_name[child.name] = child

	def __getattr__(self, key):
		return self.child_by_name[key]
