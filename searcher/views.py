from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Title, Author, Response
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

@csrf_exempt
def search(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        req_user_id = req["userRequest"]["user"]["id"]
        if 'title' in req["action"]["detailParams"]:
            req_title = req["action"]["detailParams"]["title"]["value"]
            Title.objects.create(user_id = req_user_id, title = req_title)
        elif 'author' in req["action"]["detailParams"]:
            req_author = req["action"]["detailParams"]["author"]["value"]
            Author.objects.create(user_id = req_user_id, author = req_author)
        else:
            print("실패")

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
                                "text": "검색을 완료했습니다. 결과를 확인하시려면 '결과 보기'를 눌러주세요."
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
        result = Response.objects.filter(user_id = req_user_id).last()
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "carousel": {
                            "type": "basicCard",
                            "items": []
                        }
                    },
                ],
                "quickReplies": [
                    {
                        "label": "다른 책 찾기",
                        "action": "message",
                        "messageText": "다른 책 찾기"
                    },
                    {
                        "label": "처음으로",
                        "action": "message",
                        "messageText": "처음으로"
                    }
                ]
            },
            "context": {

            }
        }

        if (result.title0 is None):
            card = {
                "title": "검색 결과가 없습니다."
            }
            res["template"]["outputs"][0]["carousel"]["items"].append(card)

            return JsonResponse(res)


        if (result.title0 != None):
            card = {
                "title": result.title0,
                "description": result.detail0,
            }
            res["template"]["outputs"][0]["carousel"]["items"].append(card)


        if (result.title1 != None):
            card = {
                "title": result.title1,
                "description": result.detail1,
            }
            res["template"]["outputs"][0]["carousel"]["items"].append(card)

        if (result.title2 != None):
            card = {
                "title": result.title2,
                "description": result.detail2,
            }
            res["template"]["outputs"][0]["carousel"]["items"].append(card)

        if (result.title4 != None):
            card = {
                "title": result.title4,
                "description": result.detail4,
            }
            res["template"]["outputs"][0]["carousel"]["items"].append(card)

        if (result.title5 != None):
            card = {
                "title": result.title5,
                "description": result.detail5,
            }
            res["template"]["outputs"][0]["carousel"]["items"].append(card)

        if (result.title6 != None):
            card = {
                "title": result.title6,
                "description": result.detail6,
            }
            res["template"]["outputs"][0]["carousel"]["items"].append(card)

        if (result.title7 != None):
            card = {
                "title": result.title7,
                "description": result.detail7,
            }
            res["template"]["outputs"][0]["carousel"]["items"].append(card)

        if (result.title8 != None):
            card = {
                "title": result.title8,
                "description": result.detail8,
            }
            res["template"]["outputs"][0]["carousel"]["items"].append(card)

        if (result.title9 != None):
            card = {
                "title": result.title9,
                "description": result.detail9,
            }
            res["template"]["outputs"][0]["carousel"]["items"].append(card)

        if (result.more):
            card = {
                "basicCard": {
                    "title": "더 많은 검색 결과를 확인하려면 아래 버튼을 눌러 중앙도서관 웹사이트를 확인하세요.",
                    "buttons": [
                        {
                            "action": "webLink",
                            "label": "더 보기",
                            "webLinkUrl": result.url
                        }
                    ]
                }
            }
            res["template"]["outputs"].append(card)

        return JsonResponse(res)



url = 'https://primoapac01.hosted.exlibrisgroup.com/primo_library/libweb/action/search.do?ct=facet&fctN=facet_library&fctV=MAIN&rfnGrp=1&rfnGrpCounter=1&frbg=&vl(19022558UI4)=books&&indx=1&fn=search&dscnt=0&vl(1UIStartWith0)=contains&tb=t&mode=Advanced&vid=82SNU&ct=search&vl(D15540194UI3)=all_items&vl(19016099UI0)='
others = '&vl(15540188UI0)=AND&srt=rank&tab=all&Submit=검색&vl(19016102UI5)=all_items&dum=true&vl(freeText0)='

@csrf_exempt
def getPosition(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        reqCallNumber = req["action"]["detailParams"]["callNumber"]["value"]
        response = requests.get('http://147.46.181.235/Mobile/BOOK/book_location_info.php?call_num=' + reqCallNumber)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        room = soup.select('#main_info > #cont_tit > .txtLayer')[0].text
        bookshelf, callNumber = soup.select('#main_info > #info_location_txt > .txtInfo')[0].text.split('청구기호 : ')
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
