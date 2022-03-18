# This is a sample Python script.
import os

import spacy
from tabulate import tabulate

import dblpTable
import corpusTools
from corpus import location
import sys

import flasktest
import wikicfpTable
import gndTable
import proceedingsDotComTable

from src import confrefTable
from src.mergeTables import merge_tables
from src.neo_4j import neo
from src.tableToGraph import add_table_to_graph


# TODO consider exchanging title with event title and series title
# TODO add "python -m spacy download en_core_web_trf" to the install script or else spacy will fail when trying to load
# TODO implement deduplication on the returned list of dicts especially early for wikicfp
# TO-DO determine if multiple series are in one response and separate them; Sort of done:
# it will do it for an annual event but I consider doing it for events with unknown frequencies as a case freestyle
# chooses not to cover

# spacy needs to be ver. 3.2.1 and you may need to update the core if you update spacy
# also watch
# Press the green button in the gutter to run the script.


if __name__ == '__main__':

    flasktest.run()
    sys.exit()

    ll = location.LocationLookup()  # initialize locationlookup
    nlp = spacy.load("en_core_web_trf")  # run "python -m spacy download en_core_web_trf" if it fails.

    dblpTable.buildFromRESTful(ll, nlp, 'HPCC')

    print("Have you done everything described in meo_4j.py? If so remove the print and following sys.exit()")
    sys.exit()

    # neo_DB = neo("bolt://127.0.0.1:7687", "neo4j", "kgl")
    # neo_DB.close()

    #sys.exit()

    flasktest.run()
    sys.exit()

    ll = location.LocationLookup()  # initialize locationlookup
    nlp = spacy.load("en_core_web_trf")   # run "python -m spacy download en_core_web_trf" if it fails.

    # dblpTable.buildFromRESTful(ll, nlp, 'HPCC')
    # dblpTable.buildFromRESTful(ll, nlp, 'HPCC')
    # proceedingsDotComTable.buildFromXLSX(ll, nlp, 'HPCC')
    # confrefTable.buildFromRESTful(ll, nlp, 'HPCC')
    # wikicfpTable.buildFromRESTful(ll, nlp, 'HPCC')

    # lod = dblpTable.buildFromRESTful(ll, nlp, 'HPCC')
    # print(tabulate(lod, headers="keys"))
    # add_table_to_graph(lod, neo_DB)
    # neo_DB.close()
    wikicfpTable.buildFromRESTful(ll, nlp, 'bicob')
    sys.exit()

    list_of_sources = [confrefTable.buildFromRESTful(ll, nlp, 'HPCC')]
    list_of_trust = [1]
    lod = merge_tables(list_of_sources, list_of_trust)

    list_of_sources = [proceedingsDotComTable.buildFromXLSX(ll, nlp, 'HPCC'),
                       dblpTable.buildFromRESTful(ll, nlp, 'HPCC'), confrefTable.buildFromRESTful(ll, nlp, 'HPCC')]
    list_of_trust = [9, 10, 7]
    lod = merge_tables(list_of_sources, list_of_trust)

    list_of_sources = [proceedingsDotComTable.buildFromXLSX(ll, nlp, 'HPCC'), dblpTable.buildFromRESTful(ll, nlp, 'HPCC'), confrefTable.buildFromRESTful(ll, nlp, 'HPCC'), wikicfpTable.buildFromRESTful(ll, nlp, 'HPCC')]
    list_of_trust = [9, 10, 7, 5]
    lod = merge_tables(list_of_sources, list_of_trust)
    # print(tabulate(lod, headers="keys"))

    # lod = merge_tables(list_of_sources, list_of_trust)

    #  add_table_to_graph(lod, neo_DB)
    # neo_DB.close()
    # proceedingsDotComTable.buildFromXLSX(ll, nlp, 'HPCC')
    # confrefTable.buildFromRESTful(ll, nlp, 'HPCC')
    # wikicfpTable.buildFromRESTful(ll, nlp, 'HPCC')
    # dblpTable.buildFromRESTful(ll, nlp, 'HPCC')
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
