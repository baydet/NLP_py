# coding: utf-8
'''
Created on 26.2.2013
@author: baydet
'''
import re
import urllib

N = 20
teams_arr = ['man-utd', 'man-city', 'tottenham', 'chelsea', 'arsenal', 'everton', 'west-brom', 'swansea', 'stoke', 'fulham', 'norwich', 'newcastle', 'west-ham', 'sunderland', 'southampton', 'wigan', 'aston-villa', 'reading', 'qpr', 'liverpool']

def build_url(i, j):
#    print 'http://www.premierleague.com/content/premierleague/en-gb/matchday/matches/2012-2013/epl.match-report.html/' + teams_arr[i] + '-vs-' + teams_arr[j]
    return 'http://www.premierleague.com/content/premierleague/en-gb/matchday/matches/2012-2013/epl.match-report.html/' + teams_arr[i] + '-vs-' + teams_arr[j] 

def article_fetch(url):
    f = urllib.urlopen(url)
    text = f.read();
    tt = re.sub(">\s*<","><",text)
    ret_str = re.search(r'<h2>Match report</h2>.*</div><div class=\"nextfixtureslist section\">', tt, re.IGNORECASE)
    if ret_str is None:
        return None
    else:
        artStr = re.sub("&quot|<br>|</b>|<b>|<p>|</p>|<h2>Match report</h2>|</div><div class=\"nextfixtureslist section\">"," ",ret_str.group())
        return artStr

if __name__ == '__main__':
    games_map = N*[N*[0]]# [[0 for x in xrange(N)] for x in xrange(N)]
    for i in range(0, N):
        for j in range(0, N):
            url = build_url(i, j)
            article = article_fetch(url)
            if article != None:
#                print i + ' ' + j
                f = open('docs/' + teams_arr[i]+'-'+teams_arr[j]+'.txt', 'w+')
                f.write(article)
                f.close()            
    print 'Well done!!'
