# # COMPUTATIONAL MORPHOLOGY WITH HFST TOOLS - LECTURE 5
#
# ## Section 1: Big picture
#
# ### Lecture 1: lexc
#
# "Lexicon without any replace rules"
#
# <img src="img/big_picture_lexc.png">
#
# ### Lectures 2 and 3: xfst and twolc
#
# "Lexicon combined with replace rules"
#
# <img src="img/big_picture_xfst_and_twolc.png">
#
# ### Lecture 4?: xfst / regular expressions 
#
# "Rules without much of a lexicon" 
#
# <img src="img/big_picture_xfst_and_regexps.png">
#
# ## Section 2: Guessers and stemmers
#
# ### Increased coverage with guessers 
#
# * Section 9.5.4 in the Beesley & Karttunen book
# * A finite-state morphological analyzer only recognizes the words that are included in its lexc lexicon.
# * It may take several person-months (or even years) of work to build up a lexicon with the tens of thousands of stems necessary for broad coverage of real text.
# * As an alternative, or a complement, one can use
#   * guessers
#   * stemmers
#   * unsupervised morphology
#
# ### Definition of a guesser
#
# * A guesser is designed to analyze words that are based on any phonologically possible stem.
# * The set of phonologically possible stems is definable, more or less precisely, using regular expressions and scripts.
# * Useful
#   * as a general backup when normal morphological analysis fails
#   * for suggesting new stems that need to be added to the lexicon
#
# ### Case study: Esperanto verb guesser lexicon
#
# <img src="img/esperanto_lexc.png">
#
# ### Case study: Esperanto verb guesser xfst script
#
"""
clear stack

! We limit ourselves here to lower case letters and ignore some Esperanto letters not found in the
! ASCII character set
define Vowel     a | e | i | o | u ;
define ConsClust b | c | d | f | g | h | j | k | l | m | n | p | r | s | t | v | z |
                 k r | p r | t r | g r | b r | d r | s k | s p | s t ;

                 ! Each verb root must be of the format Cc V Cc V Cc V Cc ..., where the first consonant cluster Cc is
                 ! optional and it must be followed by at least one pair of V Cc ( = vowel + consonant cluster):
                 define PossibleVerbRoot  ( ConsClust ) [ [ Vowel ] [ ConsClust ] ]+ "+Guess":0 ;

                 ! The lexc description is compiled and pushed on the stack
                 read lexc esperanto.lexc

                 ! Using the 'substitute defined' command, the placeholder symbol is replaced by the value of PossVerbRoot
                 substitute defined PossibleVerbRoot for ^GUESSVERBROOT

                 ! Make verb vocabulary ready to use
                 define AllPossibleVerbs ;
                 regex AllPossibleVerbs ;
"""
# ### Case study: Esperanto verb guesser example output
#
#
# Try: up donadas, random-upper, random-lower
#
# don+Guess+Verb+Cont+Pres
# don+Verb+Cont+Pres
# donad+Guess+Verb+Pres
#
# dip+Guess+Verb+Fut
# egrust+Guess+Verb+Subj
# fust+Guess+Verb+Fut
# obr+Guess+Verb+Cont+Fut
# opop+Guess+Verb+Cond
#
# etros
# hemodas
# jumadis
# soski
# tozezus
# ugrucas
# vabis

# ### Stemming
#
# * A term used particularly in information retrieval to describe the process of reducing inflected (or sometimes derived) words to their word stem, base or root form —generally a written word form.
#   * The stem is “fish” for “fishing”, “fished”, and “fisher”.
#   * The stem is “argu” for “argue”, “argued”, “argues”, “arguing”, and “argus”...(!)
# * The stem does not need to be identical to the morphological root of the word.
#   * It is sufficient that related words map to the same stem, even if this stem is not in itself a valid root, such as the stem “argu” above, or the stem “citi” for “city” and “cities”.
# * Algorithms for stemming have been studied in computer science since the 1960s.
# * Many search engines treat words with the same stem as synonyms, as a kind of query expansion, a process called conflation.

# ### Porter’s stemmer (1979-1980)
#
# * Idea:
#   * Remove what looks like suffixes of English words
#   * Tidy up a bit
# * Feasible for English with such “simple morphology”
# * The full algorithm is described here: http://tartarus.org/martin/PorterStemmer/def.txt
# * There are other English stemmers:
#   * Snowball
#   * Lancaster
#   * They are more “aggressive” than the Porter stemmer; they remove more “suffixes”.
#
# <img src="img/porters_stemmer.png">

# ## Section 3: Pronunciation lexicon for a Language with (almost) regular Orthography: Brazilian Portuguese
#
# ### Transducing between orthographic and pronounced forms of words
#
# * Section 3.5.4 in the Beesley & Karttunen book
# * Exercise on Portuguese Brazilian
# * The task is to create a cascade of rules that maps from orthographical strings in Portuguese (this will be the lexical side) down to strings that represent their pronunciation (this will be the surface side).
#   * There will not be a lexicon.
#   * A sample mapping of written “caso” to spoken “kazu” looks like this:
#
# ```
# Lexical: caso
# Surface: kazu
# ```
#
# ### Phonetic symbols for Portuguese
#
# <img src="phonetic_symbols_for_portuguese.png">
#
# ### Some example words
#
# * What applications that you can think of need a mapping between orthographic and pronounced forms?
#
# <img src="img/test_data_for_portuguese.png">
#
# ### Conversion from orthography to pronunciation for Brazilian Portuguese (1)
#
#
# ### Conversion from orthography to pronunciation for Brazilian Portuguese (2)
#
# ### Conversion from orthography to pronunciation for Brazilian Portuguese (3)
#
# ### Conversion from orthography to pronunciation for Brazilian Portuguese (4)
#
# ### Alternative: Don't define individual rules, but rather one large regular expression
#
# <img src="img/alternative_for_portuguese.png">

# ## 
#
