#!/usr/bin/env python

import os
import os.path
import re
import sys
import urlparse

REGEX_SECTION = re.compile("^#+(.+?)#*$", flags=re.MULTILINE)
REGEX_BOOKMARK = re.compile("\[([^\[\]]+?)\]\(#([^\(\)]+?)\)", flags=re.MULTILINE)
REGEX_WIKILINK = re.compile("\[\[([^\[\|\]]+?)\|([^\[\|\]]+?)\]\]", flags=re.MULTILINE)

def section_name_to_id(name):
    """
        Converts the provided section name to a section ID.

        Parameters
            name: str, required
               The section name to convert into a section ID.

        Returns
           The section name converted into a section ID. 
    """
    return name.strip().lower().replace(' ', '-').replace('/', '').replace('+', '-').replace('<', '-').replace('>', '-').replace('.', '')

def enum_files(path):
    """
        Enumerates the Markdown files inside the directory specified by the provided `path` variable.

        Parameters
            path: str, required
                The path to the directory to be enumerated for Markdown files.

        Returns
            The list of Markdown files found inside the directory specified by the provided `path` variable.
    """
    items = []
    try:
        for item in os.listdir(path):
            item = path + '/' + item
            if os.path.isdir(item):
                for subitem in enum_files(item):
                    items.append(subitem)
                continue
            if item.endswith('.md'):
                items.append(item)
    except: pass
    return items

if __name__ == '__main__':

    if not os.path.isdir('.git'):
        print 'Error: ' + __file__ + ' must be executed inside a Git repository!'
        sys.exit(0)
    
    # enumerate files
    names = enum_files('.')

    # perform name uniqueness checks first
    all_unique = True
    for name in names:
        article = '.'.join(name.split('/')[-1].split('.')[:-1])

        unique = True
        for n in names:
            if n != name:
                a = '.'.join(n.split('/')[-1].split('.')[:-1])
                if a == article:
                    unique = False
                    all_unique= False
                    break

        if not unique:
            print
            print "  WARNING: Non-unique Article Names                                            "
            print "    Files                                                                      "
            print "      " + name
            print "      " + n
            print "    Description                                                                "
            print "      All article names in a GitHub Wiki must be unique even if they are in    "
            print "      different directories. The script will be unable to perform further      "
            print "      checks on the Wiki until all article names are unique.                   "
            print

    if not all_unique:
        sys.exit(0)

    # extract information from files
    articles = {}
    for name in names:

        # prepare info caches
        sections = {}       # section-id : row-num
        bookmarks = {}      # row-num : [section-id]
        links = {}          # row-num : article : [section-id]

        # read data
        with open(name, 'r') as handle:
            row = 0
            for line in handle.readlines():
                
                # extract sections
                match = REGEX_SECTION.findall(line)
                for section in match:
                    section = section_name_to_id(section)
                    original = section
                    offset = 1
                    while section in sections:
                        section = original + '-' + str(offset)
                        offset += 1
                    sections[section] = row
                
                # extract bookmarks
                match = REGEX_BOOKMARK.findall(line)
                for label, section in match:
                    if row not in bookmarks:
                        bookmarks[row] = []
                    if section not in bookmarks[row]:
                        bookmarks[row].append(section)
                
                # extract links
                match = REGEX_WIKILINK.findall(line)
                for label, link in match:
                    url = urlparse.urlparse(link)
                    if url.scheme is not None:
                        continue
                    if row not in links:
                        links[row] = {}
                    split = link.split('#', 1) 
                    if len(split) == 1:
                        article = split[0]
                        if article == '': article = None
                        section = None
                    else:
                        article, section = split
                        if article == '': article = None
                        if section == '': section = None
                    if article not in links[row]:
                        links[row][article] = []
                    if section not in links[row][article]:
                        links[row][article].append(section)

                # next row
                row += 1

        # collate information
        articles[name] = {
            'sections': sections,
            'bookmarks': bookmarks,
            'links': links
        }

    # perform reference checks
    for name in articles:

        # perform bookmark reference checks
        sections = articles[name]['sections']
        bookmarks = articles[name]['bookmarks']
        article = '.'.join(name.split('/')[-1].split('.')[:-1])
        for row in bookmarks:
            for section in bookmarks[row]:
                if section not in sections:
                    # TODO: flag sections with capital letters
                    print
                    print "  WARNING: Missing Section Reference                                           "
                    print "    File                                                                       "
                    print "      " + name
                    print "    Line                                                                       "
                    print "      " + str(row + 1)
                    print "    Target                                                                     "
                    print "      " + article + '#' + section
                    print "    Description                                                                "
                    print "      The section being referred to by a link does not exist.                  "
                    print
        
        # perform wikilink reference checks
        links = articles[name]['links']
        for row in links:
            for article in links[row]:
                for section in links[row][article]:
                    found = False
                    for n in articles:
                        a = '.'.join(n.split('/')[-1].split('.')[:-1])
                        if a == article:
                            found = True
                            # TODO: flag sections with capital letters
                            if section is not None and section not in articles[n]['sections']:
                                print
                                print "  WARNING: Missing Section Reference                                           "
                                print "    File                                                                       "
                                print "      " + name
                                print "    Line                                                                       "
                                print "      " + str(row + 1)
                                print "    Target                                                                     "
                                print "      " + article + '#' + section
                                print "    Description                                                                "
                                print "      The section being referred to by a link does not exist.                  "
                                print
                    if not found:
                        # TODO: flag sections with capital letters
                        print
                        print "  WARNING: Missing Article Reference                                           "
                        print "    File                                                                       "
                        print "      " + name
                        print "    Line                                                                       "
                        print "      " + str(row + 1)
                        print "    Target                                                                     "
                        print "      " + article + ('#' + section) if section is not None else ""
                        print "    Description                                                                "
                        print "      The article being referred to by a link does not exist.                  "
                        print
