#!/bin/bash
set -ex

OUTPUT=README.md

cat doc/about.md > $OUTPUT
cat doc/features.md >> $OUTPUT
cat doc/quick-start.md >> $OUTPUT
cat doc/how-it-works.md >> $OUTPUT
cat doc/vs-argparse.md >> $OUTPUT
cat doc/installation.md >> $OUTPUT
