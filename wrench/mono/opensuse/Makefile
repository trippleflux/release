API_UPLOAD := rsync -tz --delay-updates *.dll mono-api-upload@go-mono.com:~mono-web/go-mono/status/binary
MONO_BUILD := /home/builder/rpmbuild/BUILD/mono-*

#TARBALL_PATH=$BUILD_DATA_LANE/$(echo $BUILD_REVISION | head -c 8)/dependencies/mono-dist-master
#TARBALL=$(find $TARBALL_PATH -name 'mono-*.tar.*')
#NAME=$(basename $TARBALL)

.configure:
	@rm -rf $(MONO_BUILD)
	cd mono && ./autogen.sh

.make:
	cd mono && make dist-bzip2 && rpmbuild -ta mono-*.tar.bz2
	# Delete our source tree here and symlink in the tree we just built
	# This means we can run the tests from the tree we actually built
	rm -rf mono && ln -s $(MONO_BUILD) ./mono

.package:
	@mkdir -p package
	find /home/builder/rpmbuild/ -type f -name "*.rpm" -exec mv {} package/ ';'

.upload:
	cd $(MONO_BUILD)/mcs/class/lib/net_2_0 && $(API_UPLOAD)/2.0
	cd $(MONO_BUILD)/mcs/class/lib/net_4_0 && $(API_UPLOAD)/4.0
	cd $(MONO_BUILD)/mcs/class/lib/net_4_5 && $(API_UPLOAD)/4.5

include wrench.make
