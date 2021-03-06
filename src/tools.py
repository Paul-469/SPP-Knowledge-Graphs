# includes all functions that may be useful beyond one file
import re
from dataclasses import dataclass

from tabulate import tabulate

num_dict = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'zero': 0,
    'ten': 10,
    'elven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,

    'first': 1,
    'second': 2,
    'third': 3,
    'fourth': 4,
    'fifth': 5,
    'sixth': 6,
    'seventh': 7,
    'eighth': 8,
    'ninth': 9,
    'tenth': 10,
    'eleventh': 11,
    'twelfth': 12,
    'thirteenth': 13,
    'fourteenth': 14,
    'fifteenth': 15,
    'sixteenth': 16,
    'seventeenth': 17,
    'eighteenth': 18,
    'nineteenth': 19,
    # bigger numbers
    'twentieth': 20,
    'twenty': 20,
    'thirtieth': 30,
    'thirty': 30,
    'fortieth': 40,
    'forty': 40,
    'fourtieth': 40,  # just in case spelling is done with ou
    'fourty': 40,  # "
    'fiftieth': 50,
    'fifty': 50,
    'sixtieth': 60,
    'sixty': 60,
    'seventieth': 70,
    'seventy': 70,
    'eightieth': 80,
    'eighty': 80,
    'ninetieth': 90,
    'ninety': 90,
    'hundredth': 100,
    'one hundredth': 100,
    'onehundredth': 100,  # just in case
}

month_dict = {
    # Full months
    'january': 1,
    'february': 2,
    'march': 3,
    'april': 4,
    'may': 5,
    'june': 6,
    'july': 7,
    'august': 8,
    'september': 9,
    'october': 10,
    'november': 11,
    'december': 12,

    # abbreviations
    'jan': 1,
    'feb': 2,
    'mar': 3,
    'apr': 4,
    'jun': 6,
    'jul': 7,
    'aug': 8,
    'sep': 9,
    'sept': 9,
    'oct': 10,
    'nov': 11,
    'dec': 12,
}
frequency_dict = {
    'annual': 1,
    'annu.': 1,
    'ann.': 1,
    'biannual': 2,
    'biannu.': 2,
    'quarterly': 4,
    'qtly.': 4,
    'qr.': 4,
    'weekly': 52,
    'wkly': 52,
    'mthly.': 12,
    'mth.': 12,
    'monthly': 12,
    'bimonthly': 24,
    'bi-monthly': 24,
    'biennial': 200,
    'triennial': 300,
    'quadrennial': 400,
    'quinquennial': 500,
    'decennial': 1000,
}


@dataclass
class FTDate:
    f_y: int = 0
    f_m: int = 0
    f_d: int = 0
    t_y: int = 0
    t_m: int = 0
    t_d: int = 0


@dataclass
class loc:
    city: str = ''
    region: str = ''
    country: str = ''


# returns the ordinal for most inputs as long as they are below 199
def ordinalToInt(ordinalInput: str):  # returns an int value for an ordinal input. returns 0 in none is found
    ordinalInput = ordinalInput.lower()  # ignore case
    output = 0
    if hasNumbers(ordinalInput):  # we assume that if there is a number in the ordinal value it'll sth. like 14th
        output = ''.join(filter(str.isdigit, ordinalInput))  # filter everything that's not a digit
    else:
        for k in num_dict:
            if k in ordinalInput:
                ordinalInput = ordinalInput.replace(k, "", 1)
                output = output + num_dict[k]
    # print(output)
    return int(output)


def hasNumbers(inputString: str):  # check whether there are numbers in the ordinal value
    return any(char.isdigit() for char in inputString)


