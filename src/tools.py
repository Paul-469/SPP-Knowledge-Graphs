# includes all functions that may be useful beyond one file
from tabulate import tabulate
import re
from dataclasses import dataclass

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


# Returns the location either from the location entry or title
def location_finder(ll, res, index):
    # a bunch of vars that should be self explanatory
    return_val = loc
    had_entries_city = False
    had_entries_region = False
    had_entries_country = False

    # the data set is fucking unreliable, we need to make sure that location if not empty contains a location and if not
    # we still need to verify whether the title might. if both are false we need this var and fill in null
    no_further_location_data = False

    # grab info from the columns. This might be misplaced trust but let's assume that this is a corner case we don't
    # concern ourself with
    if not res[index]['city'] is None:
        loc.city = res[index]['city']
        had_entries_city = True
    if not res[index]['region'] is None:
        loc.region = res[index]['region']
        had_entries_region = True
    if not res[index]['country'] is None:
        loc.country = res[index]['country']
        had_entries_country = True

    # if so we can return early
    if had_entries_city and had_entries_region and had_entries_country:
        return return_val
    else:
        # we look up the location from the location entry or the title depending on which works is any
        if not res[index]['location'] is None:
            result = ll.lookup(res[index]['location'])
            if result is None:
                result = ll.lookup(res[index]['title'])
        else:
            result = ll.lookup(res[index]['title'])
            if res is None:
                no_further_location_data = True

        # we fill in missing data from the location lookup
        if not had_entries_city:
            if no_further_location_data:
                loc.city = "null"
            else:
                loc.city = str(result).split(" ", 1)[0]
        if not had_entries_region:
            if no_further_location_data:
                loc.region = "null"
            else:
                loc.region = str(result._region)[str(result._region).find("(") + 1:str(result._region).find(")")]
        if not had_entries_region:
            if no_further_location_data:
                loc.country = "null"
            else:
                loc.country = str(result._country)[str(result._country).find("(") + 1:str(result._country).find(")")]

    return return_val


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

    for i in range(len(foundEntities)):
        # print(tabulate(foundEntities, headers="keys"))
        if 'EVENT' in foundEntities[i]['Entity Tag']:
            event_list.append(foundEntities[i]['Text'])

    for i in range(len(event_list)):
        if len(event_list[i]) < 20:  # if the event entry is longer than 20 chars we assume that we have a title here
            if res[index]['series'] in event_list[i]:
                temp_str = re.sub(r"[^a-zA-Z0-9]+", '$',
                                  temp_str)  # we assume that if more than one acronym is in an element they will be split by a special character
                temp_str = event_list[i].replace(res[index]['series'], "§")
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
    search_in = search_in.replace(search1, 'ß', 1)
    search_in = search_in.replace(search2, 'ß', 1)
    counter = -1
    start = False
    for x in range(len(search_in)):

        if search_in[x] == 'ß':

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
            if '-' in numbers[x]:
                found_day = True
                if found_year:  # sometimes the Year is in this which would result in a wonky day number
                    if temp_result.f_y in numbers[x]:
                        numbers[x] = str(numbers[x]).replace(str(temp_result.f_y), '', 1)
                days = numbers[x].split('-')
                temp_result.f_d = days[0]
                temp_result.t_d = days[1]
        if not found_day:
            if temp_result.t_m != temp_result.f_m:
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
def location_finder(ll, res, index):
    # a bunch of vars that should be self explanatory
    return_val = loc
    had_entries_city = False
    had_entries_region = False
    had_entries_country = False

    # the data set is fucking unreliable, we need to make sure that location if not empty contains a location and if not
    # we still need to verify whether the title might. if both are false we need this var and fill in null
    no_further_location_data = False

    # grab info from the columns. This might be misplaced trust but let's assume that this is a corner case we don't
    # concern ourself with
    if not res[index]['city'] is None:
        loc.city = res[index]['city']
        had_entries_city = True
    if not res[index]['region'] is None:
        loc.region = res[index]['region']
        had_entries_region = True
    if not res[index]['country'] is None:
        loc.country = res[index]['country']
        had_entries_country = True

    # if so we can return early
    if had_entries_city and had_entries_region and had_entries_country:
        return return_val
    else:
        # we look up the location from the location entry or the title depending on which works is any
        if not res[index]['location'] is None:
            result = ll.lookup(res[index]['location'])
            if result is None:
                result = ll.lookup(res[index]['title'])
        else:
            result = ll.lookup(res[index]['title'])
            if res is None:
                no_further_location_data = True

        # we fill in missing data from the location lookup
        if not had_entries_city:
            if no_further_location_data:
                loc.city = "null"
            else:
                loc.city = str(result).split(" ", 1)[0]
        if not had_entries_region:
            if no_further_location_data:
                loc.region = "null"
            else:
                loc.region = str(result._region)[str(result._region).find("(") + 1:str(result._region).find(")")]
        if not had_entries_region:
            if no_further_location_data:
                loc.country = "null"
            else:
                loc.country = str(result._country)[str(result._country).find("(") + 1:str(result._country).find(")")]

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
        if int(dict[x]['ordinal']) + 1 == int(dict[x + 1]['ordinal']):
            ord_list.append((dict[x]['ordinal']))
        else:
            if dict[x]['ordinal'] < dict[x + 1]['ordinal']:
                ord_list.append(dict[x]['ordinal'])
                chain_list.append(ord_list)
                ord_list = []
            if dict[x]['ordinal'] >= dict[x + 1]['ordinal']:
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
                next_next_year = int(dict[index_in_dict + 2]['year'])
                next_next_next_year = int(dict[index_in_dict + 3]['year'])
                # see whether the year series is continued
                if next_next_next_year - 3 == next_next_year -2 == next_year - 1 == current_year == previous_year + 1:
                    if int((chain_list[y - 1])[-1]) + 3 == int((chain_list[y+2])[0]):
                        chain_list[y][0] = int((chain_list[y - 1])[-1]) + 1
                        chain_list[y+1][0] = int(chain_list[y][0]) + 1

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