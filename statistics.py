import requests
from bs4 import BeautifulSoup
import pandas as pd

response=requests.get("https://www.soccerstats.com/results.asp?league=poland_2019&pmtype=bydate")
soup=BeautifulSoup(response.text, 'html.parser')
#table
table=soup.find("table", id="btable")
#rows
rows = table.find_all('tr', class_="odd")

data = []
groups = []
i=-1
#data scraping
for row in rows:
    cols = row.find_all('td')
    cols = [elem.text.strip() for elem in cols]
    line = [elem for elem in cols if elem]

    i+=1
    date= line[0]
    teams= line[1]
    score= line[2]
    ht= line[3]
    team1, team2 = teams.split(" - ")
    score1, score2 = score.split(" - ")
    #creating and sorting teams list
    if len(groups)==16:
        groups.sort()
        pass
    elif team1 in groups: pass
    else: groups.append(team1)
    data.append([date, str(team1), str(team2), score1, score2])

data.reverse()
df = pd.DataFrame(data, columns=['Date', 'Team1', 'Team2', 'Score1', 'Score2'])

########################################################################################################

def punkty_h(index):
    rw = int(df['Score1'][index]) - int(df['Score2'][index])  # rw /diff-roznica
    if rw == 0: pkt = 1
    elif rw > 0: pkt = 3
    elif rw < 0: pkt = 0
    return pkt
def punkty_a(index):
    rw = int(df['Score2'][index]) - int(df['Score1'][index])  # rw /diff-roznica
    if rw == 0: pkt = 1
    elif rw > 0: pkt = 3
    elif rw < 0: pkt = 0
    return pkt
def bts_h(index):
    if int(df['Score1'][index])!=0 and int(df['Score2'][index])!=0: pkt = 1
    else: pkt = 0
    return pkt
def bts_a(index):
    if int(df['Score2'][index])!=0 and int(df['Score1'][index])!=0: pkt = 1
    else: pkt = 0
    return pkt



# obecna seria
dic_bts_current_h={}
dic_bts_current_a={}
dic_bts_current_b={}
dic_bts_current_h_l5={}
dic_bts_current_a_l5={}
dic_bts_current_b_l5={}

dic_home={}
dic_away={}
dic_both={}
dic_home_l5={}
dic_away_l5={}
dic_both_l5={}
#########


# data from home matches
for team_home_groups in groups:  #groups - tablica z zespołami, dla poszczególnych zespołów z tablicy, wykonaj
# collecting indexes of team
    tab_team_home_index = [pos for pos, team_name in enumerate(df['Team1']) if team_name == team_home_groups]     #zebranie dla danego zespołu "numerów" spotkań
    s_bts=0
    s_nbts=0
    s_bts_max=0
    s_nbts_max=0
    prev_index=0
# creating and clearing
    temp_pkt_h = []
    temp_goal_s_h = []
    temp_goal_c_h = []
    temp_bts_h = []
# data adding
    for index in tab_team_home_index:
        temp_pkt_h.append(punkty_h(index))
        temp_goal_s_h.append(int(df['Score1'][index]))
        temp_goal_c_h.append(int(df['Score2'][index]))
        temp_bts_h.append(int(bts_h(index)))

# both team to score series
        if bts_h(index)==1:
            s_bts+=1
            if prev_index==0:
                if s_nbts>=s_nbts_max:
                    s_nbts_max=s_nbts
                    s_nbts=0
                s_nbts = 0
        elif bts_h(index)==0:
            s_nbts+=1
            if prev_index==1:
                if s_bts>=s_bts_max:
                    s_bts_max=s_bts
                    s_bts = 0
                s_bts = 0
        prev_index=bts_h(index)

# last both teams to score series
    if s_bts==0:
        bts_current_h={"-": s_nbts}
    else: bts_current_h={"+": s_bts}
#
    dic_home.update({team_home_groups: [sum(temp_pkt_h), sum(temp_goal_s_h), sum(temp_goal_c_h), sum(temp_bts_h),
                round((int(sum(temp_bts_h))/int(len(tab_team_home_index)))* 100, 2), s_bts_max, s_nbts_max, bts_current_h]})

# data from away matches
for team_away_groups in groups:  # Arizona / tablica ze wszystkimi zespołami
    tab_team_away_index = [pos for pos, team_name in enumerate(df['Team2']) if team_name == team_away_groups]
    s_bts=0
    s_nbts=0
    s_bts_max=0
    s_nbts_max=0
    prev_index=0