def find_ordinal(foundEntities, res, index):
    temp = 'null'
    ordinal_list = []
    event_list = []
    counter = 0
    final_count = 0

    # source specific vars (initialized as used in dblp
    series = 'series'

    # for wikicfp
    if any('locality' in d for d in res):
        series = 'acronym'

    # for confref
    if any('ranks' in d for d in res):
        series = 'acronym'

    # for proceedings.com
    if type(res[index]) == tuple:
        series = 1

    for i in range(len(foundEntities)):
        # print(tabulate(foundEntities, headers="keys"))
        if 'EVENT' in foundEntities[i]['Entity Tag']:
            event_list.append(foundEntities[i]['Text'])

    for i in range(len(event_list)):
        if len(event_list[i]) < 20:  # if the event entry is longer than 20 chars we assume that we have a title here
            if res[index][series] in event_list[i]:
                temp_str = re.sub(r"[^a-zA-Z0-9]+", '$',
                                  temp_str)  # we assume that if more than one acronym is in an element they will be split by a special character
                temp_str = event_list[i].replace(res[index][series], "??")
                for element in range(len(temp_str)):
                    if temp_str[element] == "$":
                        counter = counter + 1
                    if temp_str[element] == "$":
                        final_count = counter

    for i in range(len(foundEntities)):
        if 'ORDINAL' in foundEntities[i]['Entity Tag']:
            ordinal_list.append(foundEntities[i]['Text'])
            temp = ordinalToInt(foundEntities[i]['Text'])

    if not ordinal_list:  # see whether we found any ordinals
        temp = 'null'
    else:
        if temp == 0:
            temp = 'null'
        else:
            temp = ordinalToInt(ordinal_list[final_count % len(
                ordinal_list)])  # prevent that we will ever be out of bounds which should not happen. Technically choosing the last entry would make more sense but we are talking about an edge case of an edge case here anyways

    return temp


# very rudimentary function to tell me how many characters are between two strings in a string
def string_distance(search_in: str, search1: str, search2: str):
    search_in = search_in.lower()
    search1 = search1.lower()
    search2 = search2.lower()
    search_in = search_in.replace(search1, '??', 1)
    search_in = search_in.replace(search2, '??', 1)
    counter = -1
    start = False
    for x in range(len(search_in)):

        if search_in[x] == '??':

            if not start:
                start = True
                # counter = 0
            else:
                break
        if start:
            counter = counter + 1

    return counter


