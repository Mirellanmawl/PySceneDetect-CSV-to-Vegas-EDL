# PySceneDetect-CSV-to-Vegas-EDL
Convert PySceneDetect CSV files to Vegas EDL files.


This is a Python 3 script that reads a comma-separated values (CSV) file generated by PySceneDetect, and creates a Vegas Edit Decision List (EDL) (which is a txt text file) from it which you can use as a base for a Sony Vegas/Vegas Pro project (possibly other NLEs as well).

Useful for when editing already-cut material such as achive footage, fan editing, Anime Music Video (AMV) making, or removing commercial breaks from TV broadcast footage, amongst other things.

This is, so far, a quick and dirty script mainly for personal use, and as such you will have manually change variables in the script for it to work with your CSV and media file. It will likeley contain style errors and such. However it works on my machine.
The variables you need to change are "infile", "outfile" and "media".

This was created with Python 3.6.1 (v3.6.1:69c0db5, Mar 21 2017, 18:41:36) [MSC v.1900 64 bit (AMD64)] on win32 with Emacs and Elpy.
