
import argparse
import re
from unicodedata import *

language_prefixes = {'dev':'09','telugu':'0C','gurmukhi':'0A','malayalam':'0D'}

def extract_charmap(filename='indicg2p.map',lang='dev'):
    g2pmap = {}
    chars = [f.strip().split(',') for f in open(filename)][1:]
    lang_chars = [language_prefixes[lang]+c[1][2:] for c in chars]
    for c1,c2 in zip(chars,lang_chars):
        if c1[0] == 'NULL':c1[0] = ''
        g2pmap[(eval('u"\\u%s"'%(c1[1])),eval('u"\\u%s"'%(c2)))] = c1[0]
    return g2pmap

def group_charmap(charmap):
    charmap_groups = {}
    charmap_groups['maatra'] = []
    charmap_groups['diacritic'] = []
    for k in charmap.keys():
        if 'ANUSVARA' in name(k[0]).split() or 'NUKTA' in name(k[0]).split():
            charmap_groups['diacritic'].append(k)
        if 'SIGN' in name(k[0]).split():
            charmap_groups['maatra'].append(k)

    return charmap_groups

def convert(text,lang):
    charmap = extract_charmap(lang=lang)
    charmap_groups = group_charmap(charmap)
    #print(charmap_groups['maatra'])
    for k in charmap.keys():
        if k not in charmap_groups['maatra']:
            text = text.replace(k[1],charmap[k])

    for k in charmap_groups['diacritic']:
        if charmap[k] == 'M':
            text = text.replace('%s'%(k[1]),charmap[k])
        if charmap[k] == 'za':
            text = text.replace('%s'%('a'+k[1]),charmap[k])

    for k in charmap_groups['maatra']:
        if k not in charmap_groups['diacritic']:
            text = text.replace('%s'%('a'+k[1]),charmap[k])
                
    return text

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--infile", help="input file",required=True)
    parser.add_argument("--lang", help="Language",required=True)
    args = parser.parse_args()
    print(convert(open(args.infile).read(),args.lang))

if __name__ == "__main__":
    main()