# TODO make it more generic so it handles more inputs and especially start and end in different months
# very naive assumes a very basic format and that nothing start in a different year that it ends in
def get_from_to(foundEntities, res, index, nlp):
    # some sources have that data in a neat format so first we check whether we are dealing with one of those and if so
    # extract it from there
    # for example dblp doesn't but wikicfp does

    # for confref
    if any('ranks' in d for d in res):
        result = FTDate
        if not res[index]['startDate'] is None:
            start = res[index]['startDate'].split('-')
            result.f_d = start[2]
            result.f_m = start[1]
            result.f_y = start[0]
        if not res[index]['endDate'] is None:
            end = res[index]['endDate'].split('-')
            result.t_d = end[2]
            result.t_m = end[1]
            result.t_y = end[0]

        return result

    # for wikicfp
    if any('locality' in d for d in res):
        result = FTDate
        if not res[index]['startDate'] is None:
            start = res[index]['startDate'].split()
            result.f_d = start[1]
            for k in month_dict:
                if k in start[2].lower():
                    result.f_m = month_dict[k]
            result.f_y = start[3]
        if not res[index]['endDate'] is None:
            end = res[index]['endDate'].split()
            result.t_d = end[1]
            for k in month_dict:
                if k in end[2].lower():
                    result.t_m = month_dict[k]
            result.t_y = end[3]

        return result

    # for proceedings.com
    if type(res[index]) == tuple:
        result = FTDate

        items = res[index][4].split()
        # check whether we have an event starting in one month and ending in another if so: do the else part
        if items[4] != '-':

            days = items[1].split('-')

            result.f_d = days[0]
            for k in month_dict:
                if k in items[2].lower():
                    result.f_m = month_dict[k]
            result.f_y = ''.join(e for e in items[3] if e.isalnum())

            result.t_d = days[1]
            for k in month_dict:
                if k in items[2].lower():
                    result.t_m = month_dict[k]
            result.t_y = ''.join(e for e in items[3] if e.isalnum())
        else:

            result.f_d = items[1]
            for k in month_dict:
                if k in items[2].lower():
                    result.f_m = month_dict[k]
            result.f_y = ''.join(e for e in items[6] if e.isalnum())

            result.t_d = items[4]
            for k in month_dict:
                if k in items[5].lower():
                    result.t_m = month_dict[k]
            result.t_y = ''.join(e for e in items[6] if e.isalnum())

        return result

    date_list = []
    for i in range(len(foundEntities)):
        if 'DATE' in foundEntities[i]['Entity Tag']:
            date_list.append(foundEntities[i]['Text'])

    date_extract = nlp(''.join(str(e) for e in date_list))
    new_foundEntities = [{"Text": entity.text, "Entity Tag": entity.label_} for entity in date_extract.ents]
    # print(tabulate(new_foundEntities, headers="keys"))

    pattern = r'\d[0-9\-]*'
    result = 'null'
    result_completion = 0
    # TODO remove this for loop or make it useful
    # I know this for loop does fuck all if we return on the first loop iteration but I can't be asked to properly
    # remove it right now. likewise yes I'm aware that some of the variables are useless because of it
    for i in range(len(new_foundEntities)):
        temp_result = FTDate

        # Start and end month
        temp_months = []
        for k in month_dict:
            if k in new_foundEntities[i]['Text'].lower():
                new_foundEntities[i]['Text'] = str(new_foundEntities[i]['Text']).lower().replace(str(k), '', 1)
                temp_months.append(month_dict[k])
        if len(temp_months) == 0:
            temp_result.f_m = 0
            temp_result.t_m = 0
        else:
            if len(temp_months) == 1:
                temp_result.f_m = temp_months[0]
                temp_result.t_m = temp_months[0]
                result_completion = result_completion + 2
            else:
                temp_months.sort()
                temp_result.f_m = temp_months[0]
                temp_result.t_m = temp_months[len(temp_months) - 1]
                result_completion = result_completion + 2

        numbers = re.findall(pattern, new_foundEntities[i]['Text'].lower())
        # print(numbers)

        # Find year
        found_year = False
        numbers.sort(reverse=True)
        for x in range(len(numbers)):
            if '-' not in numbers[x]:
                if 1900 < int(numbers[x]) < 2100:  # we set bounds trying to avoid finding sth that is not a year
                    found_year = True
                    temp_result.f_y = temp_result.t_y = numbers[x]
                    break

        # start and end day
        found_day = False
        for x in range(len(numbers)):
            # print(numbers)
            if '-' in numbers[x]:
                # print(numbers[x].split('-', 1))
                # print(type(numbers[x].split('-', 1)[0]))
                # print(type(numbers[x].split('-', 1)[1]))
                # type(numbers[x].split('-', 1)[0]) is str and type(numbers[x].split('-', 1)[1]) is str
                if not numbers[x].split('-', 1)[0] == '' and not numbers[x].split('-', 1)[1] == '':
                    found_day = True
                    if found_year:  # sometimes the Year is in this which would result in a wonky day number
                        if temp_result.f_y in numbers[x]:
                            numbers[x] = str(numbers[x]).replace(str(temp_result.f_y), '', 1)
                    days = numbers[x].split('-')
                    temp_result.f_d = days[0]
                    temp_result.t_d = days[1]
        if not found_day:
            # print(temp_result.f_m)
            # print(temp_result.t_m)
            if not temp_result.t_m == temp_result.f_m:
                if len(numbers) > 2:
                    numbers.sort(reverse=False)
                    temp_result.f_d = numbers[1]  # from should be the lager number as it is the last day of the month
                    temp_result.t_d = numbers[0]
            else:
                if len(numbers) > 1:
                    numbers.sort(reverse=False)
                    temp_result.f_d = temp_result.t_d = numbers[0]

        # print(temp_result.f_y)
        # print(temp_result.f_m)
        # print(temp_result.f_d)
        # print(temp_result.t_y)
        # print(temp_result.t_m)
        # print(temp_result.t_d)

        # print(str(temp_result))
        return temp_result


