from selenium import webdriver
import encodings.idna
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import StaleElementReferenceException as StaleElementReferenceException
import sys
import time
import traceback
import requests
from bs4 import BeautifulSoup
import json
import codecs



def Beijing_time():
    r=requests.get('https://www.baidu.com')
    t=time.strptime(r.headers['date'],'%a, %d %b %Y %H:%M:%S GMT')
    return time.mktime(t)+28800

'''if(Beijing_time()-1553323438>=86400*5):
    input("测试期已过，请联系作者。")
    sys.exit() '''
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}

url1='https://www.uhaozu.com/goods/usercenter/list'
#13296751951    777888999aa
'''
{'domain': '.uhaozu.com', 'expiry': 1548966565.550468, 'httpOnly': False, 'name': 'uid', 'path': '/', 'secure': False, 'value': 'd8AZUpWrOsfV1GUYswbdixom5hesDuIqitcGxBXIUDa2333OVcWqWQasPS89_DPGecQ-52bG7jR0m_l5CvdA8DcDDmGp5-tix0Hn4cc8LAf8QM2SFN_fjkAVAaHaIKGyvhOgt2Odvyvejp2mXlLCI0mrVe6Eqy7VBQjZhIzIEA..'}
'''
url2='https://www.zuhaowan.com/Account/accountrentlist/p/1.html'
#https://www.zuhaowan.com/account/accountrentlist.html
#qq654833404    654833404
'''
{'domain': 'www.zuhaowan.com', 'httpOnly': False, 'name': 'stampu', 'path': '/', 'secure': False, 'value': '09F603228D321A29B31EABE676EC3AD17DA288EAA2F99FA3D79333E6951F4DFE6A2754E7678C391FD47D2B20F7DDCCBCA472B30AEA387130E87DA786A82CE84F18A8FBB09AE690E48E7C6277FF783D40643CCFFBBE4E15ED3953929E349AD920008ABD7901FD387E48921BE69DAFD6635D37F2F96FB31749B2D4599789B3E14C39D6893E2FB78441B8791D78DEA6B4AC118D5A1C343645348E590D4234685D022D719603BD29D2585F0E29A2A00E25DBD16DBE78241F3AE05726F0988CDF0F88EA3F9E2A6712BB'}
'''

driverOptions= webdriver.ChromeOptions()
driverOptions.add_argument('log-level=3')
driverOptions.add_argument('--user-agent='+headers['User-Agent'])
browser = webdriver.Chrome("chromedriver",0,driverOptions)

browser.get(url2)
input("登录租号玩，完成后回车……")
cookies=browser.get_cookies()

""" with open("1.json", "r", encoding="utf8") as fp:
    cookies = json.loads(fp.read()) """

cookie=dict()
for i in cookies:
    if(i['name']=='stampu'):
        cookie['stampu']=i['value']
#cookie[cookies[6]['name']]=cookies[6]['value']


browser.get(url1)
input("登录U号租，完成后回车……")
cookies=browser.get_cookies()

cookie1=dict()
for i in cookies:
    if (i['name']=='uid'):
        cookie1['uid']=i['value']
#cookie1[cookies[3]['name']]=cookies[3]['value']

browser.quit()

sleep_time=input("设置等待时间：")
print("开始……")
def zuhaowan_search(idname):
    #租号玩——搜索,返回第一条状态,id
    url_serch='https://www.zuhaowan.com/Account/accountRentList.html'
    r=requests.post(url_serch,headers=headers,cookies=cookie,data={'keyWords':idname})
    s=BeautifulSoup(r.text,'lxml')
    l=s.select(".div2-li2-a span")
    condition=l[0].text.strip()
    l=s.select(".div2-li1-a span font")
    idnum=l[0].text
    return (condition,idnum)

def zuhaowan_onrent(idnum):
    url_onrent="https://www.zuhaowan.com/Account/onRent.html"
    r=requests.get(url_onrent,headers=headers,cookies=cookie,params={'id':idnum})
    s=r.text.encode('utf-8').decode("unicode_escape")
    d=json.loads(s)
    return d['message']

