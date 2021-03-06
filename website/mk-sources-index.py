#!/usr/bin/env python

import sys
import os
import distutils.dir_util
import re

import pdb

sys.path += [ '../pyutils' ]

import shell_parse
import packaging
import config

# Command line options
try:
	(script_name, bundle, output_dir, sources_dir) = sys.argv
except:
	print "Usage: ./mk-sources-index.py <bundle name> <output webdir> <sources_dir>"
	sys.exit(1)

bundle_conf = packaging.bundle(bundle_name=bundle)

# Create url dirs
distutils.dir_util.mkpath(output_dir + os.sep + "sources-" + bundle_conf.info['bundle_urlname'])
distutils.dir_util.mkpath(os.path.join(output_dir, "archive", bundle_conf.info['archive_version'], 'sources'))

out = open(os.path.join(output_dir, 'sources-' + bundle_conf.info['bundle_urlname'], 'index.html'), 'w')
arc_out = open(os.path.join(output_dir, 'archive', bundle_conf.info['archive_version'], 'sources', 'index.html'), 'w')

fd = open(os.path.join(config.release_repo_root, 'website', 'sources-index'))
template = fd.readlines()
fd.close()

for line in template:
	line_items = line.split()
	if line_items and line_items[0] == "#":
		args = line_items[1:]
		tarballs = []
		for pack in args:
			pack_obj = packaging.package("", pack, bundle_obj=bundle_conf, source_basepath=sources_dir)
			try:
				source_file = pack_obj.get_source_file()
			except IndexError:
				# TODO: Sort of a hack...
				# There's no source for this module
				source_file = ''
			# Skip if there is no source for this bundle
			if source_file:
				tarballs.append(source_file)

		print tarballs

		out.write("<ul>\n")
		arc_out.write("<ul>\n")
		for i in tarballs:
			n = os.path.basename(i)
			s = os.path.basename(sources_dir)
			out.write("<li><a href='../%s/%s'>%s</a></li>\n" % (s, i, n))
			arc_out.write("<li><a href='../../../%s/%s'>%s</a></li>\n" % (s, i, n))

		out.write("</ul>\n")
		arc_out.write("</ul>\n")

	else:
		line = line.replace("[[version]]", bundle_conf.info['archive_version'])
		o_line = line.replace("[[webroot_path]]", "..")
		arc_oline = line.replace("[[webroot_path]]", "../../..")

		out.write(o_line)
		arc_out.write(arc_oline)


out.close()
arc_out.close()
