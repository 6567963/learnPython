import re
import requests
import http.cookiejar
from PIL import Image
import time
import hashlib
import random
import urllib

# POST请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (SymbianOS/9.3; Series60/3.2 NokiaE72-1/021.021; Profile/MIDP-2.1 Configuration/CLDC-1.1 )',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}
# 登录时POST请求头
headers_login = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding": "gzip,deflate,sdch",
    "Accept-Language": "en-US,en;q=0.8,zh;q=0.6",
    "Host":"passport.baidu.com",
    "Upgrade-Insecure-Requests": "1",
    "Origin":"http://www.baidu.com",
    "Referer":"http://www.baidu.com/",
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36"
}

# 贴吧关注请求头
headers_guanzhu = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.8,zh;q=0.6",
    "Accept-Encoding": "gzip,deflate,sdch"
}
session = requests.Session()
session.cookies = http.cookiejar.LWPCookieJar("cookie")

def fetch_cookies_and_bduss():
    user = "官方发言人"
    password = "zy524488129"

    token = ""
    verifycode = ""
    codestring = ""

    # 第一次POST的信息，如果需要验证码则获取验证码并进行第二次POST
    login_data_first_time = {
        "staticpage": "https://passport.baidu.com/static/passpc-account/html/V3Jump.html",
        "token": token,
        "tpl": "mn",
        "username": user,
        "password": password,
        "loginmerge": "true",
        "mem_pass": "on",
        "logintype": "dialogLogin",
        "logLoginType": "pc_loginDialog",
    }
    # 第二次POST的信息
    login_data_second_time = {
        "staticpage": "https://passport.baidu.com/static/passpc-account/html/V3Jump.html",
        "codestring": codestring,
        "verifycode": verifycode,
        "token": token,
        "tpl": "mn",
        "username": user,
        "password": password,
        "loginmerge": "true",
        "mem_pass": "on",
        "logintype": "dialogLogin",
        "logLoginType": "pc_loginDialog",
    }

    print("正在进行登录操作")

    #获取session cookie
    while(1):
        content = session.get("https://www.baidu.com").text
        time.sleep(random.uniform(10,20))
        content = session.get("https://passport.baidu.com/v2/api/?login").text
        time.sleep(random.uniform(10,20))

        # 获取token信息
        try:
            content = session.get("https://passport.baidu.com/v2/api/?getapi&class=login&tpl=mn&tangram=true",
                                  headers=headers).text
            #print(content)
            token =  re.compile("login_token=\'(\w+?)\';").findall(str(content))[0]
            login_data_first_time["token"] = token
            login_data_second_time["token"] = token
        except:
            print("无法获取token，正在退出...")
            return False

        #进行第一次登录
        request = session.post("https://passport.baidu.com/v2/api/?login", headers=headers_login,
                               data=login_data_first_time)
        time.sleep(random.uniform(10,20))
        is_captcha = re.compile('error=(\w+?)&').findall(str(request.text))[0]
        if is_captcha == "0":
            BDUSS = ""
            for i in  session.cookies:
                if i.name == "BDUSS":
                    BDUSS = i.value
            if BDUSS:
                print("登录成功")
                return True
            else:
                print("登录失败")
                return False

        elif is_captcha == "4" or is_captcha == "7":
            print("密码错误")
            login_data_first_time["password"] = input("请重新输入密码：")
            session.cookies.clear()
            continue
        elif is_captcha == "5" or is_captcha == "120019":
            print("账号异常，请手动登录www.baidu.com验证手机号")
            exit()
        elif is_captcha == "257":
            # 获取验证码地址并写入第二次POST信息
            codestring = re.compile('codestring=(.+?)&username').findall(str(request.text))[0]
            login_data_second_time["codestring"] = codestring
            # 访问验证码地址并下载图片
            request = session.get("https://passport.baidu.com/cgi-bin/genimage?" + codestring, headers=headers)
            with open('captcha.gif', 'wb') as f:
                f.write(request.content)
            img = Image.open('captcha.gif')
            img.show()
            verifycode = input("请填写验证码：")
            # 将验证码内容写入第二次POST信息
            login_data_second_time["verifycode"] = verifycode
            # 进行第二次登陆POST
            request = session.post("https://passport.baidu.com/v2/api/?login", headers=headers_login,
                                   data=login_data_second_time)
            is_captcha2 = re.compile('error=(\w+?)&').findall(str(request.text))[0]
            if is_captcha2 == "0":
                # 提取并验证BDUSS
                BDUSS = ""
                for i in session.cookies:
                    if i.name == 'BDUSS':
                        BDUSS = i.value
                if BDUSS:
                    print("登录成功！")
                    return True
                else:
                    print("这是个BUG")
                    return False
            elif is_captcha2 == "6":
                print("验证码错误！")
                session.cookies.clear()
                continue
            elif is_captcha2 == "4" or is_captcha2 == "7":
                print("密码错误")
                password = input("请重新输入密码：")
                login_data_first_time["password"] = password
                login_data_second_time["password"] = password
                session.cookies.clear()
                continue
            else:
                print("未知错误2，错误代码为{0}，请联系管理员".format(is_captcha2))
                exit()
        elif is_captcha == "50028":
            print("输入密码错误次数过多，请三小时后再试")
            exit()
        else:
            print("未知错误1，错误代码为{0}，请联系管理员".format(is_captcha))
            exit()
        # 保存COOKIES信息
        session.cookies.save(ignore_discard=True, ignore_expires=True)