def zuhaowan_offrent(idnum):
    url_offrent="https://www.zuhaowan.com/Account/offRent.html"
    r=requests.get(url_offrent,headers=headers,cookies=cookie,params={'id':idnum})
    s=r.text.encode('utf-8').decode("unicode_escape")
    d=json.loads(s)
    return d['message']


def uzuhao_search(idname):
    #rentStatus 0 出租中 1 other
    #1待审核 2审核未通过  3待租 4下架 
    url='https://www.uhaozu.com/goods/usercenter/list'
    r=requests.post(url,headers=headers,cookies=cookie1,json={"gameId":"","platformId":"","carrierId":"","groupId":"","serverId":"","keyWords":idname,"isBargain":"","limitPromote":"","goodsStatus":"-1","pageSize":10,"page":1})
    d=json.loads(r.text)
    idnum=d['object'][0]['id']
    condition=d['object'][0]['goodsStatus']
    rent=d['object'][0]['rentStatus']
    return (condition,rent,idnum)

def uzuhao_onrent(idnum):
    url_onrent="https://www.uhaozu.com/goods/shelves/"+idnum
    r=requests.post(url_onrent,headers=headers,cookies=cookie1)
    d=json.loads(r.text)
    return d['responseMsg']

def uzuhao_offrent(idnum):
    url_offrent="https://www.uhaozu.com/goods/unShelves/"+idnum
    r=requests.post(url_offrent,headers=headers,cookies=cookie1)
    d=json.loads(r.text)
    return d['responseMsg']

try:
    names=list()
    with open("角色名.txt",'r',encoding='utf-8-sig') as f:
        for i in f:
            names.append(i.strip())
except:
    input("读取角色名出错……")
    sys.exit()

#input('pause')
while(1):
    print("---------------------------检索租号玩---------------------------")
    for i in names:
        try:
            c=zuhaowan_search(i)
            idnum=c[1]
            condition=c[0]
            print(i,'-当前状态-',condition)
            if(condition=="出租中"):
                try:
                    v=uzuhao_search(i)
                except:
                    print(i,"在u租号中查找失败")
                    continue
                idnum1=v[2]
                condition1=v[0]
                if(condition1==3 and v[1]==1):    #待租
                    print('***U租号***',time.asctime( time.localtime(time.time()) ),uzuhao_offrent(idnum1),i)
            if(condition=="待租"):
                try:
                    v=uzuhao_search(i)
                except:
                    print(i,"在u租号中查找失败")
                    continue
                idnum1=v[2]
                condition1=v[0]
                if(condition1==4):                  #下架
                    print('***U租号***',time.asctime( time.localtime(time.time()) ),uzuhao_onrent(idnum1),i)

        except:
            print("此账号异常",i)
            #print(traceback.format_exc())
            continue
            
    print("---------------------------检索u租号---------------------------")     
    for i in names:
        #print(i)
        try:
            c=uzuhao_search(i)
            idnum=c[2]
            condition=c[0]
            #1待审核 2审核未通过  3待租 4下架
            if(c[1]==0):
                cs="出租中"
            else:
                cs='未在出租中'
                if(condition==1):
                    cs='待审核'
                if(condition==2):
                    cs='审核未通过'
                if(condition==3):
                    cs='待租'
                if(condition==4):
                    cs='下架'
            print(i,'-当前状态-',cs)
            if(c[1]==0):         #出租中
                try:
                    v=zuhaowan_search(i)
                except:
                    print(i,"在租号玩中查找失败")
                    continue
                idnum1=v[1]
                condition1=v[0]
                if(condition1=="待租"):
                    print('***租号玩***',time.asctime( time.localtime(time.time()) ),zuhaowan_offrent(idnum1),i)
            if(condition==3 and c[1]!=0):   #待租
                try:
                    v=zuhaowan_search(i)
                except:
                    print(i,"在租号玩中查找失败")
                    continue
                idnum1=v[1]
                condition1=v[0]
                if(condition1=="下架"):
                    print('***租号玩***',time.asctime( time.localtime(time.time()) ),zuhaowan_onrent(idnum1),i)
        except:
            print("此账号异常",i)
            #print(traceback.format_exc())
            continue


    
    print("等待 %d 秒" % int(sleep_time))
    time.sleep(int(sleep_time))
