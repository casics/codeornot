#!/usr/bin/env python3
'''
language: Heuristically detect the human language of a text string

This module provides functions to guess at the human language in which a
given input string or list of strings is written in.

The function `human_language(text)` wll classify the string in 'text' and
return an ISO-639 2-letter language code, such as 'en' for English.  If the
text cannot be classified or is too short to reliably classify, this function
will return 'unknown'.  The input can also be a list of strings, in which case,
the function will concatenate them first before performing analysis.

The function `majority_language(list)` will independently analyze a list of
strings and report the most popular human language used across all the strings.
'''

import chardet
import ftfy
import locale
import os
import plac
import pycld2 as cld2
import re
import string
import sys


# Constants for this module.
# .............................................................................

_min_text_length = 30


# Main functions
# .............................................................................

def min_length():
    '''Return the minimum length of text for usable text analysis.  Text 
shorter than this length will yield "unknown".'''
    return _min_text_length


def human_language(text, enforce_length=False):
    '''Classify the string in 'text' and return an ISO-639 2-letter language
    code, such as 'en' for English.  If the text cannot be classified or is
    too short to reliably classify, this function will return 'unknown'.  If
    the input is an empty string or None, the value returned will be None.
    The input can also be a list of strings, in which case, they will be
    concatenated using ' '.join(text) before analysis is performed.

    Optional keyword argument 'enforce_length', if True, will cause this
    function to raise an exception if the text is shorter than an internal
    threshold for reliable analysis.  The default is False, which means that
    if the length is less than a certain minimum, the answer returned will
    always be "unknown".  Use the function `min_length()` to get the value
    of the minimum length threshold.
    '''
    def guessed_language(text):
        reliable, _, details = cld2.detect(text, bestEffort=True)
        return details[0][1] if details else None

    if not text:
        return None
    if isinstance(text, list) and len(text) >= 1:
        text = ' '.join(text)
    if len(text) < _min_text_length:
        if enforce_length:
            raise ValueError('Minimum text length for analysis is {} characters'
                             .format(_min_text_length))
        else:
            return 'unknown'
    try:
        # Clean up & normalize the text
        text = ftfy.fix_text(text)
        try:
            lang = guessed_language(text)
        except cld2.error as err:
            # This is likely a problem with characters that cld2 doesn't
            # understand.  Apply a sledgehammer and try again.
            text = ''.join(x for x in text if x in string.printable)
            lang = guessed_language(text)
        return lang if lang else "unknown"
    except Exception as err:
        return 'unknown'


def majority_language(string_list, enforce_length=False):
    '''Take a list of text strings, evaluate highest-probability language
    off each, and report the most popular of them all.

    Optional keyword argument 'enforce_length', if True, will cause this
    function to raise an exception if the text is shorter than an internal
    threshold for reliable analysis.  The default is False, which means that
    if the length is less than a certain minimum, the answer returned will
    always be "unknown".  Use the function `min_length()` to get the value
    of the minimum length threshold.
    '''
    if not isinstance(string_list, list):
        string_list = [string_list]
    langs = [human_language(string, enforce_length) for string in string_list]
    # Ignore unknown ones.
    langs = [lang for lang in langs if lang not in ['un', 'unknown']]
    if langs:
        return max(set(langs), key=langs.count)
    else:
        return 'unknown'


