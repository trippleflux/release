#!/usr/bin/env python

# Probably will only build HEAD packages for now...  No reason it couldn't build RELEASE... ?

# TODO: Logging
# TODO: Prioritize builds: Maybe there should be one thread per jail, and that thread chooses a tarball to build, and prioritizes.  That way, there are no wait times for startup (we'll only sleep when there are no tarballs available to build) But, if we have jail multiplicity, the current design would be better, or we just start another thread for the mirror jail?
# Possible TODO: For the slower build platforms, we could check to make sure the build succeeded on i386 before starting... ?

import sys
import os
import threading
import time
import re
import signal

import pdb

sys.path += [ '../pyutils' ]

import config
import datastore
import packaging
import utils

# regex to grab version out of filename
# This only follows standards by autotools for now...
version_re = re.compile(".*-(.*).(tar.gz|tar.bz2|zip)")

tarballs = datastore.source_file_repo()


class jail_scheduler(threading.Thread):

	def __init__(self, distro):
		threading.Thread.__init__(self)

		self.distro = distro

		self.setName(distro)

	def exit_if_interrupted(self):
		if sigint_event.isSet():
			# TODO: what's the best way to exit a thread? _exit?  return?
			print "%s:\tExiting because of user interruption" % self.distro
			sys.exit(1)

	def run(self):

		distro = self.distro
		print "%s:\tStarting scheduler" % (distro)

		while True:
			# Reload config info (only useful for sleep times and which packages to build for a distro)
			reload(config)

			packages_to_build = []
			for pack_def in config.sd_latest_build_packages:
				pack_obj = packaging.package("", pack_def)
				if pack_obj.valid_build_platform(distro):
					packages_to_build.append(pack_def)

			num_started_builds = 0
			start_time = utils.get_time()

			# Build each package for this jail
			for package_name in packages_to_build:

				self.exit_if_interrupted()

				# Check to see what the latest tarball is
				tarball_filename = tarballs.get_latest_tarball("HEAD", package_name)

				if not tarball_filename:
					print "%s:\t*** Error getting latest tarball (%s) (Probably doesn't exist...)!!!" % (distro, package_name)

				else:

					#print "Latest tarball: " + tarball_filename

					# Get version
					version, ext = version_re.search(tarball_filename).groups()

					info = datastore.build_info("HEAD", distro, package_name, version)

					# Build if the build doesn't exist already
					if not info.exists:
						command = "cd %s; ./build %s %s %s" % (config.packaging_dir, distro, package_name, version)
						print "%s:\t%s" % (distro, command)

						num_started_builds += 1
						# TODO: hmm... is this not blocking?  Seems this code continues before being able to run tests?
						(code, output) = utils.launch_process(command, print_output=0)
						# Testing...
						#code = 2
						
						# Is the jail busy?  if so, just repeat this loop (and select a new tarball if a newer one exists)	
						# Hmm... this really shouldn't happen, as much at least
						if code == 2:
							print "%s:\tJail is busy or offline... will retry again (%s)" % (distro, package_name)
							num_started_builds -= 1

						if code == 5:
							print "%s:\tbuild info is missing, but packages exist... ?? will retry again (%s)" % (distro, package_name)
							num_started_builds -= 1
					else:
						print "%s:\tSkipping existing build (%s, %s)" % (distro, package_name, version)


			time_duration = utils.time_duration_asc(start_time, utils.get_time() ) * 60
			if num_started_builds == 0 and time_duration < config.sd_wakeup_interval:
				print "%s:\tSleeping %d seconds..." % (distro, config.sd_wakeup_interval - time_duration)
				time.sleep(config.sd_wakeup_interval - time_duration)



# Signal handler routine
#  This will let each thread finish when CTRL-C is pushed
def keyboard_interrupt(signum, frame):
	print "*** Signaling threads to finish ***"
	sigint_event.set()

# Set up event object
sigint_event = threading.Event()

# Set signal handler
signal.signal(signal.SIGINT, keyboard_interrupt)
threads = []

for distro in config.sd_latest_build_distros:
	thread = jail_scheduler(distro)
	thread.start()

	# For debugging (This will run each thread one at a time)
	#thread.run()

	threads.append(thread)

# Sleep if threads are still alive
#  Wow... here was the key... the main thread would exit, but pressing ctrl-c would go to the main thread (which had already exited)
#  source: http://groups.google.com/group/comp.lang.python/browse_thread/thread/bb177d4cff9cde4e/d39dbc7e71a897c2?lnk=st&q=threading+sigint+group%3Acomp.lang.python&rnum=4&hl=en#d39dbc7e71a897c2
for thread in threads:
	while thread.isAlive():
		#print "Waiting for thread %s ..." % thread.getName()
		time.sleep(1)

# Wrong!!
# This results blocks the main thread (and thus sigint gets ignored)
#for thread in threads:
#	thread.join()


