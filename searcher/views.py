from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

import requests
from bs4 import BeautifulSoup
import time

def index(request):
    return render(request, 'searcher/index.html')

def room1(request):
     return render(request, 'searcher/01.html')

def room6(request):
     return render(request, 'searcher/06.html')

#url = 'https://primoapac01.hosted.exlibrisgroup.com/primo-explore/search?query='
#others = ',AND&pfilter=pfilter,exact,books,AND&vid=82SNU&mfacet=library,include,MAIN,1&lang=ko_KR&mode=advanced'
url = 'https://primoapac01.hosted.exlibrisgroup.com/primo_library/libweb/action/search.do?ct=facet&fctN=facet_library&fctV=MAIN&rfnGrp=1&rfnGrpCounter=1&frbg=&vl(19022558UI4)=books&&indx=1&fn=search&dscnt=0&vl(1UIStartWith0)=contains&tb=t&mode=Advanced&vid=82SNU&ct=search&vl(D15540194UI3)=all_items&vl(19016099UI0)='
others = '&vl(15540188UI0)=AND&srt=rank&tab=all&Submit=검색&vl(19016102UI5)=all_items&dum=true&vl(freeText0)='

def make_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome('/usr/bin/chromedriver', options = options)
    return driver

def searchTitle(target):
#def searchTitle(target, driver):
    #driver.get(url + 'title,contains,' + target + others)
    return requests.get(url + 'title' + others + target)
    #return getResults(driver)

def searchCreator(target):
#def searchCreator(target, driver):
    #driver.get(url + 'creator,contains,' + target + others)
    return requests.get(url + 'creator' + others + target)
    #return getResults(driver)

def getResults(driver):
    results = {}
    try:
        elements = WebDriverWait(driver, 3).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".EXLResultTitle "))
        )
        index = 0
        for e in elements:
            index += 1
            results[index] = e.text
        driver.quit()
        print(results)
        return results
    except TimeoutException as ex:
        print("Exception has been thrown. " + str(ex))
    finally:
        driver.quit()


import pycurl
from io import BytesIO
from bs4 import BeautifulSoup
import time

@csrf_exempt
def search(request):
    start = time.time()
    if request.method == 'POST':
        req = json.loads(request.body)
        reqTitle = req["action"]["detailParams"]["title"]["value"]
        
        buffer = BytesIO()

        # Curl 객체 생성
        c = pycurl.Curl()

        #헤더 설정
        c.setopt(pycurl.HTTPHEADER, [
            "User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)\
                    AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
            "Accept:text/html,application/xhtml+xml,application/xml;\
                    q=0.9,imgwebp,*/*;q=0.8"
                    ])

        # url 인코딩
        reqUrl = (url + 'title' + others + reqTitle).encode('UTF-8')
        #대상 Url 설정
        c.setopt(c.URL, reqUrl)

        # 결과로 반환된 값을 저장할 buffer 지정
        # ByteIO를 사용할 것을 권장
        c.setopt(c.WRITEDATA, buffer)

        # SSL 인증서 확인 무시
        c.setopt(c.SSL_VERIFYPEER, False)

        # 웹에 접근한 후, 세션을 종료하는 코드
        c.perform()
        c.close()

        #저장된 데이터를 Bs4 객체에 넣어 파싱 및 출력
        body = buffer.getvalue().decode('utf-8')
        soup = BeautifulSoup(body, 'html.parser')
        obj = soup.find("h2",{"class":"EXLResultTitle"}).text
        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": obj
                        }
                    }
                ]
            }
        }
        print("time :", time.time() - start)
        return JsonResponse(res)

@csrf_exempt
def test(request):
    if request.method == 'POST':
        result = {
            "harry potter": "해리포터",
            "didi": "디디의 우산"
        }
        req = json.loads(request.body)
        reqTitle = req["action"]["detailParams"]["title"]["value"]
        answer = result[reqTitle]

        res = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "디디의 우산"
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
