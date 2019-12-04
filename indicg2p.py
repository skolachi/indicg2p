
import argparse
import pandas as pd
import re
import textwrap
from unicodedata import *

language_prefixes = {'dev':{'hin':'09','tel':'0C','pan':'0A','ori':'0B','mal':'0D','mar':'09','san':'09'},
        'ben':{'ben':'09','guj':'0A','kan':'0C','tam':'0B','sin':'0D'}}

#maps = {'roman':'indicg2roman.map','sampa':'indicg2sampa.map','ipa':'indicg2ipa.map','wx':'indicg2wx.map'}

def extract_langcharmap(df,charset,lang):
    if lang in language_prefixes['dev']:
        chars = list(zip(df[charset].tolist(),df['Devnagari'].tolist()))
        lang_chars = [str(language_prefixes['dev'][lang]+c[1][2:]) for c in chars]
    elif lang in language_prefixes['ben']:
        chars = list(zip(df[charset].tolist(),df['Bengali'].tolist()))
        lang_chars = [str(language_prefixes['ben'][lang]+c[1][2:]) for c in chars]
  
    return chars, lang_chars

def extract_charmap(charset,lang):
    filename = 'indicg2p.map'
    df = pd.read_csv(filename,sep=',')
    #print(df.isna())
    chars, lang_chars = extract_langcharmap(df,charset,lang)
    g2pmap = {}
    for c1,c2 in zip(chars,lang_chars):
        #if c1[0] == 'NONE':c1[0] = ''
        g2pmap[(eval('u"\\u%s"'%(c1[1])),eval('u"\\u%s"'%(c2)))] = str(c1[0]).strip()
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

def convert(text,charset,lang):
    charmap = extract_charmap(charset,lang=lang)
    charmap_groups = group_charmap(charmap)
    print(charmap_groups['maatra'],charmap_groups['diacritic'])
    for k in charmap.keys():
        if k not in charmap_groups['maatra']:
            text = text.replace(k[1],charmap[k])

    for k in charmap_groups['diacritic']:
        if 'ANUSVARA' in name(k[0]).split():
            text = text.replace('%s'%(k[1]),charmap[k])
        if 'NUKTA' in name(k[0]).split():
            text = text.replace('%s'%('a'+k[1]),charmap[k])

    for k in charmap_groups['maatra']:
        if k not in charmap_groups['diacritic']:
            text = text.replace('%s'%('a'+k[1]),charmap[k])
                
    return text

help_lines = ['Languages supported','ben:Bangla','dev:Devnagari (Hindi, Marathi, Sanskrit)','guj:Gujarati','kan:Kannada',
              'mal:Malayalam','ori:Oriya','pan:Gurmukhi Punjabi','sin:Sinhala','tam:Tamil','tel:Telugu']

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--infile",help="input file",required=True)
    parser.add_argument("--charset",choices=['ipa','sampa','wx'],help="transliteration scheme",required=True)
    parser.add_argument("--lang",choices=['ben','dev','guj','hin','kan','mal','mar','ori','pan','san','sin','tam','tel'],required=True,help=textwrap.dedent('''\
                                                                                                                Languages supported
                                                                                                                ben:Bangla
                                                                                                                guj:Gujarati
                                                                                                                hin:Hindi
                                                                                                                kan:Kannada
                                                                                                                mal:Malayalam
                                                                                                                mar:Marathi
                                                                                                                ori:Oriya
                                                                                                                pan:Gurmukhi Punjabi
                                                                                                                san:Sanskrit
                                                                                                                sin:Sinhala
                                                                                                                tam:Tamil
                                                                                                                tel:Telugu
                                                                                                                '''))
    args = parser.parse_args()
    print(convert(open(args.infile).read(),args.charset,args.lang))

if __name__ == "__main__":
    main()
