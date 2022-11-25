import copy
import requests
from bs4 import BeautifulSoup
from csv import DictWriter

headers = {'user-agent': 'Mozilla/5.0 (X11; Linux; rv:2.0.1) Gecko/20100101 Firefox/4.0.1 Midori/0.4'}

#urlLocal = "urlLocal.html"
#html = BeautifulSoup(Path(urlLocal).read_text(encoding="utf-8"), 'html.parser')
year = "2018"
url = "https://soccer365.ru/competitions/18/"
response = requests.get(url)
html = BeautifulSoup(response.text, 'html.parser')

dataPlayers = {"team": dict(), "player": dict(), "role": dict(), "goals": dict(),
               "penalties": dict(), "passes": dict(), "matches": dict(),
               "isPenalty": dict(), "fairPlay": dict(), "yellowCard": dict(),
               "twoYellowCard": dict(), "redCard": dict()}

mainTable = html.find("table", attrs={"class": "stngs"})

tables = html.find_all("table", attrs={"class": "comp_table_v2"})

trs0 = tables[0].find("tbody").find_all("tr")
# print(trs)

for tr in trs0:
    srcTeam = tr.find("img")["src"]
    team = mainTable.find("img", attrs={"src": srcTeam}).next.a.text
    player = tr.td.div.span.a.text
    role = "бомбардир"

    isPlayerInAssists = tables[1].find("a", string=player)

    if isPlayerInAssists is not None:
        role += ", ассистент"
        passes = int(isPlayerInAssists.parent.parent.parent.parent.find("td", attrs={"class": "bkcenter"}).b.text)
        isPlayerInAssists.parent.parent.parent.parent.decompose()
    else:
        passes = 0

    tds = tr.find_all("td", attrs={"class": "bkcenter"})
    goals = int(tds[0].b.text)
    textPenalties = tds[1].text
    matches = int(tds[2].text)

    if not textPenalties.isspace():
        penalties = int(textPenalties)
    else:
        penalties = 0

    isPlayerInPenalties = tables[2].find("a", string=player)

    if isPlayerInPenalties is not None:
        tdsPenalties = isPlayerInPenalties.parent.parent.parent.parent.find_all("td", attrs={"class": "bkcenter"})
        isPenalty = True

        if not tdsPenalties[0].b.text.isspace():
            fairPlay = int(tdsPenalties[0].b.text)
        else:
            fairPlay = 0

        if not tdsPenalties[1].text.isspace():
            yellowCard = int(tdsPenalties[1].text)
        else:
            yellowCard = 0

        if not tdsPenalties[2].text.isspace():
            twoYellowCard = int(tdsPenalties[2].text)
        else:
            twoYellowCard = 0

        if not tdsPenalties[3].text.isspace():
            redCard = int(tdsPenalties[3].text)
        else:
            redCard = 0
        isPlayerInPenalties.parent.parent.parent.parent.decompose()
    else:
        isPenalty = False
        fairPlay = 0
        yellowCard = 0
        twoYellowCard = 0
        redCard = 0
    dataPlayers["team"][len(dataPlayers["team"])] = team
    dataPlayers["player"][len(dataPlayers["player"])] = player
    dataPlayers["role"][len(dataPlayers["role"])] = role
    dataPlayers["goals"][len(dataPlayers["goals"])] = goals
    dataPlayers["penalties"][len(dataPlayers["penalties"])] = penalties
    dataPlayers["passes"][len(dataPlayers["passes"])] = passes
    dataPlayers["matches"][len(dataPlayers["matches"])] = matches
    dataPlayers["isPenalty"][len(dataPlayers["isPenalty"])] = isPenalty
    dataPlayers["fairPlay"][len(dataPlayers["fairPlay"])] = fairPlay
    dataPlayers["yellowCard"][len(dataPlayers["yellowCard"])] = yellowCard
    dataPlayers["twoYellowCard"][len(dataPlayers["twoYellowCard"])] = twoYellowCard
    dataPlayers["redCard"][len(dataPlayers["redCard"])] = redCard