def is_login():
    url = "https://tieba.baidu.com/index.html"
    content = session.get(url,headers = headers).text
    loc = content.find("爱逛的吧")
    if loc > 0 :
        return True
    else:
        return False



def guanzhu_tieba():

    fid = ""
    fname = ""
    tbs = ""
    uid = "%E5%AE%98%E6%96%B9%E5%8F%91%E8%A8%80%E4%BA%BA"
    t = time.time()
    guanzhu_post = {
       "_t":int(round(t * 1000)),
        "fid":fid,
        "fname":fname,
        "ie":"utf-8",
        "tbs":tbs,
        "uid":uid
    }


    request = session.get("http://tieba.baidu.com/f/index/forumclass").text
    guanzhu_sum = 0
    #content = re.compile('<a.*?href="(.+)".*?>(.*?)</a>').findall(request)
    #content = re.compile('<a rel="noopener" class="class-item-title" href="(.+)">(.*?)</a>').findall(request)
    content = re.compile('<a rel="noopener" class="class-item-title" href="([^"]*)".*?>([\S\s]*?)</a>').findall(request)
    #print(content)

    for u in content:
        time.sleep(random.uniform(2,5))
        #print(u[0])
        for i in range(1,6):
            #print("http://tieba.baidu.com" + u[0]+"&st=new&pn="+str(i))
            try:
                print(u[1]+"第"+str(i)+"页开始关注")
                request = session.get("http://tieba.baidu.com"+u[0]+"&st=new&pn="+str(i)).text
            except:
                print(u[1] + "第" + str(i) + "页无数据")
                continue
            time.sleep(random.uniform(10,20))
            content1 = re.compile('<div class="ba_like " data-fid="([^"]*)" data-fname="([\S\s]*?)" title="我喜欢"></div>').findall(
                request)
            if len(content1)==0:
                print(u[1] + "第" + str(i) + "页全部关注完毕")
                continue
            for s1 in content1:
                guanzhu_post["fid"] = s1[0]
                guanzhu_post["fname"] = s1[1]
                tbs =  fetch_tieba_info(s1[1])
                if tbs:
                    guanzhu_post["tbs"] = fetch_tieba_info(s1[1])
                else:
                    continue
                time.sleep(random.uniform(10,20))
                content2 = session.post("http://tieba.baidu.com/f/like/commit/add",headers=headers_guanzhu,data=guanzhu_post).text
               # print(content2)
                is_captcha = re.compile('"no":(\w+?)').findall(content2)
                if is_captcha:
                    if is_captcha[0] == '0':
                        print(s1[1]+":关注成功")
                        guanzhu_sum = guanzhu_sum+1
                    elif is_captcha[0] == '221':
                        continue
                else:
                    continue

    print("关注总数:"+str(guanzhu_sum))