# Returns the location either from the location entry or title
# also for cc Exciter UK or United Kingdom needs to be patched also Munich is most likely to be M??nchen
# also as we use nlp before location look up we might need to catch the online case
def location_finder(ll, res, index, nlp):
    # a bunch of vars that should be self explanatory
    return_val = loc
    had_entries_city = False
    had_entries_region = False
    had_entries_country = False
    has_such_columns = True
    title = 'title'

    # Keys for different sources (initialized for the dblp values)
    city = 'city'
    region = 'region'
    country = 'country'
    location_tab = 'location'

    # for proceedings.com
    if type(res[index]) == tuple:
        location_tab = 4
        has_such_columns = False
        title = 1
        # Fix for
        if 'Virtual Conference' in res[index][title]:
            loc.city = 'online'
            loc.region = 'online'
            loc.country = 'online'
            return loc


    # for wikicfp
    if any('locality' in d for d in res):
        location_tab = 'locality'
    # the data set is fucking unreliable, we need to make sure that location if not empty contains a location and if not
    # we still need to verify whether the title might. if both are false we need this var and fill in null
    no_further_location_data = False

    # grab info from the columns. This might be misplaced trust but let's assume that this is a corner case we don't
    # concern ourself with
    if has_such_columns:
        if not res[index][city] is None:
            loc.city = res[index][city]
            had_entries_city = True

        if not res[index][region] is None:
            loc.region = res[index][region]
            had_entries_region = True

        if not res[index][country] is None:
            loc.country = res[index][country]
            had_entries_country = True

    # print(res[index][city])
    # print(loc.city)
    # print(res[index][region])
    # print(loc.region)
    # print(res[index][country])
    # print(loc.country)
    # print(res[index])

    # if so we can return early
    if had_entries_city and had_entries_region and had_entries_country:
        return return_val
    else:
        # Get location from either location column or title.
        # we use nlp here. lookup can handle a title just fine but the result can be off for whatever reason
        # I think using nlp will create fewer problems than it solves
        # the old implementation is still as a comment at the end of the testQuerryToTable.py file
        if res[index][title] is None:
            doc = nlp('')
        else:
            doc = nlp(res[index][title])
        fromTitle = [{"Text": entity.text, "Entity Tag": entity.label_} for entity in doc.ents]
        if res[index][location_tab] is None:
            doc = nlp('')
        else:
            doc = nlp(res[index][location_tab])
        fromLocation = [{"Text": entity.text, "Entity Tag": entity.label_} for entity in doc.ents]
        found = False
        for x in range(len(fromLocation)):
            if fromLocation[x]['Entity Tag'] == 'GPE':
                result = ll.lookup(fromLocation[x]['Text'])
                found = True
                break
        if not found:
            for x in range(len(fromTitle)):
                if fromTitle[x]['Entity Tag'] == 'GPE':
                    result = ll.lookup(fromTitle[x]['Text'])
                    found = True
                    break
        if not found:
            no_further_location_data = True

        # we fill in missing data from the location lookup
        if not had_entries_city:
            if no_further_location_data:
                loc.city = "null"
            else:
                loc.city = str(result).split("(", 1)[0]
        if not had_entries_region:
            if no_further_location_data:
                loc.region = "null"
            else:
                if hasattr(result, '_region'):
                    loc.region = str(result._region)[str(result._region).find("(") + 1:str(result._region).find(")")]
                else:
                    loc.region = "null"
        if not had_entries_region:
            if no_further_location_data:
                loc.country = "null"
            else:
                if hasattr(result, '_country'):
                    loc.country = str(result._country)[str(result._country).find("(") + 1:str(result._country).find(")")]
                else:
                    loc.country = "null"

    return return_val


