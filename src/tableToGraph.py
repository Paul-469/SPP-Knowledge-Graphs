from tabulate import tabulate

from src import dblpTable


def add_table_to_graph(lod, neo_DB):

    for x in range(1, len(lod)):

        # First we determine if vital Info is present else we don't add to graph

        # 1. ordinal
        if lod[x]['ordinal'] is None:
            continue
        else:
            if str(lod[x]['ordinal']) == "0" or "-" in str(lod[x]['ordinal']) or str(lod[x]['ordinal']) == 'null':
                continue
            else:
                ordinal = lod[x]['ordinal']

        if lod[x]['seriesAcronym'] is None:
            continue
        else:
            if str(lod[x]['seriesAcronym']) == 'null':
                continue
            else:
                series_acronym = lod[x]['seriesAcronym']

        year = 'year missing'
        # We do not require the year but it is helpful
        if not lod[x]['year'] is None:
            if not lod[x]['year'] == 'null':
                if not int(lod[x]['year']) <= 0:
                    year = lod[x]['year']

        # Create a placeholder Title if it is missing
        if lod[x]['title'] is None or lod[x]['title'] == 'null' or lod[x]['title'] == 'ghost':
            title = f"Placeholder: {series_acronym}-{ordinal}, {year}"
        else:
            title = lod[x]['title']

        # if the previous conditions are satisfied we can assume that the acronym exists
        acronym = lod[x]['acronym']
        neo_DB.add_node(title, "Event")
        neo_DB.add_two_nodes(title, "Event", ordinal, "ordinal", "is")
        neo_DB.add_two_nodes(title, "Event", series_acronym, "series", "part_of")
        neo_DB.add_two_nodes(title, "Event", acronym, "event_acronym", "acronym")

        # The acronym is added as a property of the title as well mainly so we don't need to hop from node to node if we
        # trace from a series node.
        # The reason why I think keeping the acronym as it's own node around is for error checking. Since the acronym
        # node is only created if none exists there should only be one reference to the acronym node
        # If there are more we know that we either have fed broken data into the graph or we have a duplicated event
        neo_DB.add_property(title, "Event", "Acronym", acronym)

        # Add the remaining Info if present
        if not lod[x]['year'] is None:
            if not lod[x]['year'] == 'null':
                if not int(lod[x]['year']) <= 0:
                    year = lod[x]['year']
                    neo_DB.add_two_nodes(title, "Event", year, "year", "in")

        if not lod[x]['from'] is None:
            if not lod[x]['from'] == 'null':
                if not str(lod[x]['from']) == '00.00.0000' and not str(lod[x]['from']) == '00.00.00':
                    from_date = lod[x]['from']
                    neo_DB.add_two_nodes(title, "Event", from_date, "from_date", "from")

        if not lod[x]['to'] is None:
            if not lod[x]['to'] == 'null':
                if not str(lod[x]['to']) == '00.00.0000' and not str(lod[x]['to']) == '00.00.00':
                    to_date = lod[x]['to']
                    neo_DB.add_two_nodes(title, "Event", to_date, "to_date", "to")

        if not lod[x]['city'] is None:
            if not lod[x]['city'] == 'null':
                city = lod[x]['city']
                neo_DB.add_two_nodes(title, "Event", city, "city", "in")

        if not lod[x]['region'] is None:
            if not lod[x]['region'] == 'null':
                city = lod[x]['region']
                neo_DB.add_two_nodes(title, "Event", city, "region", "in")

        if not lod[x]['country'] is None:
            if not lod[x]['country'] == 'country':
                city = lod[x]['country']
                neo_DB.add_two_nodes(title, "Event", city, "country", "in")

        # We also add a node with the references
        if "gnd" in lod[x].keys():
            if lod[x]['gnd'] is None or lod[x]['gnd'] == 'null':
                gnd = 'missing'
            else:
                gnd = lod[x]['gnd']
        else:
            gnd = 'missing'

        if "dblp" in lod[x].keys():
            if lod[x]['dblp'] is None or lod[x]['dblp'] == 'null':
                dblp = 'missing'
            else:
                dblp = lod[x]['dblp']
        else:
            dblp = 'missing'

        if "wikicfpID" in lod[x].keys():
            if lod[x]['wikicfpID'] is None or lod[x]['wikicfpID'] == 'null':
                wikicfpID = 'missing'
            else:
                wikicfpID = lod[x]['wikicfpID']
        else:
            wikicfpID = 'missing'

        if "or" in lod[x].keys():
            if lod[x]['or'] is None or lod[x]['or'] == 'null':
                or_id = 'missing'
            else:
                or_id = lod[x]['or']
        else:
            or_id = 'missing'

        if "wikidata" in lod[x].keys():
            if lod[x]['wikidata'] is None or lod[x]['wikidata'] == 'null':
                wikidata = 'missing'
            else:
                wikidata = lod[x]['wikidata']
        else:
            wikidata = 'missing'

        if "confref" in lod[x].keys():
            if lod[x]['confref'] is None or lod[x]['confref'] == 'null':
                confref = 'missing'
            else:
                confref = lod[x]['confref']
        else:
            confref = 'missing'

        node_name = f"References for {acronym}:"
        neo_DB.add_two_nodes(title, "Event", node_name, "References", "referenced_in")
        neo_DB.add_property(node_name, "References", "gnd", gnd)
        if not gnd == 'missing':
            neo_DB.add_two_nodes(node_name, "References", "gnd", "Source", "is_in")
        neo_DB.add_property(node_name, "References", "dblp", dblp)
        if not dblp == 'missing':
            neo_DB.add_two_nodes(node_name, "References", "dblp", "Source", "is_in")
        neo_DB.add_property(node_name, "References", "wikicfpID", wikicfpID)
        if not wikicfpID == 'missing':
            neo_DB.add_two_nodes(node_name, "References", "wikicfpID", "Source", "is_in")
        neo_DB.add_property(node_name, "References", "or", or_id)
        if not or_id == 'missing':
            neo_DB.add_two_nodes(node_name, "References", "or", "Source", "is_in")
        neo_DB.add_property(node_name, "References", "wikidata", wikidata)
        if not wikidata == 'missing':
            neo_DB.add_two_nodes(node_name, "References", "wikidata", "Source", "is_in")
        neo_DB.add_property(node_name, "References", "confref", confref)
        if not confref == 'missing':
            neo_DB.add_two_nodes(node_name, "References", "confref", "Source", "is_in")


        # references = f"gnd: {gnd}; dblp: {dblp}; wikicfpID: {wikicfpID}; or: {or_id}; wikidata: {wikidata}; confref: {confref}"
        # neo_DB.add_two_nodes(title, "Event", references, "References", "referenced_in")

        # I don't know how useful that would be but we could also add a reference from this node to a node for each
        # source if there is a reference in the source