trs1 = tables[1].find("tbody").find_all("tr")
for tr in trs1:
    srcTeam = tr.find("img")["src"]
    team = mainTable.find("img", attrs={"src": srcTeam}).next.a.text
    player = tr.td.div.span.a.text
    role = "ассистент"
    tdsAssists = tr.find_all("td", attrs={"class": "bkcenter"})
    passes = int(tdsAssists[0].b.text)
    matches = int(tdsAssists[1].text)

    isPlayerInPenalties = tables[2].find("a", string=player)

    if isPlayerInPenalties is not None:
        tdsPenalties = isPlayerInPenalties.parent.parent.parent.parent.find_all("td", attrs={"class": "bkcenter"})
        isPenalty = True

        if not tdsPenalties[0].b.text.isspace():
            fairPlay = int(tdsPenalties[0].b.text)
        else:
            fairPlay = 0

        if not tdsPenalties[1].text.isspace():
            yellowCard = int(tdsPenalties[1].text)
        else:
            yellowCard = 0

        if not tdsPenalties[2].text.isspace():
            twoYellowCard = int(tdsPenalties[2].text)
        else:
            twoYellowCard = 0

        if not tdsPenalties[3].text.isspace():
            redCard = int(tdsPenalties[3].text)
        else:
            redCard = 0
        isPlayerInPenalties.parent.parent.parent.parent.decompose()
    else:
        isPenalty = False
        fairPlay = 0
        yellowCard = 0
        twoYellowCard = 0
        redCard = 0
    dataPlayers["team"][len(dataPlayers["team"])] = team
    dataPlayers["player"][len(dataPlayers["player"])] = player
    dataPlayers["role"][len(dataPlayers["role"])] = role
    dataPlayers["goals"][len(dataPlayers["goals"])] = 0
    dataPlayers["penalties"][len(dataPlayers["penalties"])] = 0
    dataPlayers["passes"][len(dataPlayers["passes"])] = passes
    dataPlayers["matches"][len(dataPlayers["matches"])] = matches
    dataPlayers["isPenalty"][len(dataPlayers["isPenalty"])] = isPenalty
    dataPlayers["fairPlay"][len(dataPlayers["fairPlay"])] = fairPlay
    dataPlayers["yellowCard"][len(dataPlayers["yellowCard"])] = yellowCard
    dataPlayers["twoYellowCard"][len(dataPlayers["twoYellowCard"])] = twoYellowCard
    dataPlayers["redCard"][len(dataPlayers["redCard"])] = redCard

trs2 = tables[2].find("tbody").find_all("tr")
for tr in trs2:
    srcTeam = tr.find("img")["src"]
    team = mainTable.find("img", attrs={"src": srcTeam}).next.a.text
    player = tr.td.div.span.a.text
    role = "не определено"

    tdsPenalties = tr.find_all("td", attrs={"class": "bkcenter"})
    if not tdsPenalties[4].text.isspace():
        matches = int(tdsPenalties[4].text)
    else:
        matches = 0
    isPenalty = True

    if not tdsPenalties[0].b.text.isspace():
        fairPlay = int(tdsPenalties[0].b.text)
    else:
        fairPlay = 0

    if not tdsPenalties[1].text.isspace():
        yellowCard = int(tdsPenalties[1].text)
    else:
        yellowCard = 0

    if not tdsPenalties[2].text.isspace():
        twoYellowCard = int(tdsPenalties[2].text)
    else:
        twoYellowCard = 0

    if not tdsPenalties[3].text.isspace():
        redCard = int(tdsPenalties[3].text)
    else:
        redCard = 0
    dataPlayers["team"][len(dataPlayers["team"])] = team
    dataPlayers["player"][len(dataPlayers["player"])] = player
    dataPlayers["role"][len(dataPlayers["role"])] = role
    dataPlayers["goals"][len(dataPlayers["goals"])] = 0
    dataPlayers["penalties"][len(dataPlayers["penalties"])] = 0
    dataPlayers["passes"][len(dataPlayers["passes"])] = 0
    dataPlayers["matches"][len(dataPlayers["matches"])] = matches
    dataPlayers["isPenalty"][len(dataPlayers["isPenalty"])] = isPenalty
    dataPlayers["fairPlay"][len(dataPlayers["fairPlay"])] = fairPlay
    dataPlayers["yellowCard"][len(dataPlayers["yellowCard"])] = yellowCard
    dataPlayers["twoYellowCard"][len(dataPlayers["twoYellowCard"])] = twoYellowCard
    dataPlayers["redCard"][len(dataPlayers["redCard"])] = redCard


