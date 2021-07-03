import os
import sys
from collections import OrderedDict


def read_tokens(path, tokens=None):
    with open(path, 'r') as sr:
         lines = sr.readlines()
         if tokens == None: tokens = {}
         for line in lines:
             items = line.split()
             for item in items:
                 if not item.endswith('@@'):
                        if item+"</w>" not in tokens:
                             tokens[item+"</w>"] = 1
                        else:
                             tokens[item+"</w>"] += 1
                 else:
                      if item not in tokens:
                           tokens[item] = 1
                      else:
                           tokens[item] += 1
    return tokens

def read_merge_code(path, tokens):
    merged_token = set([])
    with open(path, 'r') as sr:
         lines = sr.readlines()
         merge_dict = OrderedDict()
         for line in lines[1:]:
             merge = line.strip()
             items = merge.split(" ")
             token = "".join(items)
             if not token.endswith('</w>'):
                token = token+"@@"
             if token in tokens:
                merged_token.add(token)
                merge_dict[merge] = tokens[token]
             else:
                #print(merge)
                merge_dict[merge] = 10
    return merge_dict


def write(path,merge_code):
    with open(path, 'w') as sw:
        for code in merge_code:
            sw.write(code +" "+ str(merge_code[code]) + "\n")


def get_tokens(source_file, target_file, token_candidate_file, token_file):
    tokens = read_tokens(source_file)
    tokens = read_tokens(target_file, tokens=tokens)
    merge_code = read_merge_code(token_candidate_file, tokens)
    #write(token_file, merge_code)
    return merge_code