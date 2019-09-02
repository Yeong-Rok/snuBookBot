from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Result, Response

import requests
from bs4 import BeautifulSoup

@receiver(post_save, sender = Result)
def result_post_save(sender, **kwargs):
    req = kwargs['instance']
    req_user_id = req.user_id
    req_title = req.req_title
    response = searchTitle(req_title)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    titles = soup.select('.EXLResultTitle')

    Response.objects.create(user_id = req_user_id, res_title =  titles[0].text)


url = 'https://primoapac01.hosted.exlibrisgroup.com/primo_library/libweb/action/search.do?ct=facet&fctN=facet_library&fctV=MAIN&rfnGrp=1&rfnGrpCounter=1&frbg=&vl(19022558UI4)=books&&indx=1&fn=search&dscnt=0&vl(1UIStartWith0)=contains&tb=t&mode=Advanced&vid=82SNU&ct=search&vl(D15540194UI3)=all_items&vl(19016099UI0)='
others = '&vl(15540188UI0)=AND&srt=rank&tab=all&Submit=검색&vl(19016102UI5)=all_items&dum=true&vl(freeText0)='

def searchTitle(target):
    return requests.get(url + 'title' + others + target)

def searchCreator(target):
    return requests.get(url + 'creator' + others + target)

