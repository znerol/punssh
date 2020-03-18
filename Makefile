ifeq ($(prefix),)
    prefix := /usr/local
endif
ifeq ($(exec_prefix),)
    exec_prefix := $(prefix)
endif
ifeq ($(bindir),)
    bindir := $(exec_prefix)/bin
endif
ifeq ($(datarootdir),)
    datarootdir := $(prefix)/share
endif
ifeq ($(mandir),)
    mandir := $(datarootdir)/man
endif
ifeq ($(python),)
    python := python
endif

all: bin test doc

man1 := $(patsubst doc/%.1.rst,doc/_build/man/%.1,$(wildcard doc/*.1.rst))
man1_installed := $(patsubst doc/_build/man/%,$(DESTDIR)$(mandir)/man1/%,$(man1))

scriptdirs := bin $(wildcard lib/*hooks)
scripts := $(foreach dir,$(scriptdirs),$(wildcard $(dir)/*))
scripts_installed := \
    $(patsubst bin/%,$(DESTDIR)$(bindir)/%,$(filter bin/%,$(scripts))) \
    $(patsubst lib/%,$(DESTDIR)$(libdir)/certhub/%,$(filter lib/%,$(scripts)))

doc/_build/man/% : doc/%.rst
	${MAKE} -C doc man

bin: $(scripts)
	# empty for now

lint: bin
	flake8 $(scripts)

test: bin
	PATH="$(shell pwd)/bin:${PATH}" $(python) -m test

doc: $(man1)

clean:
	${MAKE} -C doc clean
	-rm -rf dist
	-rm -rf build

# Install rule for executables/scripts
$(DESTDIR)$(bindir)/% : bin/%
	install -m 0755 -D $< $@

# Install rule for manpages
$(DESTDIR)$(mandir)/man1/% : doc/_build/man/%
	install -m 0644 -D $< $@

install-doc: doc
	# empty for now

install-bin: bin $(scripts_installed)
	# empty for now

install: install-bin install-doc

uninstall:
	-rm -f $(man1_installed)
	-rm -f $(scripts_installed)

dist-bin:
	-rm -rf build
	${MAKE} DESTDIR=build prefix=/ install
	mkdir -p dist
	tar --owner=root:0 --group=root:0 -czf dist/punssh-dist.tar.gz -C build .

dist-src:
	mkdir -p dist
	git archive -o dist/punssh-src.tar.gz HEAD

dist: dist-src dist-bin
	cd dist && md5sum punssh-*.tar.gz > md5sum.txt
	cd dist && sha1sum punssh-*.tar.gz > sha1sum.txt
	cd dist && sha256sum punssh-*.tar.gz > sha256sum.txt

integration-test: dist
	${MAKE} -C integration-test all

.PHONY: \
	all \
	clean \
	dist \
	dist-bin \
	dist-src \
	install \
	install-bin \
	install-doc \
	integration-test \
	lint \
	test \
	uninstall \
