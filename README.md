# PGI
A Python Script that compress PDF via Ghostscript and Imagemagick

What is missing: Right now, the script leverage too much on RAM which causes the host to use swap memory, which in return makes too slow the conversion. The cheapest solution is to iterate, before or after the conversion of each page of the PDF.

Update: Right now it uses less RAM but the disk writes are now for Bitmaps and for individual PDFs, maybe there could be a way to catch the fileoutput of ghostscript and imagemagick in memory per file and avoid completly disk writes, and make all the "heavy work" in ram.
