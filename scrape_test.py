from bs4 import BeautifulSoup
import requests
def count_problems(link):
    source  = requests.get(link).text
    soup = BeautifulSoup(source, 'lxml').body 

    content = (soup.find('table', {'class': 'problems'}))
    if content == None :
        return " ";
    problems = content.findAll('tr') 
    res = ""
    for i in range(len(problems)):
        if i > 0 : 
            problem =  problems[i].td.a.text 
            problem = problem.split(' ')
            # print(problem)
            for j in problem:
                if len(j) and j != '\r\n':
                    j = j.split('\r')
                    res = res + j[0] + " " 
    return res
print(count_problems('https://codeforces.com/contest/1392'))