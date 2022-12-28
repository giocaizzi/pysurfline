# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

github:
	@make html
	@cp -a build/html/. ../docs
	@touch ../docs/.nojekyll
	@open ../docs/index.html 

gitclean:
	@make clean
	@rm -r source/_autosummary
	@rm -r ../docs/*

#This will cause the build to fail immediately when a warning is encountered.
# If you add --keep-going then the docs build will still fail but it will run 
# to completion so you can see all the warnings
github-action:
	@make html SPHINXOPTS="-W --keep-going"
	@cp -a build/html/. ../docs
	@touch ../docs/.nojekyll