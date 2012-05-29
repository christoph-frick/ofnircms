ofnircms
========

Mini-CMS to create static pages by a XML structure, ReStructured Text and ZPT.

It sole purpose is to make creation of a simple page with focus in content
easier... well like a CMS.  But it focuses on developers and not on the end
user.

Get started
-----------

Copy the .py files in a new directory.  Then create the following files and
directories:

 src/structure.xml

It might look like this:

	<?xml version="1.0" encoding="utf-8"?>
	<structure>
		<section name="index" template="default" title="Home sweet home"/>
	</structure>

`name` and `title` are mandatory.  The `name` is used to create the file
hierarchy and it also used to find the section content files.  The `title` is
used for e.g. generating menus.  The `template` must be set on the root, but
is inherited to all childs.
	
Next add an index there:

 src/index.rst

Note: the suffix desides, how to deal with the file there.  Currently `.rst`
renders the content using docutils.  Everything else is provided verbatim to
the template.

This defines the structure.  Now that there is the template `default`
mentioned in the strucutre file we have to create it.

 templates/default.html

And it might look like this:

	<!DOCTYPE html>
	<html>
	<head>
		<meta charset="utf-8" />
		<title>${section.title}</title>
	</head>
	<body>
		<h1>${section.title}</h1>
		<section>
		${structure:content.index}
		</section>
	</body>
	</html>
	 
For each file generated there are the following vars:

[cms] The whole CMS object (see ofnircms.py)
[root] The root section
[content] A dict containing all the files (without subject) from the current section
[section] the current section (more or less the data from the structure.xml)

This sets up the whole thing.  No generate the pages by:

 python ofnircms.py

If everything is fine, it creates the `build` directory and an `index.html`.
You might want to automize thins further with a Makefile to e.g. upload to
your hosting site.

License
-------

	Copyright (c) 2012, Christoph Frick
	All rights reserved.
	
	Redistribution and use in source and binary forms, with or without
	modification, are permitted provided that the following conditions are met:
	    * Redistributions of source code must retain the above copyright
	      notice, this list of conditions and the following disclaimer.
	    * Redistributions in binary form must reproduce the above copyright
	      notice, this list of conditions and the following disclaimer in the
	      documentation and/or other materials provided with the distribution.
	    * Neither the name of the <organization> nor the
	      names of its contributors may be used to endorse or promote products
	      derived from this software without specific prior written permission.
	
	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
	ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
	WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
	DISCLAIMED. IN NO EVENT SHALL <COPYRIGHT HOLDER> BE LIABLE FOR ANY
	DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
	(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
	LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
	ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
	(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
	SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