# The following codes were taken in 2017 from the Python ISO639 module by
# Mikael Karlsson, available on GitHub at https://github.com/noumar/iso639
#
# I couldn't get the Python iso639 package to load properly, and I can't
# figure out why.  I installed the package via pip for Python 3.4.
# Attempting to execute "from iso639 import languages" produced an error
# about the "languages" module being unknown, even though it's clearly there
# in in the source code and the package documentation says to load it this
# way.  I gave up and created a simple substitute for translating two-letter
# language codes into language names.
#
_language_codes = {
    'aa': 'Afar',
    'ab': 'Abkhazian',
    'ae': 'Avestan',
    'af': 'Afrikaans',
    'ak': 'Akan',
    'am': 'Amharic',
    'an': 'Aragonese',
    'ar': 'Arabic',
    'as': 'Assamese',
    'av': 'Avaric',
    'ay': 'Aymara',
    'az': 'Azerbaijani',
    'ba': 'Bashkir',
    'be': 'Belarusian',
    'bg': 'Bulgarian',
    'bh': 'Bihari',
    'bi': 'Bislama',
    'bm': 'Bambara',
    'bn': 'Bengali',
    'bo': 'Tibetan',
    'br': 'Breton',
    'bs': 'Bosnian',
    'ca': 'Catalan',
    'ce': 'Chechen',
    'ch': 'Chamorro',
    'co': 'Corsican',
    'cr': 'Cree',
    'cs': 'Czech',
    'cu': 'Church Slavic',
    'cv': 'Chuvash',
    'cy': 'Welsh',
    'da': 'Danish',
    'de': 'German',
    'dv': 'Divehi',
    'dz': 'Dzongkha',
    'ee': 'Ewe',
    'el': 'Greek',
    'en': 'English',
    'eo': 'Esperanto',
    'es': 'Spanish',
    'et': 'Estonian',
    'eu': 'Basque',
    'fa': 'Farsi',
    'ff': 'Fulah',
    'fi': 'Finnish',
    'fj': 'Fijian',
    'fo': 'Faroese',
    'fr': 'French',
    'fy': 'Western Frisian',
    'ga': 'Irish',
    'gd': 'Gaelic',
    'gl': 'Galician',
    'gn': 'Guarani',
    'gu': 'Gujarati',
    'gv': 'Manx',
    'ha': 'Hausa',
    'he': 'Hebrew',
    'hi': 'Hindi',
    'ho': 'Hiri Motu',
    'hr': 'Croatian',
    'ht': 'Haitian',
    'hu': 'Hungarian',
    'hy': 'Armenian',
    'hz': 'Herero',
    'ia': 'Interlingua',
    'id': 'Indonesian',
    'ie': 'Interlingue',
    'ig': 'Igbo',
    'ii': 'Sichuan Yi',
    'ik': 'Inupiaq',
    'io': 'Ido',
    'is': 'Icelandic',
    'it': 'Italian',
    'iu': 'Inuktitut',
    'ja': 'Japanese',
    'jv': 'Javanese',
    'ka': 'Georgian',
    'kg': 'Kongo',
    'ki': 'Kikuyu',
    'kj': 'Kuanyama',
    'kk': 'Kazakh',
    'kl': 'Kalaallisut',
    'km': 'Central Khmer',
    'kn': 'Kannada',
    'ko': 'Korean',
    'kr': 'Kanuri',
    'ks': 'Kashmiri',
    'ku': 'Kurdish',
    'kv': 'Komi',
    'kw': 'Cornish',
    'ky': 'Kirghiz',
    'la': 'Latin',
    'lb': 'Luxembourgish',
    'lg': 'Ganda',
    'li': 'Limburgan',
    'ln': 'Lingala',
    'lo': 'Lao',
    'lt': 'Lithuanian',
    'lu': 'Luba-Katanga',
    'lv': 'Latvian',
    'mg': 'Malagasy',
    'mh': 'Marshallese',
    'mi': 'Maori',
    'mk': 'Macedonian',
    'ml': 'Malayalam',
    'mn': 'Mongolian',
    'mr': 'Marathi',
    'ms': 'Malay',
    'mt': 'Maltese',
    'my': 'Burmese',
    'na': 'Nauruan',
    'nb': 'Norwegian Bokmål',
    'nd': 'Northern Ndebele',
    'ne': 'Nepali',
    'ng': 'Ndonga',
    'nl': 'Dutch',
    'nn': 'Norwegian Nynorsk',
    'no': 'Norwegian',
    'nr': 'Southern Ndebele',
    'nv': 'Navajo',
    'ny': 'Chichewa',
    'oc': 'Occitan',
    'oj': 'Ojibwa',
    'om': 'Oromo',
    'or': 'Oriya',
    'os': 'Ossetian',
    'pa': 'Panjabi',
    'pi': 'Pali',
    'pl': 'Polish',
    'ps': 'Pushto',
    'pt': 'Portuguese',
    'qu': 'Quechua',
    'rm': 'Romansh',
    'rn': 'Rundi',
    'ro': 'Romanian',
    'ru': 'Russian',
    'rw': 'Kinyarwanda',
    'sa': 'Sanskrit',
    'sc': 'Sardinian',
    'sd': 'Sindhi',
    'se': 'Northern Sami',
    'sg': 'Sango',
    'si': 'Sinhalese',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'sm': 'Samoan',
    'sn': 'Shona',
    'so': 'Somali',
    'sq': 'Albanian',
    'sr': 'Serbian',
    'ss': 'Swati',
    'st': 'Southern Sotho',
    'su': 'Sundanese',
    'sv': 'Swedish',
    'sw': 'Swahili',
    'ta': 'Tamil',
    'te': 'Telugu',
    'tg': 'Tajik',
    'th': 'Thai',
    'ti': 'Tigrinya',
    'tk': 'Turkmen',
    'tl': 'Tagalog',
    'tn': 'Tswana',
    'to': 'Tongan',
    'tr': 'Turkish',
    'ts': 'Tsonga',
    'tt': 'Tatar',
    'tw': 'Twi',
    'ty': 'Tahitian',
    'ug': 'Uighur',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'uz': 'Uzbek',
    've': 'Venda',
    'vi': 'Vietnamese',
    'vo': 'Volapük',
    'wa': 'Walloon',
    'wo': 'Wolof',
    'xh': 'Xhosa',
    'yi': 'Yiddish',
    'yo': 'Yoruba',
    'za': 'Zhuang',
    'zh': 'Chinese',
    'zu': 'Zulu'
}

def iso639_to_name(code):
    if code in _language_codes:
        return _language_codes[code]
    else:
        raise ValueError('Unknown language code "{}"'.format(code))
