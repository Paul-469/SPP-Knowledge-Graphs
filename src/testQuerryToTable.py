

import corpusTools
from tabulate import tabulate
from corpus import location
import spacy
import re
from dataclasses import dataclass

# might not be complete and is limited to 199 ordinals (in part due to function implementation)
# we assume things are spelled correctly
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
    # I know this for loop does fuck all if return on the first loop iteration but I can't be asked to properly remove
    # it right now. likewise yes I'm aware that some of the variables are useless because of it
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
                temp_months.f_m = temp_months[0]
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


def test1(cc, ll):
    test_dict = [
        {'acronym': 'null', 'acronym2': 'null', 'ordinal': 'null', 'year': 'null', 'from': 'null', 'to': 'null',
         'country': 'null', 'region': 'null', 'city': 'null', 'gnd': 'null', 'dblp': 'null', 'wikicfpID': 'null',
         'or': 'null', 'wikidata': 'null', 'seriesAcronym': 'null', 'title': 'null'}]
    # print(tabulate(test_dict3, headers="keys"))

    # cc.printSqlQueryResultTest("SELECT * FROM event_dblp WHERE eventId LIKE '%HPCC%'") Bicob
    res = cc.SqlQueryResultTest("SELECT * FROM event_dblp WHERE eventId LIKE '%HPCC%'")

    nlp = spacy.load("en_core_web_trf")  # initialize spacy _trf is the core intended for accuracy

    for index in range(len(res)):
        # TODO figure out a way so that ordinals are assigned to the correct event if more than one are in the title
        #  Note: this somewhat works now but we have to deduct trust score for details like that when multiple events
        #  are in a title

        doc = nlp(res[index]['title'])
        foundEntities = [{"Text": entity.text, "Entity Tag": entity.label_} for entity in doc.ents]

        # print(tabulate(foundEntities, headers="keys"))
        # print('next')
        # print(res[index]['series'])
        acronym = res[index]['series']
        ordinal = find_ordinal(foundEntities, res, index)
        year = res[index]['year']
        date = get_from_to(foundEntities, res, index, nlp)

        # print(ll.lookup(res[index]['location']))
        # print(ll.lookup(res[index]['title']))

        # this it utter rubbish as we rely on location lookup which is completely useless sometimes.
        # like Exeter, United Kingdom returns Exeter (US-NH(New Hampshire) - US(United States of America)) so we
        # decently need a trust score for individual entries that we can lower if we had to guess
        location = location_finder(ll, res, index)
        city = location.city
        region = location.region
        country = location.country

        dblp = res[index]['eventId']
        title = res[index]['title']

        test_dict = test_dict + [{'acronym': acronym + '-' + str(year), 'acronym2': acronym + '-' + str(ordinal),
                                  'ordinal': str(ordinal), 'year': year, 'seriesAcronym': acronym,
                                  'from': str("{:02d}".format(int(date.f_d))) + '.' + str(
                                      "{:02d}".format(int(date.f_m))) + '.' + str("{:02d}".format(int(date.f_y))),
                                  'to': str("{:02d}".format(int(date.t_d))) + '.' + str(
                                      "{:02d}".format(int(date.t_m))) + '.' + str("{:02d}".format(int(date.t_y))),
                                  'dblp': dblp, 'title': title, 'city': city, 'region': region, 'country': country}]

    print(tabulate(test_dict, headers="keys"))

    # location test
    print(ll.lookup('Bielefeld'))
    print(ll.lookup('Köln'))
    print(ll.lookup('abcd, Cologne'))  # if we have OSMPythonTools 0.3.3 or later this will fail because caching
    # changed and conferenceCorpus has not been patched as of writing


# probably not needed anymore
def location_check(ll, res, index):
    is_same = False
    result = ''
    # print('-')
    # print(type(ll.lookup(res[index]['location'])))
    # print(ll.lookup(res[index]['location']))
    # print(ll.lookup(res[index]['title']))
    # print(ll.lookup(res[index]['title']))
    # print(ll.lookup(res[index]['title'])._region)
    # print(ll.lookup(res[index]['title'])._country)

    if type(ll.lookup(res[index]['location'])) == type(ll.lookup(res[index]['title'])):
        if ll.lookup(res[index]['location']).distance(ll.lookup(res[index]['title'])) == 0:
            # print(ll.lookup(res[index]['location']).distance(ll.lookup(res[index]['title'])))
            is_same = True
            result = ll.lookup(res[index]['location'])
        else:
            result = ll.lookup(res[index]['title'])
    else:
        result = ll.lookup(res[index]['title'])
    # print(is_same)
    return result


# serves no real purpose right now but should be checking the column entries (if there) against the title  and return
# the final columns
def locache2(ll, res, index, nlp):
    doc = nlp(res[index]['title'])
    foundEntities = [{"Text": entity.text, "Entity Tag": entity.label_} for entity in doc.ents]
    location_list = []
    print(tabulate(foundEntities, headers="keys"))
    for i in range(len(foundEntities)):
        if 'GPE' in foundEntities[i]['Entity Tag']:
            location_list.append(foundEntities[i]['Text'])

    print(location_list)
    if not location_list:
        print('empty')
    else:
        is_same = False
        result = ''

        for x in range(len(location_list)):
            print('-')
            print(type(ll.lookup(res[index]['location'])))
            print(ll.lookup(res[index]['location']))
            print(ll.lookup(location_list[x]))
            print(ll.lookup(res[index]['title']))
            if type(ll.lookup(res[index]['location'])) == type(ll.lookup(location_list[x])):
                if ll.lookup(res[index]['location']).distance(ll.lookup(location_list[x])) == 0:
                    is_same = True
                    result = ll.lookup(res[index]['location'])
                print(ll.lookup(res[index]['location']).distance(ll.lookup(location_list[x])))

            if (ll.lookup(res[index]['location'])) == (ll.lookup(location_list[x])):
                print(True)
        print(is_same)
        if not is_same:
            is_same = False


# Maybe I'll finish this maybe not don't try to understand what I did here
def matching_title_w_acronym(title: str, acronym: str):
    words_of_title = []
    possible_acronyms = []
    for word in title.split():
        words_of_title.append(word)

    word_acr = ''
    for x in range(len(words_of_title)):
        word_acr = word_acr + words_of_title[x][0]
    possible_acronyms.append(word_acr)
    for x in range(len(words_of_title)):
        word_acr = word_acr + words_of_title[x][0]
        word_acr = word_acr + words_of_title[x][1]
    possible_acronyms.append(word_acr)

    for z in range(len(possible_acronyms)):
        counter = 0
        limit = len(possible_acronyms[z][0])
        y = 0
        while counter < limit:
            if acronym[y] == possible_acronyms[z][counter]:
                y = y + 1
            counter = counter + 1
            if y == len(acronym):
                return True
    return False
