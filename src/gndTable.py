# currently work in progress to build a table for an input based on the gnd database

from tabulate import tabulate
import query
from src import tools
from src.tools import find_ordinal, get_from_to, FTDate, location_finder, fix_ordinal, removeFalsePositives, \
    removeFalsePostivesEarly, freq, addGhostEvents, sortDictByYear, findWholeWord
import re

def buildFromRESTful(ll,nlp,input):
    table = [
        {'acronym': 'null', 'acronym2': 'null', 'ordinal': 'null', 'year': 'null', 'from': 'null', 'to': 'null',
         'country': 'null', 'region': 'null', 'city': 'null', 'gnd': 'null', 'dblp': 'null', 'wikicfpID': 'null',
         'or': 'null', 'wikidata': 'null', 'confref': 'null', 'seriesAcronym': 'null', 'title': 'null'}]

    res = query.getgnd(input)  # fpl
    removeFalsePostivesEarly(res, input)

    for index in range(len(res)):
        # TODO figure out a way so that ordinals are assigned to the correct event if more than one are in the title
        #  Note: this somewhat works now but we have to deduct trust score for details like that when multiple events
        #  are in a title

        if res[index]['title'] is None:
            doc = nlp('')
        else:
            doc = nlp(res[index]['title'])
        found_entities = [{"Text": entity.text, "Entity Tag": entity.label_} for entity in doc.ents]

        # TODO find a solution to the acronym issue as in this source there are multiple acronyms in the acronym column
        acronym = res[index]['acronym']
        if acronym is None:
            acronym = 'missing'

        if not findWholeWord(input)(acronym) == None:
            acronym = input

        acronym = re.sub(r'[0-9]', r'', acronym)
        acronym.replace(" ", "")

        ordinal = find_ordinal(found_entities, res, index)
        if ordinal is None:
            ordinal = -1

        # TODO format the gnd date into a consistent format
        year = res[index]['year']
        if year is None:
            year = 'missing'

        date = get_from_to(found_entities, res, index, nlp)
        if date is None:
            date = FTDate

        location = tools.location_finder(ll, res, index, nlp)
        city = location.city
        region = location.region
        country = location.country

        gnd = res[index]['eventId']
        title = res[index]['title']

        table = table + [{'acronym': acronym + '-' + str(year), 'acronym2': acronym + '-' + str(ordinal),
                          'ordinal': str(ordinal), 'year': year, 'seriesAcronym': acronym,
                          'from': f'{str("{:02d}".format(int(date.f_d)))}.{str("{:02d}".format(int(date.f_m)))}.{str("{:02d}".format(int(date.f_y)))}',
                          'to': f'{str("{:02d}".format(int(date.t_d)))}.{str("{:02d}".format(int(date.t_m)))}.{str("{:02d}".format(int(date.t_y)))}',
                          'gnd': gnd, 'title': title, 'city': city, 'region': region, 'country': country}]

        table = sortDictByYear(table)

    print(tabulate(table, headers="keys"))
    print('\n')
    print(tabulate(fix_ordinal(table), headers="keys"))
    freq(table)
    print(tabulate(addGhostEvents(fix_ordinal(table), 'annual'), headers="keys"))