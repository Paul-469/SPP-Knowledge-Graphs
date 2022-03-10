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
import wikicfpTable
import proceedingsDotComTable

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from src import confrefTable
from src.mergeTables import merge_tables
from src.neo_4j import neo
from src.tableToGraph import add_table_to_graph


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.


def limited_hardcoded_graph_addition_demo(neo_DB):
    ordinal = "11"
    acronym = "hpcc-2009"
    year = "2009"
    from_date = "25.06.2009"
    to_date = "27.06.2009"
    city = "Seoul"
    region = "Seoul"
    country = "South Korea"
    series_acronym = "hpcc"
    title = "11th IEEE International Conference on High Performance Computing and Communications, HPCC 2009, 25-27 June 2009, Seoul, Korea"

    neo_DB.add_node(title, "Event")
    neo_DB.add_two_nodes(title, "Event", ordinal, "ordinal", "is")
    neo_DB.add_two_nodes(title, "Event", acronym, "event_acronym", "acronym")
    neo_DB.add_two_nodes(title, "Event", year, "year", "in")
    neo_DB.add_two_nodes(title, "Event", from_date, "from_date", "from")
    neo_DB.add_two_nodes(title, "Event", to_date, "to_date", "to")
    neo_DB.add_two_nodes(title, "Event", city, "city", "in")
    neo_DB.add_two_nodes(title, "Event", region, "region", "in")
    neo_DB.add_two_nodes(title, "Event", country, "country", "in")
    neo_DB.add_two_nodes(title, "Event", series_acronym, "series", "part_of")

    ordinal = "12"
    acronym = "hpcc-2010"
    year = "2010"
    from_date = "01.09.2010"
    to_date = "03.09.2010"
    city = "Melbourne"
    region = "Victoria"
    country = "Australia"
    series_acronym = "hpcc"
    title = "12th IEEE International Conference on High Performance Computing and Communications, HPCC 2010, 1-3 September 2010, Melbourne, Australia"

    neo_DB.add_node(title, "Event")
    neo_DB.add_two_nodes(title, "Event", ordinal, "ordinal", "is")
    neo_DB.add_two_nodes(title, "Event", acronym, "event_acronym", "acronym")
    neo_DB.add_two_nodes(title, "Event", year, "year", "in")
    neo_DB.add_two_nodes(title, "Event", from_date, "from_date", "from")
    neo_DB.add_two_nodes(title, "Event", to_date, "to_date", "to")
    neo_DB.add_two_nodes(title, "Event", city, "city", "in")
    neo_DB.add_two_nodes(title, "Event", region, "region", "in")
    neo_DB.add_two_nodes(title, "Event", country, "country", "in")
    neo_DB.add_two_nodes(title, "Event", series_acronym, "series", "part_of")


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

    print("Have you done everything described in meo_4j.py? If so remove the print and following sys.exit()")
    sys.exit()

    neo_DB = neo("bolt://127.0.0.1:7687", "neo4j", "kgl")
    # limited_hardcoded_graph_addition_demo(neo_DB)
    # neo_DB.close()

    # sys.exit()

    ll = location.LocationLookup()  # initialize locationlookup
    nlp = spacy.load("en_core_web_trf")   # run "python -m spacy download en_core_web_trf" if it fails.

    # lod = dblpTable.buildFromRESTful(ll, nlp, 'HPCC')
    # print(tabulate(lod, headers="keys"))
    # add_table_to_graph(lod, neo_DB)
    # neo_DB.close()
    list_of_sources = [proceedingsDotComTable.buildFromXLSX(ll, nlp, 'HPCC'), dblpTable.buildFromRESTful(ll, nlp, 'HPCC'), confrefTable.buildFromRESTful(ll, nlp, 'HPCC')]
    list_of_trust = [9, 10, 7]

    lod = merge_tables(list_of_sources, list_of_trust)

    add_table_to_graph(lod, neo_DB)
    neo_DB.close()
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




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
