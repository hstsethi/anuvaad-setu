#!/bin/sh
for pdf in *.pdf; do

    pdftotext "$pdf"
done

