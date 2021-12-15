import corpusTools




def Test1():
    # stolen from ConferenceCorpusIntro

    cc = corpusTools.ConferenceCorpusIntro()            # initializes the corpus
    cc.printCacheFile()                               # prints where the cached file is located
    # cc.printAvailableDatasourceIds()                  # does what it says on the tin
    # cc.printEventsOfDatasource(sourceId="wikidata")   # prints the first ten entries of a data source
    # cc.printEventsOfSeries(sourceId="or", seriesAcronym="AAAI", limit=5)   # prints limit amount of entries found in the given source with the given acronym. Note: There has to be an eventAcronym that is matched to an entrie as we query for this. Seems to be only usable with open research
    # cc.printSqlQueryResult()                          # SQL query the Database (the cached file) via SQLite I think
    # cc.printDatasourceStats()                         # does what it says on the tin

    # Test lines

    # cc.printEventsOfSeries(sourceId="wikidata", seriesAcronym="", limit=100)
    cc.printSqlQueryResultTest("SELECT * FROM event_dblp WHERE eventId LIKE '%HPCC%'")
    print('\n')
    cc.printSqlQueryResultTest("SELECT * FROM event_wikidata WHERE acronym LIKE '%HPCC%'")

    # Like does not mean exact match for that we need =
    # % is a wild card an can be 0 or more characters
    # Note that we have to be careful that columns are named different or not existing in other sources
    # For example: dblp acronym column seems useless and the eventId column seems more useful

    # Also to note are eventseries_cdw and _wdc as they contain alternate spellings among other things of the same acronym. However it seems as if this would create more ambiguity
    # They are not mentioned on the wiki tho and I don't know how they were created or how reliable they are.
    # cc.printSqlQueryResultTest("SELECT * FROM eventseries_cdw WHERE (acronym+`acronym:1`+`acronym:2`) LIKE '%AI%'") # I don't know what is wrong with this multi column query
    cc.printSqlQueryResultTest("SELECT * FROM eventseries_cdw WHERE acronym LIKE '%aiia%'")
    cc.printSqlQueryResultTest("SELECT * FROM eventseries_cdw WHERE `acronym:1` LIKE '%aiia%'")
    cc.printSqlQueryResultTest("SELECT * FROM eventseries_cdw WHERE `acronym:2` LIKE '%aiia%'")



    # cc.printSqlQueryResultTest("SELECT * FROM eventseries_wdc WHERE (acronym+`acronym:1`+`acronym:2`) LIKE '%WWW%'")  # I don't know what is wrong with this multi column query
    cc.printSqlQueryResultTest("SELECT * FROM eventseries_wdc WHERE acronym LIKE '%WWW%'")
    cc.printSqlQueryResultTest("SELECT * FROM eventseries_wdc WHERE `acronym:1` LIKE '%WWW%'")
    cc.printSqlQueryResultTest("SELECT * FROM eventseries_wdc WHERE `acronym:2` LIKE '%WWW%'")