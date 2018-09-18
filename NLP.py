#!/usr/bin/env python
# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import argparse
import sys
import textwrap

import googleapiclient.discovery


def dependents(tokens, head_index):
    """Returns an ordered list of the token indices of the dependents for
    the given head."""
    # Create head->dependency index.
    head_to_deps = {}
    for i, token in enumerate(tokens):
        head = token['dependencyEdge']['headTokenIndex']
        if i != head:
            head_to_deps.setdefault(head, []).append(i)
    return head_to_deps.get(head_index, ())


def phrase_text_for_head(tokens, text, head_index):
    """Returns the entire phrase containing the head token
    and its dependents.
    """
    begin, end = phrase_extent_for_head(tokens, head_index)
    return text[begin:end]


def phrase_extent_for_head(tokens, head_index):
    """Returns the begin and end offsets for the entire phrase
    containing the head token and its dependents.
    """
    begin = tokens[head_index]['text']['beginOffset']
    end = begin + len(tokens[head_index]['text']['content'])
    for child in dependents(tokens, head_index):
        child_begin, child_end = phrase_extent_for_head(tokens, child)
        begin = min(begin, child_begin)
        end = max(end, child_end)
    return (begin, end)


def analyze_syntax(text):
    """Use the NL API to analyze the given text string, and returns the
    response from the API.  Requests an encodingType that matches
    the encoding used natively by Python.  Raises an
    errors.HTTPError if there is a connection problem.
    """
    service = googleapiclient.discovery.build('language', 'v1beta1')
    body = {
        'document': {
            'type': 'PLAIN_TEXT',
            'content': text,
        },
        'features': {
            'extract_syntax': True,
        },
        'encodingType': get_native_encoding_type(),
    }
    request = service.documents().annotateText(body=body)
    return request.execute()


def get_native_encoding_type():
    """Returns the encoding type that matches Python's native strings."""
    if sys.maxunicode == 65535:
        return 'UTF16'
    else:
        return 'UTF32'


def find_triples(tokens,
                 head_part_of_speech='VERB',
                 right_dependency_label='DOBJ'):
    """Generator function that searches the given tokens
    with the given part of speech tag, that have dependencies
    with the given labels.  For each such head found, yields a tuple
    (left_dependent, head, right_dependent), where each element of the
    tuple is an index into the tokens array.
    """

    for head, token in enumerate(tokens):

        if token['partOfSpeech']['tag'] == head_part_of_speech:
            children = dependents(tokens, head)
            right_deps = []
            for child in children:
                child_token = tokens[child]
                child_dep_label = child_token['dependencyEdge']['label']
                if child_dep_label == right_dependency_label:
                    right_deps.append(child)
            for right_dep in right_deps:
                yield (head, right_dep)



def find_verb_noun(tokens):
    verb_list = []
    noun_list = []
    all_list = []
    for head, token in enumerate(tokens):
        if token['partOfSpeech']['tag'] == 'VERB' and token['dependencyEdge']['label'] != 'NSUBJ' and token['lemma']!= 'be' :
            verb_list.append(token['text']['content'])
            all_list.append(token['text']['content'])

        if token['partOfSpeech']['tag'] == 'NOUN':
            noun_list.append(token['text']['content'])
            all_list.append(token['text']['content'])

    return verb_list, noun_list,all_list


def show_triple(tokens, text, triple):
    """Prints the given triple (left, head, right).  For left and right,
    the entire phrase headed by each token is shown.  For head, only
    the head token itself is shown.

    """
    #nsubj, verb, dobj = triple
    verb, dobj = triple

    # Extract the text for each element of the triple.
    #nsubj_text = phrase_text_for_head(tokens, text, nsubj)
    verb_text = tokens[verb]['text']['content']
    dobj_text = phrase_text_for_head(tokens, text, dobj)

    left = textwrap.wrap(verb_text, width=10)
    right = textwrap.wrap(dobj_text, width=28)
    parsed_string = left[0]+' '+right[0]
    return parsed_string
    #print (parsed_string)


def main(text):
    # Extracts subject-verb-object triples from the given text file,
    # and print each one.
    parsed_string = None
    analysis = analyze_syntax(text)
    tokens = analysis.get('tokens', [])
    verb_list, noun_list,all_list = find_verb_noun(tokens)
    for triple in find_triples(tokens):
        parsed_string = show_triple(tokens, text, triple)

    if parsed_string != None:
        parsed_analysis = analyze_syntax(parsed_string)
        parsed_tokens = parsed_analysis.get('tokens', [])
        parsed_verb_list, parsed_noun_list, parsed_all_list = find_verb_noun(parsed_tokens)
        print(parsed_all_list)
    else:
        print(all_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'text_file',
        help='A file containing the document to process.  '
        'Should be encoded in UTF8 or ASCII')
    args = parser.parse_args()
    main(args.text_file)
