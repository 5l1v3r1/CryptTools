#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, "../lib")
from utils import *
from validator import *
import argparse
import enchant

def caesar(text, shift):
    """Encrypts/Decrypts a `text` using the caesar substitution cipher with specified `shift` key"""
    if shift < 0 or shift > MODULE:
        error(f"key must be between 0 and {MODULE}")
    return ''.join(map(lambda char: shift_by(char, shift), text))

def crack(text):
    """Cracks the text that must be encrypted with the caesar cipher"""
    most_frequent = ord(most_frequent_char(text))
    if args.verbose:
        print(f"Most frequent character: {chr(most_frequent)}")
    for i in range(MODULE):
        possible_original = ord(FREQUENCY_ALPHABET[i])
        shift = possible_original - most_frequent
        if shift < 0:
            shift += MODULE
        decrypt = caesar(text, shift)
        if args.verbose:
            sys.stdout.write("\r")
            sys.stdout.write(f"Testing '{chr(possible_original)}' (ROT-{shift})       ")
            sys.stdout.flush()
        if args.all:
            print(f'Testing decrypted text:\n"{decrypt}"')
        if args.verbose and args.debug:
            print()
        if validator.is_valid(decrypt):
            if args.verbose:
                validator.success()
                if args.debug:
                    print()
                print(f'Decrypted with ROT-{shift}. Original encryption key: {(MODULE - shift)%MODULE}')
            print(decrypt)
            return
        if args.debug:
            print()
    if args.verbose and not args.debug:
            print()
    validator.fail()

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--text", help="text to read from. If not specified the program will read from standard input")
parser.add_argument("-k", "--key", help="key used to encrypt. If no key is provided the program will try to crack and decrypt using the specified language", type=int)
parser.add_argument("-l", "--lang", help=f"available languages: {enchant.list_languages()} (default: en_US). Only useful if no key is provided", default='en_US')
parser.add_argument("-V", "--verbose", action='store_true', help="show extra information")
parser.add_argument("-A", "--all", action='store_true', help="show decrypted text for each tested key")
parser.add_argument("-D", "--debug", action='store_true', help="show information about text validation")
parser.add_argument("-T", "--threshold", help="valid word count percentage to mark the whole text as valid language (default: 50)", type=int, default=50)
parser.add_argument("--beep", action='store_true', help="plays a beep sound when program finishes. May require SOX to be installed")
args = parser.parse_args()

validator = Validator(args.lang, args.threshold, args.debug, args.beep)
text = read(args.text)

if args.key is not None:
    if args.verbose:
        print(f"Original text most frequent characters: {most_frequent_chars(text)}\n")
    encrypted = caesar(text, args.key)
    print(encrypted)
    if args.verbose:
        print(f"\nEncrypted text most frequent characters: {most_frequent_chars(encrypted)}")
else:
    crack(text)
