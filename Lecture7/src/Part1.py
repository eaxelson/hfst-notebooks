# # COMPUTATIONAL MORPHOLOGY WITH HFST TOOLS - LECTURE 7
#
# ## 1. Flag diacritics
#
# Inflection of Arabic “kitaab” (= book):
#
# <img src="img/inflection_of_kitaab.png">
#
# Combinations of the definite article together with indefinite forms are not allowed, such as *alkitaabuN.
#
# Lexc file for the inflection of “kitaab”:
#
# ``` 
# Multichar_Symbols +Def +Indef +Nom +Acc +Gen
# 
# LEXICON Root
#         Nouns ;
# 
# LEXICON Nouns
# al      DefStems ;
#         DefStems ;
#         IndefStems ;
# 
# LEXICON DefStems
# kitaab  DefCase ;     ! add other stems here
# 
# LEXICON IndefStems
# kitaab  IndefCase ;   ! add other stems here
# 
# LEXICON DefCase
# +Def+Nom:u      # ;
# +Def+Acc:a      # ;
# +Def+Gen:i      # ;
# 
# LEXICON IndefCase
# +Indef+Nom:uN   # ;
# +Indef+Acc:aN   # ;
# +Indef+Gen:iN   # ;                      
# ```
#
# Any problems?
#
# Finite-state transducer of the “kitaab” lexc file:
#
# <img src="img/fst_of_kitaab.png">
#
# The long-distance dependency is encoded by the path taken for the stems.
#
# Lexc file for “kitaab” using flag diacritics for the definite form:
#
# ```
# Multichar_Symbols +Def +Indef +Nom +Acc +Gen
#                   @U.ART.PRESENT@ @U.ART.ABSENT@
# 
# LEXICON Root
#         Nouns ;
# 
# LEXICON Nouns
# al@U.ART.PRESENT@  Stems ;
#                    Stems ;
# 
# LEXICON Stems
# kitaab  Case ;   ! add other stems here
# 
# LEXICON Case
# +Def+Nom:u      # ;
# +Def+Acc:a      # ;
# +Def+Gen:i      # ;
# @U.ART.ABSENT@IndefCase ;
# 
# LEXICON IndefCase
# +Indef+Nom:uN   # ;
# +Indef+Acc:aN   # ;
# +Indef+Gen:iN   # ;                                             
# ```
#
# Finite-state transducer of the “kitaab” lexc file using flag diacritics for the definite form:
#
# <img src="img/fst_of_kitaab_with_flags.png">
#
# The long-distance dependency is encoded by flags that are stored in memory
# as we progress through the network.
#
# Lexc with “bi” article that governs the genitive case:
#
# ```
# Multichar_Symbols +Def +Indef +Nom +Acc +Gen
#                   @U.ART.PRESENT@ @U.ART.ABSENT@
#                   @U.CASE.NOM@ @U.CASE.ACC@ @U.CASE.GEN@
# 
# LEXICON Root
#         Preposition ;
# 
# LEXICON Preposition
# bi@U.CASE.GEN@  Article ; ! optional preposition prefix
#                 Article ; ! empty string entry
# 
# LEXICON Article
# al@U.ART.PRESENT@ Stems ; ! opt. def. article prefix
#                   Stems ; ! empty string entry
# 
# LEXICON Stems
# kitaab  Case ;            ! add other stems here
# 
# LEXICON Case
# +Def+Nom:u      MarkNOM ;
# +Def+Acc:a      MarkACC ;
# +Def+Gen:i      MarkGEN ;
# @U.ART.ABSENT@  IndefCase ;
#
# LEXICON IndefCase
# +Indef+Nom:uN   MarkNOM ;
# +Indef+Acc:aN   MarkACC ;
# +Indef+Gen:iN   MarkGEN ;
# 
# LEXICON MarkNOM
# @U.CASE.NOM@    # ;
# 
# LEXICON MarkACC
# @U.CASE.ACC@    # ;
# 
# LEXICON MarkGEN
# @U.CASE.GEN@    # ;
# ```
#
# Transducer with “bi” article governing the genitive case:
#
# <img src="img/fst_of_kitaab_genitive.png">
#
# Tricky lexc syntax when upper and lower forms are different:
#
# <img src="img/tricky_lexc_syntax.png">

