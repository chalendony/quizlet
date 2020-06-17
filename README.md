
# Development History
- module for each type of Quizlet set
    -- synon sets
    -- nouns - DONE
    -- verbs and usage - DONE
    -- MUST get prepositions
    -- adjadv usage: nomaliz.
    -- compound verbs:

- remove duplicates from input list and with term in database
- timestamp export/import into database to separate the sets. - DONE
- refactor configuration
- create code to test if batch of words are in dwds : Partially done - need to modular create method from this .Jun 14, 2020
- try better way to get dwds via API
- refactor duplicate code

# Goal:

Create Sets flash cards for training german from online resources: Reverso, Leo Linguee

# Process

## Collect Terms
How the code used: Build batch size of 100 cards, each time run code keep 'PENDING' file until 100 new terms are created.

## Collect Translations
Linguee:
1. create linguee urls
2. use wget to download page for each url, to reduce calls and traffic, then contents of page is parsed - since limited usage

3. for each term, call  leo, reverso and parse linguee page - storing all results in database
Leo: translation, phrases, examples



DONE
