from Dictionary import Match_Logs_Type as logtypes
from Dictionary import Premier_League_Teams as preleague
from Dictionary import La_Liga_Teams as liga

#flow -> function: for loop to create URL
#outer loop to main forloop will run n times depending on how many seasons you want.

seasons=[
  '2023-2024/matchlogs',
  '2022-2023/matchlogs'
]
leagues = {
    "c9": "Premier-League",
    "c12":"La-Liga"
}

def urlbuilder(seasons, leagues, dic_league, dic_logtype):
    First_Section= 'https://fbref.com/en/squads/'
    Match_Logs= '-Match-Logs-'

    #loop outer-inner: Seasons, leagues, team, logtype
    #TODO: 11/16/23 figure out way to add the league data but not interate through the loop 
    for season in seasons:
        for leagueID, leaguename in leagues.items():
            for team, teamID in dic_league.items():
                for type in dic_logtype.values():
#Example url https://fbref.com/en/squads/361ca564/2023-2024/matchlogs/c9/shooting/Tottenham-Hotspur-Match-Logs-Premier-League
#            |      First_Section       |Team ID |   Year & Filler   |L#| M_L_T  | Team_Name      | Filler   | League Name  |
                    url= f'{First_Section}{teamID}/{season}/{leagueID}/{type}/{team}-Match-Logs-{leaguename}'
                    print(url)
    

urlbuilder(seasons, leagues, preleague, logtypes)