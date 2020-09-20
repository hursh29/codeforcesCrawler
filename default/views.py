from django.shortcuts import render,redirect
from django.http import HttpResponse
import requests
import os 
from json import dumps
from default.models import *
import math
from scrape_test import *
userHandle = "masaow"
def default_page(request): 
    global userHandle
    if(request.method == 'POST'):       
        userHandle = request.POST.get('userHandle')  
        return redirect("/userInfo")     
    return render(request,"default_page.htm",{})
tags = {}
verdicts = {} 
    
def userInfo(request): 
    tags.clear()
    verdicts.clear()
    r = (requests.get("https://codeforces.com/api/user.status?handle="+userHandle).json())
    for submission in r['result']:
            for problemTag in submission['problem']['tags']:
                if(submission['verdict'] == 'OK'):
                    if(tags.get(problemTag) == None):
                        tags[problemTag] = 1
                    else:
                        tags[problemTag] +=1

            if(verdicts.get(submission['verdict']) == None):
                verdicts[submission['verdict']] = 1
            else:
                verdicts[submission['verdict']] +=1
 
    responseOfRequests = requests.get("https://codeforces.com/api/user.info?handles="+userHandle).json()
    responseOfRequests = responseOfRequests['result'][0]

    

    return render(request,"userInfo.htm",{
            "firstName"     : responseOfRequests['firstName'],
            "lastName"      : responseOfRequests['lastName'],
            "rating"        : responseOfRequests['rating'],
            "friends"       : responseOfRequests['friendOfCount'],
            "imageUrl"      : responseOfRequests['titlePhoto'],
            "city"          : responseOfRequests['city'],
            "country"       : responseOfRequests['country'],
            "organization"  : responseOfRequests['organization'],
            "rank"          : responseOfRequests['rank'],
            "userHandle"    : userHandle,
            "tags"          : dumps(tags),
            "verdicts"      : dumps(verdicts)
        })

completeUsersDataObject   = {} 
completeUsersRatingObject = {}
def refreshUsers(request):
    global completeUsersDataObject 
    completeUsersDataObject.clear()
    completeUsersRatingObject.clear()
    all_users.objects.all().delete()
    all_usersRating.objects.all().delete()
    url = 'https://codeforces.com/api/user.ratedList'
    completeUsersData = requests.get(url).json()
    completeUsersData = completeUsersData['result'] 
    for element in completeUsersData:
        # print(element)
        # print(element['rank'])
        userRating = element['rating']
        userRating /=100
        userRating = math.floor(userRating)
        if(completeUsersRatingObject.get(userRating) == None):
            completeUsersRatingObject[userRating] = 1
        else:
            completeUsersRatingObject[userRating] += 1
        
        if(completeUsersDataObject.get(element['rank']) == None):
            completeUsersDataObject[element['rank']] = 1
        else:
            completeUsersDataObject[element['rank']] += 1
    
    for x in completeUsersRatingObject:
        obj = all_usersRating(rating= x, ratingCount= completeUsersRatingObject[x])
        obj.save()
     
    for x in completeUsersDataObject:
        obj = all_users(rank =x, rankCount= completeUsersDataObject[x])
        obj.save()
    return redirect("/completeUsers")

def completeUsers(request):
    global completeUsersDataObject
    completeUsersDataObject.clear() 
    myobjectForRank = all_users.objects.all()
    for x in myobjectForRank:
        completeUsersDataObject[x.rank] = x.rankCount
    
    myobjectForRating = all_usersRating.objects.all()
    for x in myobjectForRating:
        completeUsersRatingObject[x.rating] = x.ratingCount

    return render(request,"completeUsers.htm",{
            "completeUsersDataObject": dumps(completeUsersDataObject),
            "completeUsersRatingObject":dumps(completeUsersRatingObject)
            }) 

def refreshContests(request):
    
    Educational.objects.all().delete()
    Global.objects.all().delete()
    Div_1.objects.all().delete()
    Div_2.objects.all().delete()
    Div_3.objects.all().delete()
    Others.objects.all().delete()
    r = requests.get('https://codeforces.com/api/contest.list').json()
    for x in r['result']:
        contestName = x['name']
        contestid   = x['id']
        print('error 😣',f'https://codeforces.com/contest/{contestid}')
        if(contestName.find('Educational') != -1): 
            print('added in Educational $ ', contestid)
            problemlist = count_problems(f'https://codeforces.com/contest/{contestid}')
            obj = Educational(   contestId = contestid,
                            contestName = contestName,
                            problemList = problemlist)
            obj.save()
        elif(contestName.find('(Div. 1)') != -1): 
            print('added in Div 1 $ ', contestid)
            
            problemlist = count_problems(f'https://codeforces.com/contest/{contestid}')
            obj = Div_1(   contestId = contestid,
                            contestName = contestName,
                            problemList = problemlist)
            obj.save()
        elif(contestName.find('(Div. 2)') != -1):
            print('added in Div 2 $ ', contestid)
            problemlist = count_problems(f'https://codeforces.com/contest/{contestid}')
            obj = Div_2(   contestId = contestid,
                            contestName = contestName,
                            problemList = problemlist)
            obj.save() 
        elif(contestName.find('(Div. 3)') != -1):
            print('added in Div 3 $ ', contestid)
            problemlist = count_problems(f'https://codeforces.com/contest/{contestid}')
            obj = Div_3(   contestId = contestid,
                            contestName = contestName,
                            problemList = problemlist)
            obj.save()
        elif(contestName.find('Global') != -1):
            print('added in global $', contestid)
            problemlist = count_problems(f'https://codeforces.com/contest/{contestid}')
            obj = Global(   contestId = contestid,
                            contestName = contestName,
                            problemList = problemlist)
            obj.save()
        else:
            print('added in others $', contestid)
            problemlist = count_problems(f'https://codeforces.com/contest/{contestid}')
            obj = Others(   contestId = contestid,
                            contestName = contestName,
                            problemList = problemlist)
            obj.save()
    return redirect('/contestsInfo')

def contestsInfo(request):
    myobjectForEducationalContests = Educational.objects.all()
    myobjectForDiv_1Contests = Div_1.objects.all()
    myobjectForDiv_2Contests = Div_2.objects.all()
    myobjectForDiv_3Contests = Div_3.objects.all()
    myobjectForGlobalContests = Global.objects.all()
    myobjectForOthersContests = Others.objects.all()
    
    return render(request,"contestsInfo.htm",{
        "myobjectForEducationalContests": myobjectForEducationalContests,
        "myobjectForDiv_1Contests": myobjectForDiv_1Contests,
        "myobjectForDiv_2Contests": myobjectForDiv_2Contests,
        "myobjectForDiv_3Contests": myobjectForDiv_3Contests,
        "myobjectForGlobalContests": myobjectForGlobalContests,
        "myobjectForOthersContests": myobjectForOthersContests
    })