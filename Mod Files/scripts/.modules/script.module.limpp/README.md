L.I.M.P.P.

Library of Image Manipulation in Pure Python

Wrote this forever ago because I needed a pure python method to handle various icon formats in a script for XBMC on XBox, and as a python learning exercise.

Thought I'd share it in case someone found it useful.

Reads PNG, BMP, ICO, TGA, XPM, XBM and DXTC textures.
Reads JPG via TonyJpegDecoder.py which was not written by me. See the file for its license.

Writes in PNG, BMP, TGA, XPM and XBM. (Note that the color selection algorithm for writing indexed images is lousy, so avoid it)

Does some simple image manipulation.

Beyond that, I can't remember anything about the code, so if you have a question about something,
your guess is as good as mine.

Also included is xbe.py which reads old XBox .xbe executable data, and with limpp can extract program and save icons.

I was learning python as I wrote this, so please excuse anything stupid :)

