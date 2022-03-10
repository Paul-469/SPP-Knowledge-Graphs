from tabulate import tabulate

from src.tools import ordinal_integrity


def merge_tables(list_of_sources, list_of_trust):

    # If we don't have trust factors for every source sth. is wrong
    if not len(list_of_trust) == len(list_of_sources):
        print("Error in the merging input")
        return

    # We split our inputs into a list with intact ordinals and one without

    # First e which is which
    with_ord_integrity_index = []
    without_ord_integrity_index = []
    for x in range(len(list_of_sources)):
        if ordinal_integrity(list_of_sources[x]):
            with_ord_integrity_index.append(x)
        else:
            without_ord_integrity_index.append(x)

    # List of entries and trust for with
    with_ord_integrity = []
    with_ord_integrity_trust = []
    for x in range(len(with_ord_integrity_index)):
        with_ord_integrity.append(list_of_sources[with_ord_integrity_index[x]])
        with_ord_integrity_trust.append(list_of_trust[with_ord_integrity_index[x]])

    # List of entries and trust for without
    without_ord_integrity = []
    without_ord_integrity_trust = []
    for x in range(len(without_ord_integrity_index)):
        without_ord_integrity.append(list_of_sources[without_ord_integrity_index[x]])
        without_ord_integrity_trust.append(list_of_trust[without_ord_integrity_index[x]])

    # initialize output
    output = [
        {'acronym': 'null', 'acronym2': 'null', 'ordinal': 'null', 'year': 'null', 'from': 'null', 'to': 'null',
         'country': 'null', 'region': 'null', 'city': 'null', 'gnd': 'null', 'dblp': 'null', 'wikicfpID': 'null',
         'or': 'null', 'wikidata': 'null', 'confref': 'null', 'seriesAcronym': 'null', 'title': 'null'}]

    a = 0
    # merging part 1
    while True:
        entry_mem = []
        for x in range(len(with_ord_integrity)):
            entry_mem.append(with_ord_integrity[x][1])

        to_merge_index = find_lowest(entry_mem, 'ordinal')

        to_merge = []
        to_merge_trust = []

        for x in range(len(to_merge_index)):
            to_merge.append(entry_mem[to_merge_index[x]])
            to_merge_trust.append(with_ord_integrity_trust[to_merge_index[x]])
            del (with_ord_integrity[to_merge_index[x]])[1]

        for x in range(len(to_merge_index)):
            if len(with_ord_integrity[to_merge_index[x] - x]) < 2:
                del with_ord_integrity[to_merge_index[x] - x]

        output.append(merge(to_merge, to_merge_trust))

        if len(with_ord_integrity) == 0:
            break
        a = a + 1
        if a == 20:
            break

    print(tabulate(output, headers="keys"))

    return output


