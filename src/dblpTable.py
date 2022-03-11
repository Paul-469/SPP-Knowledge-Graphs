# currently work in progress to build a table for an input based on the dblp database
import re

from tabulate import tabulate
import query
from src import tools
from src.tools import find_ordinal, get_from_to, FTDate, location_finder, fix_ordinal, removeFalsePositives, \
    removeFalsePostivesEarly, freq, isThereMoreThanOne, year_integrity, ordinal_integrity


# deprecated!!!
def buildFromLocalCC(cc, ll, nlp, query):
    table = [
        {'acronym': 'null', 'acronym2': 'null', 'ordinal': 'null', 'year': 'null', 'from': 'null', 'to': 'null',
         'country': 'null', 'region': 'null', 'city': 'null', 'gnd': 'null', 'dblp': 'null', 'wikicfpID': 'null',
         'or': 'null', 'wikidata': 'null', 'seriesAcronym': 'null', 'title': 'null'}]

    res = cc.SqlQueryResultTest(query)  # fpl
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

        # TODO more in None checks
        acronym = res[index]['series']
        if acronym is None:
            acronym = 'missing'

        ordinal = find_ordinal(found_entities, res, index)
        if ordinal is None:
            ordinal = 'missing'

        year = res[index]['year']
        if year is None:
            year = 'missing'

        date = get_from_to(found_entities, res, index, nlp)
        if date is None:
            date = FTDate

        location = location_finder(ll, res, index)
        city = location.city
        region = location.region
        country = location.country

        dblp = res[index]['eventId']
        title = res[index]['title']

        table = table + [{'acronym': acronym + '-' + str(year), 'acronym2': acronym + '-' + str(ordinal),
                          'ordinal': str(ordinal), 'year': year, 'seriesAcronym': acronym,
                          'from': str("{:02d}".format(int(date.f_d))) + '.' + str(
                              "{:02d}".format(int(date.f_m))) + '.' + str("{:02d}".format(int(date.f_y))),
                          'to': str("{:02d}".format(int(date.t_d))) + '.' + str(
                              "{:02d}".format(int(date.t_m))) + '.' + str("{:02d}".format(int(date.t_y))),
                          'dblp': dblp, 'title': title, 'city': city, 'region': region, 'country': country}]

    print(tabulate(table, headers="keys"))
    print('\n')
    print(tabulate(fix_ordinal(table), headers="keys"))


# TODO remove the former at a later point


def buildFromRESTful(ll, nlp, input):
    table = [
        {'acronym': 'null', 'acronym2': 'null', 'ordinal': 'null', 'year': 'null', 'from': 'null', 'to': 'null',
         'country': 'null', 'region': 'null', 'city': 'null', 'gnd': 'null', 'dblp': 'null', 'wikicfpID': 'null',
         'or': 'null', 'wikidata': 'null', 'confref': 'null', 'seriesAcronym': 'null', 'title': 'null'}]

    res = query.getdblp(input)  # fpl
    if res == 'error' or res == 'source not available':
        print(res)
        return
    # print(tabulate(res, headers="keys"))

    removeFalsePostivesEarly(res, input)

    # print(tabulate(res, headers="keys"))
    if len(res) == 0:
        print('no results')
        return
    # print(tabulate(res, headers="keys"))

    for index in range(len(res)):
        # TODO figure out a way so that ordinals are assigned to the correct event if more than one are in the title
        #  Note: this somewhat works now but we have to deduct trust score for details like that when multiple events
        #  are in a title

        if res[index]['title'] is None:
            doc = nlp('')
        else:
            doc = nlp(res[index]['title'])
        found_entities = [{"Text": entity.text, "Entity Tag": entity.label_} for entity in doc.ents]
        # print(tabulate(found_entities, headers="keys"))

        # TODO more in None checks
        acronym = res[index]['series']
        if acronym is None:
            acronym = 'missing'
        acronym = re.sub(r'[0-9]', r'', acronym)
        acronym = acronym.replace(" ", "")

        ordinal = find_ordinal(found_entities, res, index)
        if ordinal is None:
            ordinal = 'missing'

        year = res[index]['year']
        if year is None:
            year = 'missing'

        date = get_from_to(found_entities, res, index, nlp)
        if date is None:
            date = FTDate()


        location = tools.location_finder(ll, res, index, nlp)
        city = location.city
        region = location.region
        country = location.country

        # print(tabulate(res, headers="keys"))
        # print(date.f_d)
        # print(date.f_m)
        # print(date.f_y)
        # print(date.t_d)
        # print(date.t_m)
        # print(date.t_y)

        dblp = res[index]['eventId']
        title = res[index]['title']

        table = table + [{'acronym': acronym + '-' + str(year), 'acronym2': acronym + '-' + str(ordinal),
                          'ordinal': str(ordinal), 'year': year, 'seriesAcronym': acronym,
                          'from':  f'{str("{:02d}".format(int(date.f_d)))}.{str("{:02d}".format(int(date.f_m)))}.{str("{:02d}".format(int(date.f_y)))}',
                          'to':  f'{str("{:02d}".format(int(date.t_d)))}.{str("{:02d}".format(int(date.t_m)))}.{str("{:02d}".format(int(date.t_y)))}',
                          'dblp': dblp, 'title': title, 'city': city, 'region': region, 'country': country}]

    # print(tabulate(table, headers="keys"))
    print('\n')
    print(tabulate(fix_ordinal(table), headers="keys"))
    # print('\n')
    # print(tabulate(removeFalsePositives(table, input), headers="keys"))
    freq(table)
    if year_integrity(table) and ordinal_integrity(table):
        temp = isThereMoreThanOne(table)
        for x in range(len(temp)):
            print(tabulate(temp[x], headers="keys"))
        table = temp[0]

    return table