dataPlayers_copy = copy.deepcopy(dataPlayers)

# print(dataPlayers)

dataTeams = {"team": dict(), "goals": dict(), "yellowCards": dict(),
             "maxMatches": dict(), "penalties": dict(), "points": dict()}

for currentTeam in dataPlayers["team"].items():
    if currentTeam[1] not in dataTeams["team"].values():
        dataTeams["team"][len(dataTeams["team"])] = currentTeam[1]
        dataTeams["goals"][len(dataTeams["goals"])] = dataPlayers["goals"][currentTeam[0]]
        dataTeams["yellowCards"][len(dataTeams["yellowCards"])] = \
            dataPlayers["yellowCard"][currentTeam[0]] + dataPlayers["twoYellowCard"][currentTeam[0]] * 2
        dataTeams["maxMatches"][len(dataTeams["maxMatches"])] = dataPlayers["matches"][currentTeam[0]]
        dataTeams["penalties"][len(dataTeams["penalties"])] = dataPlayers["penalties"][currentTeam[0]]
    else:
        for teamInDataTeamGoals in dataTeams["team"].items():
            if currentTeam[1] == teamInDataTeamGoals[1]:
                dataTeams["goals"][teamInDataTeamGoals[0]] += dataPlayers["goals"][currentTeam[0]]
                dataTeams["yellowCards"][teamInDataTeamGoals[0]] += \
                    dataPlayers["yellowCard"][currentTeam[0]] + dataPlayers["twoYellowCard"][currentTeam[0]] * 2
                if dataTeams["maxMatches"][teamInDataTeamGoals[0]] < dataPlayers["matches"][currentTeam[0]]:
                    dataTeams["maxMatches"][teamInDataTeamGoals[0]] = dataPlayers["matches"][currentTeam[0]]
                dataTeams["penalties"][teamInDataTeamGoals[0]] += dataPlayers["penalties"][currentTeam[0]]
                break
for team in mainTable.find("tbody").find_all("tr"):
    teamName = team.find("a", attrs={"rel": "nofollow"}).text
    teamMatches = int(team.find("td", attrs={"class": "ctr"}).text)
    for dataTeam in dataTeams["team"].items():
        if teamName == dataTeam[1] and dataTeams["maxMatches"][dataTeam[0]] < teamMatches:
            dataTeams["maxMatches"][dataTeam[0]] = teamMatches
            break
mainTrs = mainTable.find("tbody").find_all("tr")
for currentMainTr in mainTrs:
    currentTeam = currentMainTr.find("a").text
    currentPoints = currentMainTr.find("b").text
    for team in dataTeams["team"].items():
        if currentTeam == team[1]:
            dataTeams["points"][len(dataTeams["points"])] = int(currentPoints)

headForTable = ["Команда", "ФИ игрока", "Роль", "Голы", "Пенальти", "Пасы", "Матчи", "Штрафные", "Fairy play", "ЖК", "2ЖК", "КК", "Год"]


with open('players_info.csv', 'a', newline='') as file:
    dict_writter = DictWriter(file, fieldnames=headForTable)
    for team in dataPlayers_copy["team"].items():
        dict_row = {
            "Команда": dataPlayers_copy["team"][team[0]],
            "ФИ игрока": dataPlayers_copy["player"][team[0]],
            "Роль":dataPlayers_copy["role"][team[0]],
            "Голы":dataPlayers_copy["goals"][team[0]],
            "Пенальти":dataPlayers_copy["penalties"][team[0]],
            "Пасы":dataPlayers_copy["passes"][team[0]],
            "Матчи":dataPlayers_copy["matches"][team[0]],
            "Штрафные":dataPlayers_copy["isPenalty"][team[0]],
            "Fairy play":dataPlayers_copy["fairPlay"][team[0]],
            "ЖК":dataPlayers_copy["yellowCard"][team[0]],
            "2ЖК":dataPlayers_copy["twoYellowCard"][team[0]],
            "КК":dataPlayers_copy["redCard"][team[0]],
            "Год": year
        }
        dict_writter.writerow(dict_row)
