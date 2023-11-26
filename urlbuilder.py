from itertools import islice
import importlib
import pandas as pd
#import Leage_Teaminfo

#flow -> function: for loop to create URL
#outer loop to main forloop will run n times depending on how many seasons you want.

seasons=[
  '2023-2024/matchlogs',
  '2022-2023/matchlogs'
]
Match_Logs_Type = {
  "Shooting": "shooting",
  "keeping": "keeper",
  "Passing": "passing",
  "pass type": "passing_types",
  "GCA": "gca",
  "Defensive_actions": "defense",
  "Possession": "possession",
  "Miscellaneous Stats": "misc",
}
def is_dictionary(obj):
    return isinstance(obj,dict)
URLList= []
def urlbuilderfunc(seasons, dic_league, logtypes):
    First_Section= 'https://fbref.com/en/squads/'
    Match_Logs= '-Match-Logs-'

    #we want to skip the first 2 lines because we embedded some metadata there (I.E)
    iterator = iter(dic_league.items())

    #loop outer-inner: Seasons, leagues, team, logtype
    #TODO: 11/16/23 figure out way to add the league data but not interate through the loop 
    #for season in seasons:
        #for leagueID, leaguename in leagues.items():
    for team, teamID in islice(iterator, 2, None):
        #skipping first 2 lines of dictionary
        for type in logtypes.values():
#Example url https://fbref.com/en/squads/361ca564/2023-2024/matchlogs/c9/shooting/Tottenham-Hotspur-Match-Logs-Premier-League
#            |      First_Section       |Team ID |   Year & Filler   |L#| M_L_T  | Team_Name      | Filler   | League Name  |
            url= f'{First_Section}{teamID}/2022-2023/matchlogs/{dic_league.get("leagueID")}/{type}/{team}-Match-Logs-{dic_league.get("leagueName")}'
            #print(url)
            #list function? data function?
            URLList.append(url)



league_dict_module = importlib.import_module('Leage_Teaminfo')
league_dictionary=dict()

for atter_name in dir(league_dict_module):
    attr=getattr(league_dict_module, atter_name)
    if is_dictionary(attr) and not atter_name.startswith('_'):
      league_dictionary[f'{atter_name}'] = attr

#Iterate through each dictionary
for league_dict in league_dictionary:
    league_dict=league_dictionary[league_dict]
    urlbuilderfunc(seasons, league_dict, Match_Logs_Type)

ListDataFrame= pd.DataFrame(URLList)
ListDataFrame.to_csv('Masterlink2022-2023.csv', index=False)