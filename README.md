# wikicheck
This is a simple GitHub Markdown Wiki Consistency Checker. This tool checks for the common mistakes that people usually make when writing down GitHub Markdown Wiki articles.

## Contents
1. [Usage](#usage)
2. [Checks](#checks)
3. [Contact](#contact)

## Usage
[[Back to Top](wikicheck)]

In order to use this tool on your GitHub Wiki, you first need to get your wiki cloned onto your machine, like so:
```
git clone https://github.com/<username>/<repository>.wiki.git
```

After that, download `wikicheck.py`, open a terminal, navigate to your cloned wiki repository, and invoke this tool, like so:
```
cd <repository>.wiki.git
python <path-to-wikicheck>/wikicheck.py
```

Upon invocation, the tool shall proceed to print the inconsistencies that it finds within your wiki onto the terminal window

## Checks
[[Back to Top](wikicheck)]

As of now, the following checks are performed by this tool:
* Checks for duplicate file names in different directories within the Wiki
* Checks for missing bookmark references
* Checks for missing WikiLink references

More checks shall be added onto this tool as I think up of more stuff.

## Contact
[[Back to Top](wikicheck)]

Contact me at `penafieljlm@gmail.com` if you have any concerns about this tool.