# creating and clearing
    temp_pkt_a = []
    temp_goal_s_a = []
    temp_goal_c_a = []
    temp_bts_a = []
# data adding
    for index in tab_team_away_index:
        temp_pkt_a.append(punkty_a(index))
        temp_goal_s_a.append(int(df['Score2'][index]))
        temp_goal_c_a.append(int(df['Score1'][index]))
        temp_bts_a.append(int(bts_a(index)))

        if bts_a(index)==1:
            s_bts+=1
            if prev_index==0:
                if s_nbts>=s_nbts_max:
                    s_nbts_max=s_nbts
                    s_nbts=0
                s_nbts = 0
        elif bts_a(index)==0:
            s_nbts+=1
            if prev_index==1:
                if s_bts>=s_bts_max:
                    s_bts_max=s_bts
                    s_bts = 0
                s_bts = 0
        prev_index=bts_a(index)

# current both teams to score series
    if s_bts==0:
        bts_current_a={"-": s_nbts}
    else: bts_current_a={"+": s_bts}
    #
    dic_away.update({team_away_groups: [sum(temp_pkt_a), sum(temp_goal_s_a), sum(temp_goal_c_a), sum(temp_bts_a),
                round((int(sum(temp_bts_a))/int(len(tab_team_away_index)))* 100, 2), s_bts_max, s_nbts_max, bts_current_a]})

# data from last 5 home matches
for team_home_groups in groups:
# collecting indexes of team
    tab_team_home_index = [pos for pos, team_name in enumerate(df['Team1']) if team_name == team_home_groups]
    s_bts=0
    s_nbts=0
    s_bts_max=0
    s_nbts_max=0
    prev_index=0
# creating and clearing
    temp_pkt_h_l5 = []
    temp_goal_s_h_l5 = []
    temp_goal_c_h_l5 = []
    temp_bts_h_l5 = []
# data adding
    for index in tab_team_home_index[-5:]:
        # points
        temp_pkt_h_l5.append(punkty_h(index))
        # goals
        temp_goal_s_h_l5.append(int(df['Score1'][index]))
        temp_goal_c_h_l5.append(int(df['Score2'][index]))
        # both teams to score
        temp_bts_h_l5.append(int(bts_h(index)))

        if bts_h(index)==1:
            s_bts+=1
            if s_bts > s_bts_max:
                s_bts_max = s_bts
            if prev_index==0:
                if s_nbts>=s_nbts_max:
                    s_nbts_max=s_nbts
                    s_nbts=0
                s_nbts = 0
        elif bts_h(index)==0:
            s_nbts+=1
            if s_nbts > s_nbts_max:
                s_nbts_max = s_nbts
            if prev_index==1:
                if s_bts>=s_bts_max:
                    s_bts_max=s_bts
                    s_bts = 0
                s_bts = 0
        prev_index=bts_h(index)

# current both teams to score series
    if s_bts==0:
        bts_current_h={"-": s_nbts}
    else: bts_current_h={"+": s_bts}
    #
    dic_home_l5.update({team_home_groups: [sum(temp_pkt_h_l5), sum(temp_goal_s_h_l5), sum(temp_goal_c_h_l5), sum(temp_bts_h_l5),
                round((int(sum(temp_bts_h_l5))/5)* 100, 2), s_bts_max, s_nbts_max, bts_current_h]})

# data from last 5 away matches
for team_away_groups in groups:
# collecting indexes of team
    tab_team_away_index = [pos for pos, team_name in enumerate(df['Team2']) if team_name == team_away_groups]
    s_bts=0
    s_nbts=0
    s_bts_max=0
    s_nbts_max=0
    prev_index=0
# creating and clearing
    temp_pkt_a_l5 = []
    temp_goal_s_a_l5 = []
    temp_goal_c_a_l5 = []
    temp_bts_a_l5 = []
