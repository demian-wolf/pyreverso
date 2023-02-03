"""Mini-version of Reverso Conjugation with command-line interface."""

from reverso_api import ReversoConjugationAPI

api = ReversoConjugationAPI(
    input("Enter the source verb to conjugate... "),
    input("Enter the source language code... ")
)

print()
print("Conjugation:")
for verb, conjugation, extra, tense, mode in api.get_conjugations():
    print('verb="%s", conjugation="%s", tense="%s", mode="%s"' % (verb, (extra + ' ' +conjugation).strip(), tense, mode))