# a rudimentary attempt to fix simple ordinal errors. Relies heavily on the year being available
# currently only fixes singular errors
def fix_ordinal(dict):
    # divide all present ordinals into chunks that contain a consistent series
    chain_list = []
    ord_list = []
    for x in range(len(dict)):
        if dict[x]['title'] == 'null':  # ignore null entries
            continue

        # make sure that if we miss an ordinal we have no None type but also can be sure that it is defiantly wrong
        if dict[x]['ordinal'] is None or dict[x]['ordinal'] == 'null':
            dict[x]['ordinal'] = -1

        if dict[x]['ordinal'] == 'null':  # check for a missing ordinal
            chain_list.append(ord_list)
            chain_list.append([dict[x]['ordinal']])
            ord_list = []
            continue
        if x + 1 >= len(dict):  # see whether we are on the last entry
            if int(dict[x]['ordinal']) - 1 == int(dict[x - 1]['ordinal']):
                ord_list.append(dict[x]['ordinal'])
                chain_list.append(ord_list)
            else:
                chain_list.append([dict[x]['ordinal']])
            continue

        # make sure that if we miss an ordinal we have no None type but also can be sure that it is defiantly wrong
        if dict[x+1]['ordinal'] is None or dict[x+1]['ordinal'] == 'null':
            dict[x+1]['ordinal'] = -1

        if int(dict[x]['ordinal']) + 1 == int(dict[x + 1]['ordinal']):
            ord_list.append((dict[x]['ordinal']))
        else:
            if int(dict[x]['ordinal']) < int(dict[x + 1]['ordinal']):
                ord_list.append(dict[x]['ordinal'])
                chain_list.append(ord_list)
                ord_list = []
            if int(dict[x]['ordinal']) >= int(dict[x + 1]['ordinal']):
                ord_list.append(dict[x]['ordinal'])
                chain_list.append(ord_list)
                ord_list = []

    # return if we found no errors
    if len(chain_list) == 1:
        return dict

    # Fix ordinal errors if it's reasonable to assume that they are errors

    for y in range(len(chain_list)):

        # calc the index in the dict
        index_in_dict = 1
        for z in range(y-1):
            index_in_dict = index_in_dict + len(chain_list[z])
        index_in_dict = index_in_dict + 1

        # first ordinal series
        if y == 0:
            if len(chain_list[y]) == 1:  # we only attempt correcting if we don't have a series of ordinals

                # if the following event is next year we assume that the it our current event is a direct predecessor
                if int(dict[index_in_dict]['year']) + 1 == int(dict[index_in_dict + 1]['year']):
                    (chain_list[y])[0] = int((chain_list[y+1])[0]) - 1
            continue

        # last ordinal series
        if y + 1 == len(chain_list):
            if len(chain_list[y]) == 1:  # we only attempt correcting if we don't have a series of ordinals

                # if the preceding event is a year prior we assume that the it our current event is a direct successor
                if int(dict[index_in_dict]['year']) - 1 == int(dict[index_in_dict - 1]['year']):
                    (chain_list[y])[0] = int((chain_list[y - 1])[0]) + 1
            continue

        # everything else
        # tho for now i would only attempt to try to fix singular  errors ie. len(chain_list) == 1

        if len(chain_list[y]) == 1:
            previous_year = int(dict[index_in_dict - 1]['year'])
            current_year = int(dict[index_in_dict]['year'])
            next_year = int(dict[index_in_dict + 1]['year'])

            if next_year - 1 == current_year == previous_year + 1 & int((chain_list[y-1])[-1]) + 2 == int((chain_list[y+1])[0]):
                chain_list[y][0] = int((chain_list[y-1])[-1]) + 1
            else:
                # if the within the next two entries the series is continued and does not violate the year we will
                # correct the error
                # if we are almost at the end of a list we can't do much in order to correct errors

                if index_in_dict + 2 < len(dict):
                    next_next_year = int(dict[index_in_dict + 2]['year'])
                else:
                    continue

                if index_in_dict + 3 < len(dict):
                    next_next_next_year = int(dict[index_in_dict + 3]['year'])
                else:
                    # we can't know whether the series holds for more than year longer as we are at the end
                    continue # TODO decide whether one more year been known is enough to decide

                # see whether the year series is continued
                if next_next_next_year - 3 == next_next_year -2 == next_year - 1 == current_year == previous_year + 1:
                    if y + 2 < len(chain_list) and 1 == len(chain_list[y+1]):
                        if int((chain_list[y - 1])[-1]) + 3 == int((chain_list[y+2])[0]):
                            chain_list[y][0] = int((chain_list[y - 1])[-1]) + 1
                            chain_list[y+1][0] = int(chain_list[y][0]) + 1
                    else:
                        if y + 1 < len(chain_list) and 1 > len(chain_list[y+1]):
                            from_next_next = int((chain_list[y + 1])[1])
                            if y + 2 < len(chain_list) and 1 == len(chain_list[y + 1]):
                                if int((chain_list[y - 1])[-1]) + 3 == int((chain_list[y + 2])[0]):
                                    chain_list[y][0] = int((chain_list[y - 1])[-1]) + 1
                                    chain_list[y + 1][0] = int(chain_list[y][0]) + 1

    # join the result into one list
    final_list = []
    for y in range(len(chain_list)):
        final_list = final_list + chain_list[y]

    # update the dict
    i = 0
    for z in range(len(dict)):
        if dict[z]['title'] == 'null':  # ignore null entries
            continue
        dict[z]['ordinal'] = str(final_list[i])
        dict[z]['acronym2'] = str(dict[z]['acronym2'].split("-", 1)[0]) + '-' + str(final_list[i])
        i = i + 1

        # if sth. goes wrong we want to prevent an out of bounds error for the index
        if i >= len(final_list):
            i = len(final_list) - 1

    return dict


