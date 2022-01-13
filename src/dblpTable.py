# currently work in progress to build a table for an input based on the dblp database
from tabulate import tabulate

from src.tools import find_ordinal, get_from_to, FTDate, location_finder, fix_ordinal


def build(cc, ll, nlp, query):
    table = [
        {'acronym': 'null', 'acronym2': 'null', 'ordinal': 'null', 'year': 'null', 'from': 'null', 'to': 'null',
         'country': 'null', 'region': 'null', 'city': 'null', 'gnd': 'null', 'dblp': 'null', 'wikicfpID': 'null',
         'or': 'null', 'wikidata': 'null', 'seriesAcronym': 'null', 'title': 'null'}]

    res = cc.SqlQueryResultTest(query)  # fpl

    for index in range(len(res)):
        # TODO figure out a way so that ordinals are assigned to the correct event if more than one are in the title
        #  Note: this somewhat works now but we have to deduct trust score for details like that when multiple events
        #  are in a title

        doc = nlp(res[index]['title'])
        found_entities = [{"Text": entity.text, "Entity Tag": entity.label_} for entity in doc.ents]

        # TODO more in None checks
        acronym = res[index]['series']
        if acronym is None:
            acronym = 'error'
        ordinal = find_ordinal(found_entities, res, index)
        year = res[index]['year']
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
