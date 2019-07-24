#!/bin/bash
set -ex

OUTPUT=README.md

cat doc/about.md > $OUTPUT
cat doc/features.md >> $OUTPUT
cat doc/quick-start.md >> $OUTPUT
cat doc/how-it-works.md >> $OUTPUT
cat doc/vs-argparse.md >> $OUTPUT
cat doc/installation.md >> $OUTPUT

cat doc/builder.md >> $OUTPUT
cat doc/subcommands.md >> $OUTPUT
cat doc/flags.md >> $OUTPUT
cat doc/parameters.md >> $OUTPUT
cat doc/positional-args.md >> $OUTPUT
cat doc/dictionaries.md >> $OUTPUT
cat doc/autocompletion.md >> $OUTPUT
cat doc/help.md >> $OUTPUT
cat doc/data-types.md >> $OUTPUT
cat doc/errors.md >> $OUTPUT
cat doc/cheatsheet.md >> $OUTPUT
