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

import os
import logging
import fnmatch
import codecs
from chameleon import PageTemplateFile
from docutils.core import publish_parts

class Template(object):
	
	def __init__(self, cms, section):
		self.cms = cms
		self.section = section

		source_dir = os.path.join(cms.SOURCE, os.path.sep.join(section.path_names))
		if not os.path.isdir(source_dir):
			logging.warning("Missing source directory: %s" % source_dir)

		self.sources = {}
		for l in os.listdir(source_dir):
			f = os.path.join(source_dir, l)
			if os.path.isfile(f) and l[0]!='.':
				self.sources[os.path.splitext(l)[0]] = f

		self.target_path = os.path.join(cms.BUILD, os.path.sep.join(section.path_names))
		self.target = os.path.join(self.target_path, 'index')+'.html'

		self.template = os.path.join(self.cms.TEMPLATES, section.template)+".html"
		if not os.path.isfile(self.template):
			logging.warning("Missing template: %s" % self.template)

	def generate(self):
		if not os.path.isdir(self.target_path):
			os.makedirs(self.target_path)

		contents = {}
		for name,sourcefile in self.sources.items():
			content = codecs.open(sourcefile, encoding='utf-8').read()
			if fnmatch.fnmatch(sourcefile, '*.rst'):
				contents[name] = body=publish_parts(
					content, 
					writer_name='html', 
					settings_overrides=dict(
						input_encoding='utf-8', 
						output_encoding='utf-8',
						doctitle_xform=False,
					)
				)['html_body']
			else:
				contents[name] = content

		logging.info("Creating: %s -(%s)-> %s" % (", ".join(self.sources.values()), self.template, self.target))
		taltemplate = PageTemplateFile(self.template)
		result = taltemplate(
				encoding='utf-8',
				cms=self.cms, 
				root=self.cms.navigation.root,
				content=contents,
				section=self.section, 
				)
		codecs.open(self.target, "w", encoding='utf-8').write(result)