# We remove events that were returned but do not share the same acronym as the input from the final list
# This should be redundant now as we have removeFalsePostivesEarly.
# Moreover it is very strict i.e. prefect match,  so it may not be so useful
def removeFalsePositives(dict, input):
    to_remove = []
    for x in range(len(dict)):
        if not input.lower() == dict[x]['seriesAcronym'].lower():
            to_remove.append(x)

    for x in range(len(to_remove)):
        del dict[to_remove[x] - x]

    return dict


# remove events from the query output whos acronym does not match the input
def removeFalsePostivesEarly(res, input):

    # source specific var
    acronym = 'series'

    # for wikicfp
    if any('locality' in d for d in res):
        acronym = 'acronym'

    # for confref
    if any('ranks' in d for d in res):
        acronym = 'acronym'

    # for gnd
    if any('regionIso' in d for d in res):
        acronym = 'acronym'

    to_remove = []
    for x in range(len(res)):
        if findWholeWord(input)(res[x][acronym]) is None or ("IEEE" in res[x][acronym] and not "IEEE" in input):
            to_remove.append(x)

    for x in range(len(to_remove)):
        del res[to_remove[x] - x]

    return res


# Function I nicked from stackoverflow: https://stackoverflow.com/a/5320179
def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


# Inverts the dict but keeps the null line as the fist line of the dict. (It expects there to be one)
def invertDict(dict):
    out = [dict[0]]
    for x in range(1, len(dict)):
        out.append(dict[len(dict) - x])
    return out


# determine the frequency of an event. We assume an ordered data set and that we only have one series in the table and
# deduplicated
def freq(dict):
    fr = 0
    no_conflict = True

    # first by title
    for x in range(1, len(dict)):
        for key in frequency_dict:
            if not dict[x]['title'] is None:
                if key in dict[x]['title']:
                    if frequency_dict[key] == fr or fr == 0:
                        fr = frequency_dict[key]
                    else:
                        no_conflict = False

    # determine via years and ordinals
    if fr == 0:
        first_ord = 0
        if not dict[1]['ordinal'] == 'null':
            first_ord = int(dict[1]['ordinal'])
        else:
            for x in range(1, len(dict)):
                if not dict[x]['ordinal'] == 'null':
                    first_ord = int(dict[1]['ordinal'])
        if first_ord == 0:
            return 'could not be determined'

        last_ord = 0
        if not dict[-1]['ordinal'] == 'null':
            last_ord = int(dict[-1]['ordinal'])
        else:
            for x in range(len(dict), 1, -1):
                if not dict[x]['ordinal'] == 'null':
                    last_ord = int(dict[1]['ordinal'])
        if last_ord == 0:
            return 'could not be determined'
        if last_ord == first_ord:
            return 'could not be determined'

        first_year = int(dict[1]['year'])
        last_year = int(dict[-1]['year'])

        no_of_present_events = last_ord - first_ord
        years_covered = last_year - first_year

        # print(no_of_present_events)
        # print(years_covered)
        # Note: Python 3.10 has case switch statements (match case) python 3.9 does not...
        # and I'm not building dict 'solution' for that so an if-else chain it is
        if no_of_present_events == years_covered:
            fr = 1
        else:
            if no_of_present_events == years_covered * 2:
                fr = 2
            else:
                if no_of_present_events == years_covered * 4:
                    fr = 4
                else:
                    if no_of_present_events == years_covered * 12:
                        fr = 12
                    else:
                        if no_of_present_events == years_covered * 24:
                            fr = 24
                        else:
                            if no_of_present_events == years_covered * 52:
                                fr = 52
                            else:
                                if no_of_present_events == years_covered / 2:
                                    fr = 200
                                else:
                                    if no_of_present_events == years_covered / 3:
                                        fr = 300
                                    else:
                                        if no_of_present_events == years_covered / 4:
                                            fr = 400
                                        else:
                                            if no_of_present_events == years_covered / 5:
                                                fr = 500
                                            else:
                                                if no_of_present_events == years_covered / 10:
                                                    fr = 1000

    # print(fr)
    if fr == 0 or not no_conflict:
        return 'could not be determined'
    else:
        keys = [k for k, v in frequency_dict.items() if v == fr]
        return keys[0]


