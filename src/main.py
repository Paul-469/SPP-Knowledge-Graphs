# This is a sample Python script.
import os

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
import gndTable
import proceedingsDotComTable
import pandas as pd


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


from fb4.app import AppWrap
from fb4.sqldb import db
from sqlalchemy import Column
import sqlalchemy.types as types
from flask import redirect,render_template, request, flash, Markup, url_for, abort

class Message2(db.Model):
    id = Column(types.Integer, primary_key=True)
    text = Column(types.Text, nullable=False)
    author = Column(types.String(100), nullable=False)
    category = Column(types.String(100), nullable=False)
    draft = Column(types.Boolean, default=False, nullable=False)
    create_time = Column(types.Integer, nullable=False, unique=True)



class HelloWeb(AppWrap):
    '''
    a sample web application
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super().__init__(host='localhost')

        AppWrap.addTemplatePath(self, "../templates")
        db.init_app(self.app)
        self.db = db

        self.app.secret_key = 'dev'
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['BOOTSTRAP_BTN_STYLE'] = 'primary'
        self.app.config['BOOTSTRAP_BTN_SIZE'] = 'sm'

        @self.app.before_first_request
        def before_first_request_func():
            self.initDB()

        @self.app.route('/table/<message_id>/view')
        def view_message(message_id):
            return self.message_view(message_id)

        @self.app.route('/table/<message_id>/edit')
        def edit_message(message_id):
            return self.message_edit(message_id)

        @self.app.route('/table/<message_id>/delete', methods=['POST'])
        def delete_message(message_id):
            return self.message_delete(message_id)

        @self.app.route('/table')
        def test_table():
            return self.table()

        @self.app.route('/')
        def home():
            return self.home()

    def initDB(self,limit=20):
        '''
        initialize the database
        '''
        self.db.drop_all()
        self.db.create_all()
        ll = location.LocationLookup()  # initialize locationlookup
        nlp = spacy.load("en_core_web_trf")  # run "python -m spacy download en_core_web_trf" if it fails.


        res = [dblpTable.buildFromRESTful(ll, nlp, 'HPCC')]
        list = [1]
        res = merge_tables(res,list)
        dictToMessages(res, self)

    def message_delete(self, message_id):
        message = Message.query.get(message_id)
        if message:
            db.session.delete(message)
            db.session.commit()
            return f'Message {message_id} has been deleted. Return to <a href="/table">table</a>.'
        return f'Message {message_id} did not exist and could therefore not be deleted. Return to <a href="/table">table</a>.'

    def message_edit(self, message_id):
        message = Message.query.get(message_id)
        if message:
            message.draft = not message.draft
            db.session.commit()
            return f'Message {message_id} has been edited by toggling draft status. Return to <a href="/table">table</a>.'
        return f'Message {message_id} did not exist and could therefore not be edited. Return to <a href="/table">table</a>.'

    def message_view(self, message_id):
        message = Message.query.get(message_id)
        if message:
            return f'Viewing {message_id} with text "{message.text}". Return to <a href="/table">table</a>.'
        return f'Could not view message {message_id} as it does not exist. Return to <a href="/table">table</a>.'

    def initMessages(self, limit=20):
        '''
        create an initial set of message with the given limit
        Args:
            limit(int): the number of messages to create
        '''

        for i in range(limit):
            m = Message(
                text='Test message {}'.format(i + 1),
                author='Author {}'.format(i + 1),
                category='Category {}'.format(i + 1),
                create_time=4321 * (i + 1)
            )
            if i % 4:
                m.draft = True
            self.db.session.add(m)
        self.db.session.commit()

    def table(self):
        '''
        test table
        '''
        page = request.args.get('page', 1, type=int)
        pagination = Message.query.paginate(page, per_page=20)
        messages = pagination.items
        titles = [('id', '#'), ('text', 'Message'), ('author', 'Author'), ('category', 'Category'), ('draft', 'Draft'),
                  ('create_time', 'Create Time')]
        return render_template('table.html', messages=messages, titles=None)



    def home(self):
        '''
        render the home page of the HelloWeb application
        '''
        html = render_template("bootstrap.html", title="HelloWeb demo application",
                               content="Welcome to the Flask + Bootstrap4 Demo web application", error=None)
        return html


helloWeb = HelloWeb()
app = helloWeb.app

class Message(db.Model):
    acronym = Column(types.String(100), primary_key=True)
    acronym2 = Column(types.String(100), nullable=True)
    ordinal = Column(types.String(100), nullable=True)
    year = Column(types.String(100), nullable=True)
    from_date = Column(types.String(100), nullable=True)
    to_date = Column(types.String(100), nullable=True)
    country = Column(types.String(100), nullable=True)
    region = Column(types.String(100), nullable=True)
    city = Column(types.String(100), nullable=True)
    gnd = Column(types.String(100), nullable=True)
    dblp = Column(types.String(100), nullable=True)
    wikicfpID = Column(types.String(100), nullable=True)
    or_id = Column(types.String(100), nullable=True)
    wikidata = Column(types.String(100), nullable=True)
    confref = Column(types.String(100), nullable=True)
    seriesAcronym = Column(types.String(100), nullable=True)
    title = Column(types.String(100), nullable=True)

def dictToMessages(ldict, app):
    for x in range(1, len(ldict)):

        m = Message(
            acronym=ldict[x]['acronym'],
            acronym2=ldict[x]['acronym2'],
            ordinal=ldict[x]['ordinal'],
            year=ldict[x]['year'],
            country=ldict[x]['country'],
            from_date=ldict[x]['from'],
            to_date = ldict[x]['to'],
            region = ldict[x]['region'],
            city = ldict[x]['city'],
            gnd = ldict[x]['gnd'],
            dblp = ldict[x]['dblp'],
            wikicfpID = ldict[x]['wikicfpID'],
            or_id = ldict[x]['or'],
            wikidata = ldict[x]['wikidata'],
            confref = ldict[x]['confref'],
            seriesAcronym = ldict[x]['seriesAcronym'],
            title = ldict[x]['title'],
        )

        app.db.session.add(m)
    app.db.session.commit()


if __name__ == '__main__':

    parser = helloWeb.getParser("Flask + Bootstrap4 Demo Web Application")
    args = parser.parse_args()
    helloWeb.optionalDebug(args)
    helloWeb.run(args)

    print("Have you done everything described in meo_4j.py? If so remove the print and following sys.exit()")
    sys.exit()

    # neo_DB = neo("bolt://127.0.0.1:7687", "neo4j", "kgl")
    # limited_hardcoded_graph_addition_demo(neo_DB)
    # neo_DB.close()

    #sys.exit()

    ll = location.LocationLookup()  # initialize locationlookup
    nlp = spacy.load("en_core_web_trf")   # run "python -m spacy download en_core_web_trf" if it fails.

    # dblpTable.buildFromRESTful(ll, nlp, 'HPCC')
    dblpTable.buildFromRESTful(ll, nlp, 'HPCC')
    proceedingsDotComTable.buildFromXLSX(ll, nlp, 'HPCC')
    confrefTable.buildFromRESTful(ll, nlp, 'HPCC')
    wikicfpTable.buildFromRESTful(ll, nlp, 'HPCC')

    # lod = dblpTable.buildFromRESTful(ll, nlp, 'HPCC')
    # print(tabulate(lod, headers="keys"))
    # add_table_to_graph(lod, neo_DB)
    # neo_DB.close()
    # list_of_sources = [proceedingsDotComTable.buildFromXLSX(ll, nlp, 'HPCC'), dblpTable.buildFromRESTful(ll, nlp, 'HPCC'), confrefTable.buildFromRESTful(ll, nlp, 'HPCC')]
    # list_of_trust = [9, 10, 7]

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




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
