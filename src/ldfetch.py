#!/usr/bin/env python3

"""
Fetch linked data statements
"""

import argparse
import os
import string
import sys
import urllib.request
import time

class LDSource:
    def __init__(self, name, base_url, formats, url_template):
        self.name = name
        self.base_url = base_url
        self.formats = formats
        self.url_template = url_template
    def get_url(self, id, format):
        self.url_template.format(base_url=self.base_url, id=id, format=format)
        
ld_sources = {
   'tgn':  LDSource('tgn', 'http://vocab.getty.edu/tgn/',
                    ['json', 'jsonld', 'rdf', 'ttl', 'nt'], '{base_url}{id}.{format}'),
   'ulan': LDSource('ulan', 'http://vocab.getty.edu/ulan/',
                    ['json', 'jsonld', 'rdf', 'ttl', 'nt'], '{base_url}{id}.{format}'),
}
        
def parse_arguments(arguments):
    """parse command-line arguments and return a Namespace object"""
    global ld_sources
    
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    #parser.add_argument('infile', help="Input file", type=argparse.FileType('r'))
    parser.add_argument('vocabulary', nargs=1,
                        help="vocabulary to harvest, legal values are: " + ', '.join(ld_sources.keys()))
    parser.add_argument('format', nargs=1,
                        help="format for retreived data")
    parser.add_argument('id', nargs='*', help="IDs to retrieve, read from stdin if no IDs on command line")
    parser.add_argument('-p', '--pause', type=int, default=3,
                        help="sleep (seconds) between requests")
    parser.add_argument('-o', '--outfile', help="Output file",
                        default=sys.stdout, type=argparse.FileType('w'))
    args = parser.parse_args(arguments)
    #print(args)
    
    # Sanity check arguments:
    # ... check vocabulary
    vocab = args.vocabulary[0]
    #print('vocab: ' + vocab)
    if vocab not in ld_sources:
        tmpl = "Unuspported vocabulary {vocab}; supported vocabularies are: {vocab_list}"
        msg = tmpl.format(vocab=vocab, vocab_list=', '.join(iter(ld_sources.keys())))
        parser.exit(msg)
    # ... check format
    format = args.format[0]
    format_list = ld_sources[vocab].formats
    if format not in format_list:
        tmpl = "Format {format} not available for {vocabulary}, available formats are: {formats}"
        msg = tmpl.format(format=format, vocabulary=vocab,
                          formats=', '.join(iter(ld_sources[vocab].formats)))
        parser.exit(msg)
        
    return args

def main(arguments):
    global ld_sources

    args = parse_arguments(arguments)
    #print(args)
    id_iterator = args.id
    if len(id_iterator) == 0:
        id_iterator = sys.stdin
    for id in id_iterator:
        id = id.strip()
        # TODO: Replace print with fetching and output of the retrieved assertions
        print(id)
        if args.pause > 0:
            time.sleep(args.pause)
                    
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
