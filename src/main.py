# This is a sample Python script.
import spacy

import excelExtract
import corpusTesting
import dedupeTest
import testQuerryToTable
import dblpTable
import corpusTools
from corpus import location
import sys

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
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
    nlp = spacy.load("en_core_web_trf")  # initialize spacy _trf is the core intended for accuracy
    print_hi('PyCharm')
    #corpusTesting.Test1()
    #excelExtract.test('CMES')
    #dedupeTest.test1()
    dblpTable.build(cc, ll, nlp, "SELECT * FROM event_dblp WHERE eventId LIKE '%HPCC%'")
    print('\n\n')
    testQuerryToTable.test1(cc, ll)
    #testQuerryToTable.ordinalToInt('fiftyfirst')
    #testQuerryToTable.ordinalToInt('101th')
    #testQuerryToTable.ordinalToInt('fourth')
    #testQuerryToTable.string_distance("ghaogiadfghobdfahgoiadsgdfaigWort1123456789Wort2dföoashgioaegh", "wort1", "wort2")



# See PyCharm help at https://www.jetbrains.com/help/pycharm/





