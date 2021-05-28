import requests
import urllib
from bs4 import BeautifulSoup
import json
from django.http import HttpResponse
from datetime import datetime, timedelta, timezone
import dateutil.parser
import locale
from .models import TimeTable, Notification, Assignment
from django.core import serializers
import base64
import configparser


def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)


JST = timezone(timedelta(hours=+9), 'JST')
locale.setlocale(locale.LC_CTYPE, "Japanese_Japan.932")
s = requests.Session()


def login():
    login = True

    ini = configparser.ConfigParser()
    ini.read('C:/ProgramData/SinPandA/data/ecs.ini', 'UTF-8')

    username = decode("pand", ini['user']['user'].encode('utf-8').strip())
    password = decode("pand", ini['user']['password'].encode('utf-8').strip())

    # ログインに使うURL
    url = "https://cas.ecs.kyoto-u.ac.jp/cas/login?service=https://panda.ecs.kyoto-u.ac.jp/sakai-login-tool/container"

    # ログインフォームからLTを抜き出す
    r1 = s.get(url)
    soup = BeautifulSoup(r1.content, 'html.parser')
    for input in soup.select('form input'):
        if input['name'] == 'lt':
            lt = input['value']
            login = False

    if login == False:
        # ログイン処理
        params = {'_eventId': 'submit', 'execution': 'e1s1', 'lt': lt,
                  'username': username, 'password': password}
        params = urllib.parse.urlencode(params)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        s.post(url=url, data=params, headers=headers)


def getTimetable(request):
    login()

    lList = []

    # 課題一覧取得
    r = s.get('https://panda.ecs.kyoto-u.ac.jp/direct/assignment/my.json')
    r.encoding = r.apparent_encoding
    aData = json.loads(r.content.decode())

    for a in aData["assignment_collection"]:
        if a["status"] == "OPEN":
            r4 = s.get('https://panda.ecs.kyoto-u.ac.jp/direct/site/' +
                       a["context"] + '.json')
            r4.encoding = r4.apparent_encoding
            lData = json.loads(r4.content.decode())
            due = dateutil.parser.parse(a["dueTimeString"]).astimezone(
                timezone(timedelta(hours=+9)))
            drop = dateutil.parser.parse(a["dropDeadTimeString"]).astimezone(
                timezone(timedelta(hours=+9)))
            limit = (due-datetime.now(JST)).total_seconds()
            if limit > 0:
                lList.append({'ltitle': lData['title'], 'atitle': a["title"], 'due': due.strftime('%Y年%m月%d日 %H:%M'), 'drop': drop.strftime('%Y年%m月%d日 %H:%M'), 'limit': str(
                    int(limit/86400)) + '日' + str(int((limit % 86400)/3600)) + '時間' + str(int((limit % 3600)/60)) + '分', 'url': a["entityURL"], 'limitsecond': limit, 'assignment': due.strftime('%Y-%m-%d %H:%M:%S')})

    # 履修講義一覧取得

    period = "後期"
    if 4 <= int(datetime.now(JST).strftime('%m')) and int(datetime.now(JST).strftime('%m')) <= 9:
        period = "前期"
    year = '20' + datetime.now(JST).strftime('%y')
    dow = ['月', '火', '水', '木', '金']
    tim = ['１', '２', '３', '４', '５']
    tt = [{}] * 25
    r3 = s.get('https://panda.ecs.kyoto-u.ac.jp/direct/site.json?_limit=2000')
    r3.encoding = r3.apparent_encoding
    lData = json.loads(r3.content.decode())
    for l in lData["site_collection"]:
        title = l["title"]
        if title[1: 5] == year and title[5: 7] == period:
            for d in range(len(dow)):
                if title[7] == dow[d]:
                    for t in range(len(tim)):
                        if title[8] == tim[t]:
                            due = ''
                            flag = 0
                            for ll in lList:
                                if ll["ltitle"] == title:
                                    if ll["limitsecond"] < flag or flag == 0:
                                        flag = ll["limitsecond"]
                                        due = ll["assignment"]
                            for site in l["sitePages"]:
                                if(site["title"] == "お知らせ"):
                                    notiURL = site["url"]
                                if(site["title"] == "授業資料（リソース）"):
                                    resoURL = site["url"]
                                if(site["title"] == "課題"):
                                    assiURL = site["url"]
                                if(site["title"] == "Zoom (KU License)"):
                                    zoomURL = site["url"]
                            tt[d+t*5] = {'title': title[10:], 'assignment': due, 'url': "https://panda.ecs.kyoto-u.ac.jp/portal" + l['reference'],
                                         'notiURL': notiURL, 'resoURL': resoURL, 'assiURL': assiURL, 'zoomURL': zoomURL}

    TimeTable.objects.all().delete()

    for x in range(25):
        if tt[x] != {}:
            tti = TimeTable(tt=x, title=tt[x]['title'], assignment=tt[x]['assignment'], url=tt[x]['url'],
                            notiURL=tt[x]['notiURL'], resoURL=tt[x]['resoURL'], assiURL=tt[x]['assiURL'], zoomURL=tt[x]['zoomURL'])
        else:
            tti = TimeTable(tt=x)
        tti.save()

    response = HttpResponse('')
    return response


