#!/bin/bash
set -ex

OUTPUT=README.md

cat docs/about.md > $OUTPUT
cat docs/features.md >> $OUTPUT
cat docs/quick-start.md >> $OUTPUT
cat docs/how-it-works.md >> $OUTPUT
cat docs/vs-argparse.md >> $OUTPUT
cat docs/installation.md >> $OUTPUT

cat docs/builder.md >> $OUTPUT
cat docs/subcommands.md >> $OUTPUT
cat docs/flags.md >> $OUTPUT
cat docs/parameters.md >> $OUTPUT
cat docs/positional-args.md >> $OUTPUT
cat docs/many-args.md >> $OUTPUT
cat docs/dictionaries.md >> $OUTPUT
cat docs/autocompletion.md >> $OUTPUT
cat docs/help.md >> $OUTPUT
cat docs/data-types.md >> $OUTPUT
cat docs/errors.md >> $OUTPUT
cat docs/cheatsheet.md >> $OUTPUT
