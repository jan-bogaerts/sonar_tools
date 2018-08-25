__author__ = 'Jan Bogaerts'
__copyright__ = "Copyright 2018, Elastetic"
__credits__ = []
__maintainer__ = "Jan Bogaerts"
__email__ = "jb@elastetic.com"
__status__ = "Development"  # "Prototype", or "Production"

"""
a small tool to convert files from the sonar corpus into raw text data (as it only comes annotated).
sonar source: https://ivdnt.org/downloads/taalmaterialen/tstc-sonar-corpus  (login: janb, pwd: you-know-what-the-default-one
warning: extremely large file
"""

import logging
logger = logging.getLogger(__name__)

import os
import untangle

SKIP_SPACE_BEFORE = [')', ',', '.', ':', '/']
SKIP_SPACE_AFTER = ['(', '#', ':', '/']

QUOTES = ["'", '"']
quote_count = 0

def process_paragraph(paragraph):
    prev_word = ''
    quote_count = 0
    text = ''
    for sentence in paragraph.s:
        for word_el in sentence.w:
            word = word_el.cdata
            if not prev_word == '' and (not word in SKIP_SPACE_BEFORE and not prev_word in SKIP_SPACE_AFTER):
                if not ((prev_word in QUOTES and quote_count % 2 == 1) or (word in QUOTES and quote_count % 2 == 1)):
                    text += ' '
            text += word
            prev_word = word
            if word in QUOTES:
                quote_count += 1
        prev_word = ''
        quote_count = 0
        text += ' '
    text += '\n'
    return text

def iterate_files(input_path, output_path):
    """
    iterate over all the sonar files and extract the text out of it. Store the raw text in a new file.
    :return: None
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    directory = os.fsencode(input_path)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".xml"):
            try:
                full_file = os.path.join(input_path, filename)
                obj = untangle.parse(full_file)
                text = ""
                if hasattr(obj.DCOI.text.body, 'div1'):
                    body = obj.DCOI.text.body.div1
                elif hasattr(obj.DCOI.text.body, 'div0'):
                    body = obj.DCOI.text.body.div0
                else:
                    body = obj.DCOI.text.body.div
                if type(body) is list:
                    for div in body:
                        if hasattr(div, 'head'):
                            if hasattr(div.head, 's'):
                                text = process_paragraph(div.head)
                            elif hasattr(div.head, 'cdata'):
                                text += div.head.cdata
                            text += '\n'
                        if hasattr(div, 'p'):
                            for paragraph in div.p:
                                text += process_paragraph(paragraph)
                else:
                    if hasattr(body, 'head'):
                        if hasattr(body.head, 's'):
                            text = process_paragraph(body.head)
                        elif hasattr(body.head, 'cdata'):
                            text += body.head.cdata
                        text += '\n'
                    if hasattr(body, 'p'):
                        for paragraph in body.p:
                            text += process_paragraph(paragraph)

                output_file = os.path.join(output_path, os.path.splitext(filename)[0] + '.txt')
                with open(output_file, 'w') as out:
                    out.write(text)
            except KeyboardInterrupt as key:
                exit(1)
            except:
                logger.exception("failed to convert file " + filename)




if __name__ == "__main__":
    # execute only if run as a script
    print("start")
    start_point = '../sonarCorpus/SoNaRCorpus_NC_1.2/SONAR500/DCOI/'
    for root, directories, filenames in os.walk(start_point):
        root_part = root[len(start_point):]
        for dir in directories:
            input_dir = os.path.join(root, dir)
            print(input_dir)
            output_path = os.path.join('.', 'output', root_part, dir)
            print(output_path)
            iterate_files(input_dir, output_path)
