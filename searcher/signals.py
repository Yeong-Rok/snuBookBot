# -*- coding: utf-8 -*-
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Title, Author, Response

import requests
from bs4 import BeautifulSoup

@receiver(post_save, sender = Title)
def title_post_save(sender, **kwargs):
    req = kwargs['instance']
    response = search_title(req.title)
    books = select_books(response)
    books_length = len(books)
    is_more = True if books_length > 10 else False
    result = parse(books, books_length)
    url = get_title_url(req.title)
    create_response(result, req.user_id, url, is_more)

@receiver(post_save, sender = Author)
def author_post_save(sender, **kwargs):
    req = kwargs['instance']
    response = search_author(req.author)
    books = select_books(response)
    books_length = len(books)
    is_more = True if books_length > 10 else False
    result = parse(books, books_length)
    url = get_author_url(req.author)
    create_response(result, req.user_id, url, is_more)

def select_books(response):
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    books = soup.select('.EXLSummaryFields')

    return books

def parse(books, books_length):
    result = []
    for i in range(9):
        if (i >= books_length):
            break
        author = books[i].select('.EXLResultAuthor') 
        detail = books[i].select('.EXLResultAvailability')[0]
        availability = detail.text.lstrip().split(':')[0]
        if (availability == '이용가능'):
            availability = '✅️'+ availability
        else:
            availability = '⚠️' + availability

        book = {}
        book['title'] = books[i].select('.EXLResultTitle')[0].text.strip()
        book['author']  = author[0].text if author else '' 
        book['availability'] = availability 
        book['publisher'] = books[i].select('.EXLResultFourthLine')[0].text
        book['callNumber'] = detail.select('.EXLAvailabilityCallNumber')[0].text.lstrip().replace('(', '').replace(')', '').rstrip()
        result.append(book)

    return result

def create_response(result, _user_id, _url, is_more):
    Response.objects.create(
        user_id = _user_id,
        url = _url,
        more = is_more,

        title0 = result[0]['title'] if len(result) > 0 else None,
        detail0 = result[0]['availability'] + ": " + result[0]['author'] + " ; " + result[0]['publisher'] if len(result) > 0 else None,
        callNumber0 = result[0]['callNumber'] if len(result) > 0 else None,


        title1 = result[1]['title'] if len(result) > 1 else None,
        detail1 = result[1]['availability'] + ": " + result[1]['author'] + " ; " + result[1]['publisher'] if len(result) > 1 else None,
        callNumber1 = result[1]['callNumber'] if len(result) > 1 else None,

        title2 = result[2]['title'] if len(result) > 2 else None,
        detail2 = result[2]['availability'] + ": " + result[2]['author'] + " ; " + result[2]['publisher'] if len(result) > 2 else None,
        callNumber2 = result[2]['callNumber'] if len(result) > 2 else None,

        title3 = result[3]['title'] if len(result) > 3 else None,
        detail3 = result[3]['availability'] + ": " + result[3]['author'] + " ; " + result[3]['publisher'] if len(result) > 3 else None,
        callNumber3 = result[3]['callNumber'] if len(result) > 3 else None,

        title4 = result[4]['title'] if len(result) > 4 else None,
        detail4 = result[4]['availability'] + ": " + result[4]['author'] + " ; " + result[4]['publisher'] if len(result) > 4 else None,
        callNumber4 = result[4]['callNumber'] if len(result) > 4 else None,

        title5 = result[5]['title'] if len(result) > 5 else None,
        detail5 = result[5]['availability'] + ": " + result[5]['author'] + " ; " + result[5]['publisher'] if len(result) > 5 else None,
        callNumber5 = result[5]['callNumber'] if len(result) > 5 else None,

        title6 = result[6]['title'] if len(result) > 6 else None,
        detail6 = result[6]['availability'] + ": " + result[6]['author'] + " ; " + result[6]['publisher'] if len(result) > 6 else None,
        callNumber6 = result[6]['callNumber'] if len(result) > 6 else None,

        title7 = result[7]['title'] if len(result) > 7 else None,
        detail7 = result[7]['availability'] + ": " + result[7]['author'] + " ; " + result[7]['publisher'] if len(result) > 7 else None,
        callNumber7 = result[7]['callNumber'] if len(result) > 7 else None,

        title8 = result[8]['title'] if len(result) > 8 else None,
        detail8 = result[8]['availability'] + ": " + result[8]['author'] + " ; " + result[8]['publisher'] if len(result) > 8 else None,
        callNumber8 = result[8]['callNumber'] if len(result) > 8 else None,

        title9 = result[9]['title'] if len(result) > 9 else None,
        detail9 = result[9]['availability'] + ": " + result[9]['author'] + " ; " + result[9]['publisher'] if len(result) > 9 else None,
        callNumber9 = result[9]['callNumber'] if len(result) > 9 else None,
    )

url = 'https://primoapac01.hosted.exlibrisgroup.com/primo_library/libweb/action/search.do?ct=facet&fctN=facet_library&fctV=MAIN&rfnGrp=1&rfnGrpCounter=1&frbg=&vl(19022558UI4)=books&&indx=1&fn=search&dscnt=0&vl(1UIStartWith0)=contains&tb=t&mode=Advanced&vid=82SNU&ct=search&vl(D15540194UI3)=all_items&vl(19016099UI0)='
others = '&vl(15540188UI0)=AND&srt=rank&tab=all&Submit=검색&vl(19016102UI5)=all_items&dum=true&vl(freeText0)='

def search_title(target):
    return requests.get(url + 'title' + others + target)

def search_author(target):
    return requests.get(url + 'creator' + others + target)

def get_title_url(target):
    return url + 'title' + others + target

def get_author_url(target):
    return url + 'creator' + others + target
