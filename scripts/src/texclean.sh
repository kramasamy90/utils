#!/bin/bash

# This script cleans up the temporary files created by LaTeX.
# Delete files with the following extensions:.aux, .bbl, .blg, .log, .out, .synctex.gz


find . -iname "*.aux" | xargs -I {} rm {}
find . -iname "*.bbl" | xargs -I {} rm {}
find . -iname "*.blg" | xargs -I {} rm {}
find . -iname "*.log" | xargs -I {} rm {}
find . -iname "*.out" | xargs -I {} rm {}
find . -iname "*.synctex.gz" | xargs -I {} rm {}
find . -iname "*.snm" | xargs -I {} rm {}
find . -iname "*.toc" | xargs -I {} rm {}
find . -iname "*.nav" | xargs -I {} rm {}