'''
Created on 11.3.2013

@author: baydet
'''
import re
import os
N = 20
teams_arr = ['man-utd', 'man-city', 'tottenham', 'chelsea', 'arsenal', 'everton', 'west-brom', 'swansea', 'stoke', 'fulham', 'norwich', 'newcastle', 'west-ham', 'sunderland', 'southampton', 'wigan', 'aston-villa', 'reading', 'qpr', 'liverpool']
lines = []
res_arr = []

def filterData(filename):
    if (os.path.isfile(filename)):
        f = open(filename, 'r')
        report = f.readline()
        for line in lines:
            res = re.findall('[A-Z][^\.;]*' + line + '[^\.;]*', report)
            for n in res:
                res_arr.append(n)
    return

if __name__ == '__main__':
    concepts = open('concepts.txt', 'r');
    for line in concepts.readlines():
        line = line.rstrip()      # Remove trailing whitespace.
        lines.append(line)
    print lines
    
    for i in range(0, N):
        for j in range(0, N):
            filterData('docs/' + teams_arr[i]+'-'+teams_arr[j]+'.txt');
    ff = open('output.txt', 'w+')
    i = 0
    for n in res_arr:
        i += 1
        ff.write(n + '\n')
        
    ff.close()
    print "Well done!"