# The merging function ie. Part 2
def merge(to_merge, trust):

    ordinal = to_merge[0]['ordinal']

    # acronym
    current_value = ['null']
    current_trust = [0]
    for x in range(len(to_merge)):
        if not to_merge[x]['acronym'] is None and not "null" in to_merge[x]['acronym'] and not "missing" in to_merge[x]['acronym'] and not "error" in to_merge[x]['acronym']:
            has_found = False
            for i in range(len(current_value)):
                if current_value[i] == to_merge[x]['acronym']:
                    current_trust[i] = current_trust[i] + trust[x]
                    has_found = True
            if not has_found:
                current_value.append(to_merge[x]['acronym'])
                current_trust.append(trust[x])
    acronym = current_value[index_with_highest_value(current_trust)]

    # acronym2
    current_value = ['null']
    current_trust = [0]
    for x in range(len(to_merge)):
        if not to_merge[x]['acronym2'] is None and not "null" in to_merge[x]['acronym2'] and not "missing" in to_merge[x]['acronym2'] and not "error" in to_merge[x]['acronym2']:
            has_found = False
            for i in range(len(current_value)):
                if current_value[i] == to_merge[x]['acronym2']:
                    current_trust[i] = current_trust[i] + trust[x]
                    has_found = True
            if not has_found:
                current_value.append(to_merge[x]['acronym2'])
                current_trust.append(trust[x])
    acronym2 = current_value[index_with_highest_value(current_trust)]

    # year
    current_value = ['null']
    current_trust = [0]
    for x in range(len(to_merge)):
        if not to_merge[x]['year'] is None and type(to_merge[x]['year']) == int and int(to_merge[x]['year']) > 0:
            has_found = False
            for i in range(len(current_value)):
                if current_value[i] == int(to_merge[x]['year']):
                    current_trust[i] = current_trust[i] + trust[x]
                    has_found = True
            if not has_found:
                current_value.append(int(to_merge[x]['year']))
                current_trust.append(trust[x])
    year = current_value[index_with_highest_value(current_trust)]

    # from
    current_value = ['null']
    current_trust = [0]
    for x in range(len(to_merge)):
        if not to_merge[x]['from'] is None and not "null" in to_merge[x]['from'] and not "missing" in to_merge[x]['from'] and not "error" in to_merge[x]['from'] and not "00.00.00" in to_merge[x]['from']:
            has_found = False
            for i in range(len(current_value)):
                if current_value[i] == to_merge[x]['from']:
                    current_trust[i] = current_trust[i] + trust[x]
                    has_found = True
            if not has_found:
                current_value.append(to_merge[x]['from'])
                current_trust.append(trust[x])
    from_date = current_value[index_with_highest_value(current_trust)]

    # to
    current_value = ['null']
    current_trust = [0]
    for x in range(len(to_merge)):
        if not to_merge[x]['to'] is None and not "null" in to_merge[x]['to'] and not "missing" in to_merge[x]['to'] and not "error" in to_merge[x]['to'] and not "00.00.00" in to_merge[x]['to']:
            has_found = False
            for i in range(len(current_value)):
                if current_value[i] == to_merge[x]['to']:
                    current_trust[i] = current_trust[i] + trust[x]
                    has_found = True
            if not has_found:
                current_value.append(to_merge[x]['to'])
                current_trust.append(trust[x])
    to_date = current_value[index_with_highest_value(current_trust)]

    # country
    current_value = ['null']
    current_trust = [0]
    for x in range(len(to_merge)):
        if not to_merge[x]['country'] is None and not "null" in to_merge[x]['country'] and not "missing" in to_merge[x]['country'] and not "error" in to_merge[x]['country']:
            has_found = False
            for i in range(len(current_value)):
                if current_value[i] == to_merge[x]['country']:
                    current_trust[i] = current_trust[i] + trust[x]
                    has_found = True
            if not has_found:
                current_value.append(to_merge[x]['country'])
                current_trust.append(trust[x])
    country = current_value[index_with_highest_value(current_trust)]

    # region
    current_value = ['null']
    current_trust = [0]
    for x in range(len(to_merge)):
        if not to_merge[x]['region'] is None and not "null" in to_merge[x]['region'] and not "missing" in to_merge[x]['region'] and not "error" in to_merge[x]['region']:
            has_found = False
            for i in range(len(current_value)):
                if current_value[i] == to_merge[x]['region']:
                    current_trust[i] = current_trust[i] + trust[x]
                    has_found = True
            if not has_found:
                current_value.append(to_merge[x]['region'])
                current_trust.append(trust[x])
    region = current_value[index_with_highest_value(current_trust)]

    # city
    current_value = ['null']
    current_trust = [0]
    for x in range(len(to_merge)):
        if not to_merge[x]['city'] is None and not "null" in to_merge[x]['city'] and not "missing" in to_merge[x]['city'] and not "error" in to_merge[x]['city']:
            has_found = False
            for i in range(len(current_value)):
                if current_value[i] == to_merge[x]['city']:
                    current_trust[i] = current_trust[i] + trust[x]
                    has_found = True
            if not has_found:
                current_value.append(to_merge[x]['city'])
                current_trust.append(trust[x])
    city = current_value[index_with_highest_value(current_trust)]

    # gnd
    current_value = ['null']
    current_trust = [0]
    for x in range(len(to_merge)):
        if 'gnd' in to_merge[x].keys() and not to_merge[x]['gnd'] is None and not "null" in to_merge[x]['gnd'] and not "missing" in to_merge[x]['gnd'] and not "error" in to_merge[x]['gnd']:
            has_found = False
            for i in range(len(current_value)):
                if current_value[i] == to_merge[x]['gnd']:
                    current_trust[i] = current_trust[i] + trust[x]
                    has_found = True
            if not has_found:
                current_value.append(to_merge[x]['gnd'])
                current_trust.append(trust[x])
    gnd = current_value[index_with_highest_value(current_trust)]

    # dblp
    current_value = ['null']
    current_trust = [0]
    for x in range(len(to_merge)):
        if 'dblp' in to_merge[x].keys() and not to_merge[x]['dblp'] is None and not "null" in to_merge[x]['dblp'] and not "missing" in to_merge[x]['dblp'] and not "error" in to_merge[x]['dblp']:
            has_found = False
            for i in range(len(current_value)):
                if current_value[i] == to_merge[x]['dblp']:
                    current_trust[i] = current_trust[i] + trust[x]
                    has_found = True
            if not has_found:
                current_value.append(to_merge[x]['dblp'])
                current_trust.append(trust[x])
    dblp = current_value[index_with_highest_value(current_trust)]

    # wikicfpID
    current_value = ['null']
    current_trust = [0]
    for x in range(len(to_merge)):
        if 'wikicfpID' in to_merge[x].keys() and not to_merge[x]['wikicfpID'] is None and not "null" in to_merge[x]['wikicfpID'] and not "missing" in to_merge[x]['wikicfpID'] and not "error" in to_merge[x]['wikicfpID']:
            has_found = False
            for i in range(len(current_value)):
                if current_value[i] == to_merge[x]['wikicfpID']:
                    current_trust[i] = current_trust[i] + trust[x]
                    has_found = True
            if not has_found:
                current_value.append(to_merge[x]['wikicfpID'])
                current_trust.append(trust[x])
    wikicfpID = current_value[index_with_highest_value(current_trust)]

    # or
    current_value = ['null']
    current_trust = [0]
    for x in range(len(to_merge)):
        if 'or' in to_merge[x].keys() and not to_merge[x]['or'] is None and not "null" in to_merge[x]['or'] and not "missing" in to_merge[x]['or'] and not "error" in to_merge[x]['or']:
            has_found = False
            for i in range(len(current_value)):
                if current_value[i] == to_merge[x]['or']:
                    current_trust[i] = current_trust[i] + trust[x]
                    has_found = True
            if not has_found:
                current_value.append(to_merge[x]['or'])
                current_trust.append(trust[x])
    or_id = current_value[index_with_highest_value(current_trust)]

    # wikidata
    current_value = ['null']
    current_trust = [0]
    for x in range(len(to_merge)):
        if 'wikidata' in to_merge[x].keys() and not to_merge[x]['wikidata'] is None and not "null" in to_merge[x]['wikidata'] and not "missing" in to_merge[x]['wikidata'] and not "error" in to_merge[x]['wikidata']:
            has_found = False
            for i in range(len(current_value)):
                if current_value[i] == to_merge[x]['wikidata']:
                    current_trust[i] = current_trust[i] + trust[x]
                    has_found = True
            if not has_found:
                current_value.append(to_merge[x]['wikidata'])
                current_trust.append(trust[x])
    wikidata = current_value[index_with_highest_value(current_trust)]

    # confref
    current_value = ['null']
    current_trust = [0]
    for x in range(len(to_merge)):
        if 'confref' in to_merge[x].keys() and not to_merge[x]['confref'] is None and not "null" in to_merge[x]['confref'] and not "missing" in to_merge[x]['confref'] and not "error" in to_merge[x]['confref']:
            has_found = False
            for i in range(len(current_value)):
                if current_value[i] == to_merge[x]['confref']:
                    current_trust[i] = current_trust[i] + trust[x]
                    has_found = True
            if not has_found:
                current_value.append(to_merge[x]['confref'])
                current_trust.append(trust[x])
    confref = current_value[index_with_highest_value(current_trust)]

    # seriesAcronym
    current_value = ['null']
    current_trust = [0]
    for x in range(len(to_merge)):
        if not to_merge[x]['seriesAcronym'] is None and not "null" in to_merge[x]['seriesAcronym'] and not "missing" in to_merge[x]['seriesAcronym'] and not "error" in to_merge[x]['seriesAcronym']:
            has_found = False
            for i in range(len(current_value)):
                if current_value[i] == to_merge[x]['seriesAcronym']:
                    current_trust[i] = current_trust[i] + trust[x]
                    has_found = True
            if not has_found:
                current_value.append(to_merge[x]['seriesAcronym'])
                current_trust.append(trust[x])
    seriesAcronym = current_value[index_with_highest_value(current_trust)]

    # title
    current_value = ['null']
    current_trust = [0]
    for x in range(len(to_merge)):
        if not to_merge[x]['title'] is None and not "null" in to_merge[x]['title'] and not "missing" in to_merge[x]['title'] and not "error" in to_merge[x]['title']:
            has_found = False
            for i in range(len(current_value)):
                if current_value[i] == to_merge[x]['title']:
                    current_trust[i] = current_trust[i] + trust[x]
                    has_found = True
            if not has_found:
                current_value.append(to_merge[x]['title'])
                current_trust.append(trust[x])
    title = current_value[index_with_highest_value(current_trust)]

    output = {'acronym': acronym, 'acronym2': acronym2, 'ordinal': ordinal, 'year': year, 'from': from_date,
              'to': to_date, 'country': country, 'region': region, 'city': city, 'gnd': gnd, 'dblp': dblp,
              'wikicfpID': wikicfpID, 'or': or_id, 'wikidata': wikidata, 'confref': confref,
              'seriesAcronym': seriesAcronym, 'title': title}

    return output


def index_with_highest_value(list):
    index = 0
    highest = 0
    for x in range(len(list)):
        if highest < list[x]:
            highest = list[x]
            index = x
    print(index)
    return index


def find_lowest(mem, key):
    temp_value = int(mem[0][key])
    index = [0]
    for x in range(1, len(mem)):
        if not mem[x][key] == 'null' and int(mem[x][key]) < temp_value:
            temp_value = int(mem[x][key])
            index = [x]
        else:
            if not mem[x][key] == 'null' and int(mem[x][key]) == temp_value:
                index.append(x)

    return index