# data adding
    for index in tab_team_away_index[-5:]:
        # points
        temp_pkt_a_l5.append(punkty_a(index))
        # goals
        temp_goal_s_a_l5.append(int(df['Score2'][index]))
        temp_goal_c_a_l5.append(int(df['Score1'][index]))
        # both teams to score
        temp_bts_a_l5.append(int(bts_a(index)))
        if bts_a(index)==1:
            s_bts+=1
            if s_bts > s_bts_max:
                s_bts_max = s_bts
            if prev_index==0:
                if s_nbts>=s_nbts_max:
                    s_nbts_max=s_nbts
                    s_nbts=0
                s_nbts = 0
        elif bts_a(index)==0:
            s_nbts+=1
            if s_nbts > s_nbts_max:
                s_nbts_max = s_nbts
            if prev_index==1:
                if s_bts>=s_bts_max:
                    s_bts_max=s_bts
                    s_bts = 0
                s_bts = 0
        prev_index=bts_a(index)

# current both teams to score series
    if s_bts==0:
        bts_current_a={"-": s_nbts}
    else: bts_current_a={"+": s_bts}
    #
    dic_away_l5.update({team_away_groups: [sum(temp_pkt_a_l5), sum(temp_goal_s_a_l5), sum(temp_goal_c_a_l5), sum(temp_bts_a_l5),
                round((int(sum(temp_bts_a_l5))/5)* 100, 2), s_bts_max, s_nbts_max, bts_current_a]})


# data from home and away (both) matches
for team_groups in groups:
# collecting indexes of team
    tab_team_home_index = [pos for pos, team_name in enumerate(df['Team1']) if team_name == team_groups]
    tab_team_away_index = [pos for pos, team_name in enumerate(df['Team2']) if team_name == team_groups]
    tab_team_index = tab_team_home_index + tab_team_away_index
    tab_team_index.sort()
    s_bts=0
    s_nbts=0
    s_bts_max=0
    s_nbts_max=0
    prev_index=0
# creating and clearing
    temp_pkt_b = []
    temp_goal_s_b = []
    temp_goal_c_b = []
    temp_bts_b = []
# data adding
    for index in tab_team_index:
        #together
        if df['Team1'][index]==team_groups:
            bts_b=int(bts_h(index))
            team1=int(df['Score1'][index])
            team2=int(df['Score2'][index])
            punkty=punkty_h(index)
        elif df['Team2'][index]==team_groups:
            bts_b=int(bts_a(index))
            team2=int(df['Score1'][index])
            team1=int(df['Score2'][index])
            punkty=punkty_a(index)
        # points
        temp_pkt_b.append(punkty)
        # goals
        temp_goal_s_b.append(team1)
        temp_goal_c_b.append(team2)
        # both team to score series
        temp_bts_b.append(bts_b)
        if bts_b==1:
            s_bts+=1
            if s_bts > s_bts_max:
                s_bts_max = s_bts
            if prev_index==0:
                if s_nbts>=s_nbts_max:
                    s_nbts_max=s_nbts
                    s_nbts=0
                s_nbts = 0
        elif bts_b==0:
            s_nbts+=1
            if s_nbts > s_nbts_max:
                s_nbts_max = s_nbts
            if prev_index==1:
                if s_bts>=s_bts_max:
                    s_bts_max=s_bts
                    s_bts = 0
                s_bts = 0
        prev_index=bts_b

    # current both teams to score series
    if s_bts==0:
        bts_current_b={"-": s_nbts}
    else: bts_current_b={"+": s_bts}
    #
    dic_both.update({team_groups: [sum(temp_pkt_b), sum(temp_goal_s_b), sum(temp_goal_c_b), sum(temp_bts_b),
                round((int(sum(temp_bts_b))/int(len(tab_team_index)))* 100, 2), s_bts_max, s_nbts_max, bts_current_b]})


# data from last 5 home and away (both) matches
for team_groups in groups:
# collecting indexes of team
    tab_team_home_index = [pos for pos, team_name in enumerate(df['Team1']) if team_name == team_groups]
    tab_team_away_index = [pos for pos, team_name in enumerate(df['Team2']) if team_name == team_groups]
    tab_team_index = tab_team_home_index + tab_team_away_index
    tab_team_index.sort()
    s_bts=0
    s_nbts=0
    s_bts_max=0
    s_nbts_max=0
    prev_index=0
# creating and clearing
    temp_pkt_b_l5 = []
    temp_goal_s_b_l5 = []
    temp_goal_c_b_l5 = []
    temp_bts_b_l5 = []