def qx_guanzhu_tieba():

    fid = ""
    fname = ""
    tbs = ""
    uid = "%E5%AE%98%E6%96%B9%E5%8F%91%E8%A8%80%E4%BA%BA"
    t = time.time()
    guanzhu_post = {
        "_t": int(round(t * 1000)),
        "fid": fid,
        "fname": fname,
        "ie": "utf-8",
        "tbs": tbs,
        "uid":"",
        "usn":uid
    }

    request = session.get("http://tieba.baidu.com/f/index/forumclass").text
    guanzhu_sum = 0
    # content = re.compile('<a.*?href="(.+)".*?>(.*?)</a>').findall(request)
    # content = re.compile('<a rel="noopener" class="class-item-title" href="(.+)">(.*?)</a>').findall(request)
    content = re.compile('<a rel="noopener" class="class-item-title" href="([^"]*)".*?>([\S\s]*?)</a>').findall(
        request)
    # print(content)

    for u in content:
        time.sleep(random.uniform(2, 5))
        # print(u[0])
        for i in range(1, 6):
            # print("http://tieba.baidu.com" + u[0]+"&st=new&pn="+str(i))
            try:
                print(u[1] + "第" + str(i) + "页开始取消关注")
                request = session.get("http://tieba.baidu.com" + u[0] + "&st=new&pn=" + str(i)).text
            except:
                print(u[1] + "第" + str(i) + "页无数据")
                continue
            time.sleep(random.uniform(10, 20))
            content1 = re.compile(
                '<div class="ba_like " data-fid="([^"]*)" data-fname="([\S\s]*?)" title="我喜欢"></div>').findall(
                request)
            content11 = re.compile(
                '<div class="ba_like is_like " data-fid="([^"]*)" data-fname="([\S\s]*?)" title="我喜欢"></div>').findall(
                request)
            if len(content1) != 0:
                for s1 in content1:
                    guanzhu_post["fid"] = s1[0]
                    guanzhu_post["fname"] = s1[1]
                    tbs = fetch_tieba_info(s1[1])
                    if tbs:
                        guanzhu_post["tbs"] = fetch_tieba_info(s1[1])
                    else:
                        continue
                    time.sleep(random.uniform(10, 20))
                    content2 = session.post("http://tieba.baidu.com/f/like/commit/delete", headers=headers_guanzhu,
                                            data=guanzhu_post).text
                    print(s1[1] + ":取消关注成功")

            if len(content11) != 0:
                for s1 in content1:
                    guanzhu_post["fid"] = s1[0]
                    guanzhu_post["fname"] = s1[1]
                    tbs = fetch_tieba_info(s1[1])
                    if tbs:
                        guanzhu_post["tbs"] = fetch_tieba_info(s1[1])
                    else:
                        continue
                    time.sleep(random.uniform(10, 20))
                    content3 = session.post("http://tieba.baidu.com/f/like/commit/delete", headers=headers_guanzhu,
                                            data=guanzhu_post).text
                    print(s1[1] + ":取消关注成功")

            print(u[1] + "第" + str(i) + "页全部取消关注完毕")


        #下一页
        #&st=new&pn=2
        #print(content)


def fetch_tieba_info(tieba):
    # 获取是否签到以及两个POST用信息
    url = "http://tieba.baidu.com/mo/m?kw=" + tieba
    content = session.get(url, headers=headers, allow_redirects=False).text
    re_tbs = '<input type="hidden" name="tbs" value="(.+?)"\/>'
    _tbs = re.findall(re_tbs, content)
    tbs = _tbs and _tbs[0] or None
    if tbs == None:
        tbs = re.compile('itb_tbs=(\w+?)&').findall(content)

    return tbs



if __name__ == '__main__':
    try:
        session.cookies.load(ignore_discard=True);
    except:
        print(u"cookie未加载")
        if fetch_cookies_and_bduss() == False:
            exit()

    if is_login():
        print("成功登录")
        session.cookies.save(ignore_discard=True,ignore_expires=True)

        guanzhu_tieba()
        #qx_guanzhu_tieba()

