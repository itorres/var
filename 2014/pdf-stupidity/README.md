# Synopsys

Cannot copy text from http://www.fbofill.cat/intra/fbofill/documents/publicacions/477.pdf

It's a free (as in beer) book, but someone decided to use funny options in the PDF writer and stack a copyright notice on it. Out of habit, I suppose.

The text cannot be copied. And when treated with text extraction software the resulting text is scrambled.

So I started to play and the result is in [https://github.com/itorres/junk-drawer/2014/pdf-stupidity](https://github.com/itorres/junk-drawer/2014/pdf-stupidity).

All referenced files are related to that path.

# Process

## First round (first/read.py)

Extract text using pdf2htmlEX. The resulting text is not correctly decoded and some extraneous characters appear in the resulting file (first/tribo.html)

There's an obvious `ord+31` for ascii characters. Extended characters are a completely different issue so we do a custom mapping.

This is enough for what we wanted, and we can use the text, but I'm intrigued so I go for a second round.

## Second round (second/read2.py)

Found some clues about the issue at hand:

  * [Adobe PDF Printer Outputs Scrambled Text][printer]
  * [The problem with PDF and glyphs][glyphs]

[glyphs]: http://www.glyphandcog.com/textext.html
[printer]: https://tokyoimage.wordpress.com/2011/05/05/adobe-pdf-printer-outputs-scrambled-text/

Extract a sane text dump with:

    pdftotext -enc UTF-8 source/tribo.pdf -f 73 -l 76 second/tribo.txt

With this some high values in the previous input are coherent and we can create a rule ( `255-(n-155)` ) for the translation of lowercase latin-1 characters.

According to the second article there's no rule for what will be the mapping used for glyphs. To me it seems to work by groups of characters. I would need more sources to check it out.

## Todo

I'm not sure if I will go for a third round. If I do I will make a utility to find unhandled characters.

# Other resources

[Unicode Table](http://unicode-table.com/en/)
