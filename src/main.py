# This is a sample Python script.
import spacy
from tabulate import tabulate

import excelExtract
import corpusTesting
import testQuerryToTable
import dblpTable
import corpusTools
from corpus import location
import query
import sys

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.


# TODO add "python -m spacy download en_core_web_trf" to the install script or else spacy will fail when trying to load
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ll = location.LocationLookup()  # initialize locationlookup
    nlp = spacy.load("en_core_web_trf")   # run "python -m spacy download en_core_web_trf" if it fails.

    dblpTable.buildFromRESTful(ll, nlp, 'HPCC')
    # query.test()
    sys.exit()
    # s = "IT - 72(Campania)"
    # print(s[s.find("(") + 1:s.find(")")])
    # print(s)
    # print("IT - 72(Campania)"["IT - 72(Campania)".find("(") + 1:"IT - 72(Campania)".find(")")])
    # val = 4
    # val = "{:02d}".format(val)
    # print(val)
    # sys.exit()
    # we want main to initialize the corpus etc.
    cc = corpusTools.ConferenceCorpusIntro()  # initialize conferenceCorpus instance
    cc.printCacheFile()
    ll = location.LocationLookup()  # initialize locationlookup
    nlp = spacy.load("en_core_web_trf")  # initialize spacy _trf is the core intended for accuracy run "python -m spacy download en_core_web_trf" if it fails. it is missing from the install script
    print_hi('PyCharm')
    # corpusTesting.Test1()
    # excelExtract.test('CMES')
    dblpTable.buildFromLocalCC(cc, ll, nlp, "SELECT * FROM event_dblp WHERE eventId LIKE '%HPCC%'")
    print('\n\n')
    dblpTable.buildFromRESTful(ll, nlp, 'HPCC')
    print('\n\n')
    testQuerryToTable.test1(cc, ll)
    # testQuerryToTable.ordinalToInt('fiftyfirst')
    # testQuerryToTable.ordinalToInt('101th')
    # testQuerryToTable.ordinalToInt('fourth')
    # testQuerryToTable.string_distance("ghaogiadfghobdfahgoiadsgdfaigWort1123456789Wort2dföoashgioa", "wort1", "wort2")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