# ### Full range of flag-diacritic operators
#
# * General format:
#   - `@operator.feature.value@`
#   - `@operator.feature@` (operates on the “neutral” = unset value)
# * The features and values can be (almost) any string you like; the strings are case sensitive, e.g., “DEFINITE” is not the same as “definite”.
# * The operator must be one of: `P`, `N`, `C`, `R`, `D`, `U`:
#
# <img src="img/flag_diacritic_operators.png">
#
# ### P flag: positive (re)setting
#
# * Example:
#   - `@P.CASE.GEN@`
#   - Set the value of `CASE` to `GEN`
#   - It does not matter what `CASE` was before, or if it was set at all
#   - Never fails
#
# ### N flag: negative (re)setting
#
# * Example: `@N.CASE.GEN@`
#   - Set the value of `CASE` to something else than `GEN`
#   - The value of `CASE` is not well defined after this, but there is some value and we know it is not `GEN`
#   - It does not matter what `CASE` was before, or if it was set at all
#   - Never fails
#
# ### C flag: clear feature
#
# * Example: `@C.CASE@`
#   - Unset the value of `CASE`
#   - `CASE` has no value after this (also called neutral)
#   - It does not matter what `CASE` was before, or if it was set at all
#   - Never fails
#
# ### R flag: require test
#
# * Examples:
#   - `@R.CASE.GEN@`
#     - Succeeds if `CASE` has the value `GEN`
#     - Otherwise fails and blocks this path
#     - Does not set or modify the value of `CASE`
#   - `@R.CASE@`
#     - Succeeds if `CASE` is set to some value (not neutral)
#     - Otherwise fails and blocks this path
#     - Does not set or modify the value of `CASE`
#
# ### D flag: disallow test
#
# * Examples:
#   - `@D.CASE.GEN@`
#     - Succeeds if `CASE` does not have the value `GEN`
#     - Otherwise fails and blocks this path
#     - Does not set or modify the value of `CASE`
#   - `@D.CASE@`
#     - Succeeds if `CASE` is not set to any value (neutral)
#     - Otherwise fails and blocks this path
#     - Does not set or modify the value of `CASE`
#
# ### U flag: unification test
#
# * Examples:
#   - `@U.CASE.GEN@`
#     - Succeeds if `CASE` has the value `GEN`
#     - Also succeeds if `CASE` is unset (neutral); in this case, `CASE` is set to `GEN` after this operation
#     - Otherwise fails and blocks this path
#   - `al@U.ART.PRESENT@kitaab@U.ART.ABSENT@uN@U.CASE.NOM@`
#     - Fails
#   - `bi@P.CASE.GEN@al@U.ART.PRESENT@kitaabi@U.CASE.GEN@`
#     - Succeeds
#
# ### More examples with the same flag-diacritic operators
#
# <img src="img/n_foo_blah.png">
#
# * `@P.FEAT.M@` `@D.FEAT.M@` will fail.
# * `@N.FEAT.M@` `@D.FEAT.Q@` will fail.
# * `@R.FEAT@` will succeed if `FEAT` is currently set to some other value than neutral.
# * `@U.FEAT.M@` succeeds if `FEAT` is currently set to `M` or neutral; the value is reset to `M` after this operation.
# * `@N.FEAT.M@` `@U.FEAT.Q@` succeeds, leaving `FEAT=Q` in memory.

# ## 2. Non-concatenative morphotactics
#
# ### Limited reduplication in Tagalog verbs
#
# <img src="img/tagalog_verbs.png">
#
# ### Full-stem reduplication in Malay nouns
#
# <img src="img/malay_nouns.png">
#
# ### Arabic word forms based on roots d-r-s and k-t-b
#
# <img src="img/arabic_word_forms.png">
#
# ### Tagalog limited reduplication: easy with two-level morphology!
#
# <img src="img/tagalog_reduplication.png">
#
# ### Malay full-stem reduplication with compile-replace
#
# <img src="img/malay_reduplication.png">
#
# ### Arabic “morphemes”
#
# <img src="img/arabic_morphemes.png">
#
# ### Arabic morphotactics using merge and compile-replace
#
# * xfst operator for merge to the right: `.m>.`
# * xfst operator for merge to the left: `.<m.`
# * For instance,
#   - Lexical form: `[ ktb     +FormI     +Pass] +3P+Fem+Sg`
#   - Surface form: `^[{ktb}.m>.{CVCVC}.<m.[u*i]^]at`
# * The compile-replace algorithm executes the merge commands in the regular expression and produces the final surface form: `kutibat`
#
# ### Arabic morphotactics with Twol regular expression center rules
#
# <img src="img/arabic_morphotactics.png">
#
# ### More information
#
# * Chapter 7 of the Beesley & Karttunen book: “Flag Diacritics”
# * Chapter 8 of the Beesley & Karttunen book: “Non-Concatenative Morphotactics”
# * HFST: hfst-twolc − A Two-Level Grammar Compiler: TODO