# adds place holder for missing events to a list. We assume the list is deduplicated, ordered and only contains one
# series; the freq is expected to be in format described in the dict
def addGhostEvents(dict, freq):
    out = dict
    acr = 'null'
    yr = 0
    yr_min = 0
    multiplication = False
    first_ord = 0
    if not dict[1]['ordinal'] == 'null':
        first_ord = int(dict[1]['ordinal'])

    if not dict[1]['year'] == 'null':
        yr = int(dict[1]['year'])

    if not dict[1]['seriesAcronym'] == 'null':
        acr = dict[1]['seriesAcronym']

    factor = frequency_dict.get(freq, 0)
    if factor >= 100:
        factor = factor / 100
        multiplication = True

    # we add all ghosts until the first ord
    if first_ord != 1 and first_ord !=0:
        for x in range(first_ord-1, 0, -1):
            ord = x
            if multiplication:
                yr_min = yr_min - (1 * factor)
            else:
                yr_min = yr_min - (1 / factor)
            yr_temp = yr + int(yr_min)
            out.insert(1, {'acronym': acr + '-' + str(yr_temp), 'acronym2': acr + '-' + str(ord),
                           'ordinal': str(ord), 'year': yr_temp, 'seriesAcronym': acr, 'from':  'null', 'to':  'null', 'title': 'ghost', 'city': 'null', 'region': 'null', 'country': 'null'})

    # A not too accurate way of creating ghost entries with year but it should fill ordinal gaps
    x = 1
    while x < (len(out)-1):
        if not out[x]['ordinal'] == 'null' and not out[x-1]['ordinal'] == 'null':
            if int(out[x]['ordinal']) > 0:
                if int(out[x]['ordinal']) + 1 < int(dict[x+1]['ordinal']):
                    ord = int(out[x]['ordinal']) + 1
                    if not out[x]['year'] == 'null':
                        yr = int(out[x]['year'])
                        if multiplication:
                            yr = yr - (1 * factor)
                        else:
                            yr = yr - (1 / factor)
                    out.insert(x, {'acronym': acr + '-' + str(yr), 'acronym2': acr + '-' + str(ord),
                                   'ordinal': str(ord), 'year': yr, 'seriesAcronym': acr, 'from': 'null', 'to': 'null', 'title': 'ghost', 'city': 'null', 'region': 'null', 'country': 'null'})
        x += 1

    return out


# checks whether there are proper ordinals for all entries in a list
def ordinal_integrity(dict):
    for x in range(1, len(dict)):
        if not type(dict[x]['ordinal']) == int:
            if not dict[x]['ordinal'].isnumeric():
                return False
        else:
            if dict[x]['ordinal'] < 1:
                return False
    return True


# checks whether there are proper years for all entries in a list
def year_integrity(dict):
    for x in range(1, len(dict)):
        if not type(dict[x]['year']) == int:
            if not dict[x]['year'].isnumeric():
                return False
        else:
            if dict[x]['year'] < 1:
                return False
    return True


