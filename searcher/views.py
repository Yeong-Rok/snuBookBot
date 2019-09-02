from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Result, Response
import json
import requests
from bs4 import BeautifulSoup
import time

def index(request):
    return render(request, 'searcher/index.html')

def room1(request):
     return render(request, 'searcher/01.html')

def room6(request):
     return render(request, 'searcher/06.html')

url = 'https://primoapac01.hosted.exlibrisgroup.com/primo_library/libweb/action/search.do?ct=facet&fctN=facet_library&fctV=MAIN&rfnGrp=1&rfnGrpCounter=1&frbg=&vl(19022558UI4)=books&&indx=1&fn=search&dscnt=0&vl(1UIStartWith0)=contains&tb=t&mode=Advanced&vid=82SNU&ct=search&vl(D15540194UI3)=all_items&vl(19016099UI0)='
others = '&vl(15540188UI0)=AND&srt=rank&tab=all&Submit=검색&vl(19016102UI5)=all_items&dum=true&vl(freeText0)='

def searchTitle(target):
    return requests.get(url + 'title' + others + target)

def searchCreator(target):
    return requests.get(url + 'creator' + others + target)

@csrf_exempt
def search(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        req_user_id = req["userRequest"]["user"]["id"]
        req_title = req["action"]["detailParams"]["title"]["value"]
        Result.objects.create(user_id = req_user_id, req_title = req_title)
        res = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": '검색 중입니다...'
                            }
                        },
                        {
                            "simpleText": {
                                "text": "'" + req_title +  "'에 대한 검색을 완료했습니다. 결과를 확인하시려면 '결과 보기'를 눌러주세요."
                            }
                        }
                    ],
                    "quickReplies": [
                        {
                            "label": "결과 보기",
                            "action": "message",
                            "messageText": "결과 보기"
                        }
                    ]
                }
            }
        return JsonResponse(res)

@csrf_exempt
def result(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        req_user_id = req["userRequest"]["user"]["id"]
        res_title = Response.objects.filter(user_id = req_user_id).last().res_title
        res = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": res_title
                            }
                        }
                    ]
                }
            }
        return JsonResponse(res)


@csrf_exempt
def getPosition(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        reqCallNumber = req["action"]["detailParams"]["callNumber"]["value"]
        print(reqCallNumber)
        response = requests.get('http://147.46.181.235/Mobile/BOOK/book_location_info.php?call_num=' + reqCallNumber)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        room = soup.select('#main_info > #cont_tit > .txtLayer')[0].text
        bookshelf, callNumber = soup.select('#main_info > #info_location_txt > .txtInfo')[0].text.split('청구기호 : ')
        print(room, bookshelf, callNumber)
        answer = "찾으시는 책은 " + room + "의 " + bookshelf + "에 있습니다."
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": answer
                        }
                    }
                ]
            }
        }
        return JsonResponse(res)
