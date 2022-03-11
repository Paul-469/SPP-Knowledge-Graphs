# currently work in progress to build a table for an input based on the proceedings.com database
import re

from tabulate import tabulate
from src import tools, excelExtract
from src.tools import find_ordinal, get_from_to, FTDate, fix_ordinal, sortDictByYear, removeFalsePostivesEarly


# Important In the output the index starts at 0 but in the search it starts at one not to be confused use start at 0
# outside of the search function iter_rows and similar
# Publisher	            0
# Conference Title	    1
# Book Title	        2
# Series	            3
# Description	        4
# Mtg Year	            5
# Editor	            6
# ISBN	                7
# Pages	                8
# Format	            9
# POD Publisher	        10
# Publ Year	            11
# Subject1	            12
# Subject2	            13
# Subject3	            14
# Subject4	            15
# List Price            16


def buildFromXLSX(ll, nlp, input):
    table = [
        {'acronym': 'null', 'acronym2': 'null', 'ordinal': 'null', 'year': 'null', 'from': 'null', 'to': 'null',
         'country': 'null', 'region': 'null', 'city': 'null', 'gnd': 'null', 'dblp': 'null', 'wikicfpID': 'null',
         'or': 'null', 'wikidata': 'null', 'confref': 'null', 'seriesAcronym': 'null', 'title': 'null'}]

    res = excelExtract.querryPDC(input)  # fpl

    if res == 'error' or res == 'source not available':
        print(res)
        return
    # print(tabulate(res, headers="keys"))
    # removeFalsePostivesEarly(res, input)

    if len(res) == 0:
        print('no results')
        return

    for index in range(len(res)):
        # TODO figure out a way so that ordinals are assigned to the correct event if more than one are in the title
        #  Note: this somewhat works now but we have to deduct trust score for details like that when multiple events
        #  are in a title

        if res[index][1] is None:
            doc = nlp('')
        else:
            doc = nlp(res[index][2])
        found_entities = [{"Text": entity.text, "Entity Tag": entity.label_} for entity in doc.ents]

        acronym = res[index][3]
        if acronym is None:
            acronym = input    # 'missing' i think we can do that for this source as we dont find an acronym
        acronym = re.sub(r'[0-9]', r'', acronym)
        acronym = acronym.replace(" ", "")

        ordinal = find_ordinal(found_entities, res, index)
        if ordinal is None:
            ordinal = 'missing'

        year = res[index][5]
        if year is None:
            year = 'missing'

        date = get_from_to(found_entities, res, index, nlp)
        if date is None:
            date = FTDate

        location = tools.location_finder(ll, res, index, nlp)
        city = location.city
        region = location.region
        country = location.country

        title = res[index][2]

        table = table + [{'acronym': acronym + '-' + str(year), 'acronym2': acronym + '-' + str(ordinal),
                          'ordinal': str(ordinal), 'year': year, 'seriesAcronym': acronym,
                          'from':  f'{str("{:02d}".format(int(date.f_d)))}.{str("{:02d}".format(int(date.f_m)))}.{str("{:02d}".format(int(date.f_y)))}',
                          'to':  f'{str("{:02d}".format(int(date.t_d)))}.{str("{:02d}".format(int(date.t_m)))}.{str("{:02d}".format(int(date.t_y)))}',
                          'title': title, 'city': city, 'region': region, 'country': country}]

    # print(tabulate(table, headers="keys"))
    # print('\n')
    table = sortDictByYear(table)
    # print(tabulate(table, headers="keys"))
    print('\n')
    print(tabulate(fix_ordinal(table), headers="keys"))
    return table
    # print('\n')
    # print(tabulate(removeFalsePositives(table, input), headers="keys"))
