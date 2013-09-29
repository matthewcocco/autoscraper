# README.md for autoscraper

A library for searching Google and scraping the first 100 results.
Designed to be easy for non-programmers to use (when compiled as a windows binary)

## TL;DR:

This searches Google for keywords, looks through the first 100 (nonpersonalized) results,
and produces a `.csv` with the positions of specific domains. You can set up the keywords 
and domains yourself by creating two files, `keywords.txt` and `domains.txt` in the same
folder as the script.

I provide the script and the `useragents.txt`, which contains a bunch of common useragents.

I make no guarantees regarding the accuracy of results, nor do I guarantee that this script
won't get you in trouble with Google or fry your computer. 

Things happen; use this (and/or its derivatives) at your own risk.

----------

I built this in Python 2.7.4; you will need the `lxml` and `requests` libraries.

Files necessary for proper operation:

+ `Autoscraper.py`
+ `keywords.txt`
+ `domains.txt`
+ `useragents.txt`

I have included `example_keywords.txt`, `example_domains.txt`, and `example_31-Jul-2013.results.csv`.

You could rename these to `keywords.txt` and `domains.txt`, 
and then run `Autoscraper.py` to test it for yourself.

----------

## Usage:

Using Autoscraper should be easy;

import Autoscraper, 
create an Autoscraper object,
tell the Autoscraper object to execute.

    import Autoscraper
    fizz = Autoscraper()
    fizz.execute()

It's that easy.

This will assume that you just want the default settings.

Expected to be found in the same directory:

+ `keywords.txt`
+ `domains.txt`
+ `useragents.txt`

and the resulting [ .csv ] will be named in the format `DD-MMM-YYYY_results.csv`.

### Usage of configuration files

`keywords.txt` should have one 'set' of keywords you wish to search per line - what you'd enter into 
  the google search form before hitting 'Return' or 'Enter'.

`domains.txt` should have the domains that you'd like to find in the results - one domain per line.
  don't add `http://` or `/path/to/a/page`, either - just use something like: 

+ `google.com`
+ `yahoo.de`
+ `reddit.com`