# determine if there is more than one annual series in an output we expect there to be an ordinal and year for
# every event
# !!!!!!!!!!!! returns the individual series not a bool !!!!!!!!!!!!!!!!!!!
def isThereMoreThanOne(dict):
    if len(dict) <=2:
        return
    last_ord = dict[1]['ordinal']
    last_year = dict[1]['year']
    ends = []

    for x in range(2, len(dict)):

        if int(last_ord) + 1 == int(dict[x]['ordinal']) and int(last_year) + 1 == int(dict[x]['year']):
            last_ord = dict[x]['ordinal']
            last_year = dict[x]['year']
        else:
            if int(last_year) + 1 >= int(dict[x]['year']):
                ends.append(x-1)
                last_ord = dict[x]['ordinal']
                last_year = dict[x]['year']
            else:
                if int(last_ord) + 1 < int(dict[x]['ordinal']) and int(last_year) + 1 < int(dict[x]['year']):
                    if x < len(dict):
                        if abs(last_ord-int(dict[x]['ordinal'])) == abs(last_year - int(dict[x]['year'])):
                            last_ord = dict[x]['ordinal']
                            last_year = dict[x]['year']
                        else:
                            ends.append(x - 1)
                            last_ord = dict[x]['ordinal']
                            last_year = dict[x]['year']

    out = [dict]
    for x in range(len(ends)):
        temp = out[0]
        out.append(temp[:int(ends[x])+1])
        temp = temp[ends[x]+1:len(temp)]
        temp.insert(0, {'acronym': 'null', 'acronym2': 'null', 'ordinal': 'null', 'year': 'null',
                                           'from': 'null', 'to': 'null', 'country': 'null', 'region': 'null',
                                           'city': 'null', 'gnd': 'null', 'dblp': 'null', 'wikicfpID': 'null',
                                           'or': 'null', 'wikidata': 'null', 'confref': 'null', 'seriesAcronym': 'null',
                                           'title': 'null'})
        out[0] = temp

    # we put the longest list in front
    max_len = 0
    index = 0
    for x in range(len(out)):
        if max_len < len(out[x]):
            max_len = len(out[x])
            index = x
    out.insert(0, out[index])
    out.pop(x)

    return out


# removes all entries from a lod that have broken or no ordinals and returns both
def remove_entries_without_ordinals(lod):
    out = lod
    out_inverted = [{'acronym': 'null', 'acronym2': 'null', 'ordinal': 'null', 'year': 'null',
                                           'from': 'null', 'to': 'null', 'country': 'null', 'region': 'null',
                                           'city': 'null', 'gnd': 'null', 'dblp': 'null', 'wikicfpID': 'null',
                                           'or': 'null', 'wikidata': 'null', 'confref': 'null', 'seriesAcronym': 'null',
                                           'title': 'null'}]
    to_remove = []
    for x in range(1, len(lod)):
        if not type(lod[x]['ordinal']) == int:
            if not lod[x]['ordinal'].isnumeric():
                to_remove.append(x)

    for x in range(len(to_remove)):
        out_inverted.append(out[to_remove[x] - x])
        del out[to_remove[x] - x]

    return out, out_inverted


# sorts the list of dicts by year but keeps the null line in place and put every event with no year entry at the top
def sortDictByYear(dict):
    out = [dict[0]]
    dict.pop(0)
    to_exclude = []
    for x in range(len(dict)):
        if dict[x]['year'] is None or dict[x]['year'] == 'null':
            to_exclude.append(x)

    for x in range(len(to_exclude)):
        out.append(dict[to_exclude[x] - x])
        del dict[to_exclude[x] - x]

    out = out + qs(dict)
    return out


# a quicksort implementation for our purpose of sorting a LoD by 'year' if the list length exceeds the max amount of
# recursions this will fail but realistically this won't happen unless our queries are doing sth wrong
def qs(dict):
    if len(dict) <= 2:
        if len(dict) == 2:
            if int(dict[0]['year']) > int(dict[1]['year']):
                temp = dict[1]
                dict[1] = dict[0]
                dict[0] = temp
        return dict

    pivot = int(dict[int(len(dict) / 2)]['year'])
    pivot_element = dict[int(len(dict) / 2)]

    left = dict[:int(len(dict) / 2)]
    right = dict[int(len(dict) / 2):]
    right.pop(0)

    temp_add_r = []
    to_remove = []
    i = 0
    for x in left:
        if int(x['year']) > pivot:
            temp_add_r.append(x)
            to_remove.append(i)
        i = i + 1

    for x in range(len(to_remove)):
        del left[to_remove[x] - x]

    temp_add_l = []
    to_remove = []
    i = 0
    for x in right:
        if int(x['year']) <= pivot:
            temp_add_l.append(x)
            to_remove.append(i)
        i = i + 1

    for x in range(len(to_remove)):
        del right[to_remove[x] - x]

    for x in reversed(range(len(temp_add_r))):
        right.insert(0, temp_add_r[x])

    for x in reversed(range(len(temp_add_l))):
        left.append(temp_add_l[x])

    return qs(left) + [pivot_element] + qs(right)