# data adding
    for index in tab_team_index[-5:]:
        # points
        if df['Team1'][index] == team_groups:
            bts_b_l5 = int(bts_h(index))
            team1 = int(df['Score1'][index])
            team2 = int(df['Score2'][index])
            punkty = punkty_h(index)
        elif df['Team2'][index] == team_groups:
            bts_b_l5 = int(bts_a(index))
            team2 = int(df['Score1'][index])
            team1 = int(df['Score2'][index])
            punkty = punkty_a(index)
        temp_pkt_b_l5.append(punkty)
        # goals
        temp_goal_s_b_l5.append(team1)
        temp_goal_c_b_l5.append(team2)
        # both teams to score
        temp_bts_b_l5.append(bts_b_l5)
        if bts_b_l5 == 1:
            s_bts += 1
            if s_bts > s_bts_max:
                s_bts_max = s_bts
            if prev_index == 0:
                if s_nbts >= s_nbts_max:
                    s_nbts_max = s_nbts
                    s_nbts = 0
                s_nbts = 0
        elif bts_b_l5 == 0:
            s_nbts += 1
            if s_nbts > s_nbts_max:
                s_nbts_max = s_nbts
            if prev_index == 1:
                if s_bts >= s_bts_max:
                    s_bts_max = s_bts
                    s_bts = 0
                s_bts = 0
        prev_index = bts_b_l5

    # current both teams to score series
    if s_bts == 0:
        bts_current = {"-": s_nbts}
    else:
        bts_current = {"+": s_bts}
    #
    dic_both_l5.update({team_groups: [sum(temp_pkt_b_l5), sum(temp_goal_s_b_l5), sum(temp_goal_c_b_l5), sum(temp_bts_b_l5),
                round((int(sum(temp_bts_b_l5))/5)* 100, 2), s_bts_max, s_nbts_max, bts_current]})


ex=(["pkt", "goal_s", "goal_c", "bts", "p_bts", "s_bts", "s_nbts", "l_bts", "_b", "_h", "_a"],["number of points", "goals scored", "goals conceded", "'both team to score'",
    "% of 'both team to score'", "maximum series of 'both team to score'", "maximum series of 'not both team to score'", "current 'both team to score' series",
    "statistics for home+away", "statistics for home", "statistics for away"])
exx=pd.DataFrame(ex, index=["shortcut", "explanation"]).T
print(exx, "\n")



headers=["pkt", "goal_s", "goal_c", "bts", "p_bts", "s_bts", "s_nbts", "l_bts"]
df_dic_both=pd.DataFrame(dic_both, index=headers).T
df_dic_home=pd.DataFrame(dic_home, index=headers).T
df_dic_away=pd.DataFrame(dic_away, index=headers).T
df_dic_both_l5=pd.DataFrame(dic_both_l5, index=headers).T
df_dic_home_l5=pd.DataFrame(dic_home_l5, index=headers).T
df_dic_away_l5=pd.DataFrame(dic_away_l5, index=headers).T

print("table: home+away", "\n", df_dic_both, "\n")
print("table: home", "\n", df_dic_home, "\n")
print("table: away", "\n", df_dic_away, "\n")
print("table: home+away_l5", "\n", df_dic_both_l5, "\n")
print("table: home_l5", "\n", df_dic_home_l5, "\n")
print("table: away_l5", "\n", df_dic_away_l5, "\n")


table={}
table_bts={}
for x in groups:
    table.update({x: [df_dic_both.loc[x]["pkt"], str(df_dic_both.loc[x]["goal_s"])+":"+str(df_dic_both.loc[x]["goal_c"]), df_dic_home.loc[x]["pkt"], str(df_dic_home.loc[x]["goal_s"])+":"+str(df_dic_home.loc[x]["goal_c"]),
          df_dic_away.loc[x]["pkt"],str(df_dic_away.loc[x]["goal_s"])+":"+str(df_dic_away.loc[x]["goal_c"])]})
df=pd.DataFrame(table, index=["pkt_b", "goals_b", "pkt_h", "goals_h","pkt_a", "goals_a"]).T
print("table: point & goals")
print(df, "\n")

for x in groups:
    table_bts.update({x: [str(df_dic_both.loc[x]["bts"]), str(round(df_dic_both.loc[x]["p_bts"], 3)), str(df_dic_home.loc[x]["bts"]),
            str(round(df_dic_home.loc[x]["p_bts"], 3)), str(df_dic_away.loc[x]["bts"]), str(round(df_dic_away.loc[x]["p_bts"], 3))]})
df=pd.DataFrame(table_bts, index=["bts_b", "p_bts_b","bts_h", "p_bts_h","bts_a", "p_bts_a"]).T
print("table: both team to score")
print(df)