def getAnnounce(request):
    login()

    # お知らせ一覧取得
    r = s.get('https://panda.ecs.kyoto-u.ac.jp/direct/portal/bullhornAlerts.json')
    r.encoding = r.apparent_encoding
    aData = json.loads(r.content.decode())

    Notification.objects.all().delete()

    for a in aData["alerts"]:
        if a["event"] == "asn.grade.submission":
            ni = Notification(ann=a["siteTitle"] + "から" +
                              a["title"] + "の課題が返却されました。", url=a["url"])
        elif a["event"] == "annc.new":
            ni = Notification(ann=a["siteTitle"] + "から「" +
                              a["title"] + "」というタイトルのお知らせがあります。", url=a["url"])
        elif a["event"] == "asn.new.assignment":
            ni = Notification(ann=a["siteTitle"] + "から「" +
                              a["title"] + "」というタイトルの課題が出されました。", url=a["url"])
        else:
            ni = Notification(ann=a["siteTitle"] + "から「" +
                              a["title"] + "」というタイトルのお知らせがあります。", url=a["url"])
        ni.save()

    response = HttpResponse('')
    return response


def getAssignment(request):
    login()

    # 課題一覧取得
    r = s.get('https://panda.ecs.kyoto-u.ac.jp/direct/assignment/my.json')
    r.encoding = r.apparent_encoding
    aData = json.loads(r.content.decode())

    Assignment.objects.all().delete()

    for a in aData["assignment_collection"]:
        if a["status"] == "OPEN":
            r4 = s.get('https://panda.ecs.kyoto-u.ac.jp/direct/site/' +
                       a["context"] + '.json')
            r4.encoding = r4.apparent_encoding
            lData = json.loads(r4.content.decode())
            due = dateutil.parser.parse(a["dueTimeString"]).astimezone(
                timezone(timedelta(hours=+9)))
            drop = dateutil.parser.parse(a["dropDeadTimeString"]).astimezone(
                timezone(timedelta(hours=+9)))
            limit = (due-datetime.now(JST)).total_seconds()
            if limit > 0:
                for site in lData["sitePages"]:
                    if(site["title"] == "課題"):
                        assiURL = site["url"]
                aai = Assignment(ltitle=lData['title'], atitle=a["title"], due=due.strftime('%Y年%m月%d日 %H:%M'), drop=drop.strftime(
                    '%Y年%m月%d日 %H:%M'),  url=assiURL, assignment=due.strftime('%Y-%m-%d %H:%M:%S'))
                aai.save()

    response = HttpResponse('')
    return response


def timetable(request):
    ttq = TimeTable.objects.all().order_by("tt")
    ttl = serializers.serialize('json', ttq)
    return HttpResponse(ttl, content_type="text/json-comment-filtered")


def announce(request):
    nq = Notification.objects.all().order_by('-pk')
    nl = serializers.serialize('json', nq)
    return HttpResponse(nl, content_type="text/json-comment-filtered")


def assignment(request):
    aaq = Assignment.objects.all().order_by('due')
    aal = serializers.serialize('json', aaq)
    return HttpResponse(aal, content_type="text/json-comment-filtered")
