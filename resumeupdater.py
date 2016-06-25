import requests
from lxml import html

def upresume(logn, pswd, resume_name):
    with requests.Session() as c:
        url = 'https://jobs.tut.by/account/login'
        USERNAME = logn
        PASSWORD = pswd
        HEADERS = {'Referer': 'https://jobs.tut.by/account/login',\
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',\
    'Host':'jobs.tut.by',\
    'Accept-Encoding':'gzip, deflate, br',\
    'Accept-Language':'en-US,en;q=0.5',\
    'Connection':'keep-alive',\
    'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:47.0) Gecko/20100101 Firefox/47.0',\
    'DNT':'1'
    }
        c.get(url,headers=HEADERS)
        token = c.cookies['_xsrf']
        login_data = dict(username=USERNAME,\
    password=PASSWORD,\
    backUrl='https://jobs.tut.by/',\
    failUrl='/account/login?backurl=%2F&role=',\
    _xsrf=token
    )
        c.post(url, data=login_data, headers=HEADERS)
        c.get('https://jobs.tut.by/account/login')
        page = c.get('https://jobs.tut.by/applicant/resumes')
        tree = html.fromstring(page.content)
        all_links = tree.xpath('//a[@href]')
        for link in all_links:
            try:
                if link.text == resume_name:
                    resume_link = link
            except Exception as err:
                 raise err
    #    print resume_link.attrib['href']
        url = 'https://jobs.tut.by' + resume_link.attrib['href']
        id_resume = url.split('/')[-1]
        c.get(url)
        params_data = {'resume': id_resume, 'undirectable':'true'}
        url_update = 'https://jobs.tut.by/applicant/resumes/touch'
        CHANGES = {
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',\
    'X-Xsrftoken': c.cookies['_xsrf'],\
    'X-Requested-With': 'XMLHttpRequest',\
    'Referer': url,\
    'Accept': '*/*',\
    'Content-Length': '63'
    }
        HEADERS.update(CHANGES)
        r = c.post(url=url_update, data=params_data, headers=HEADERS)
        page = c.get(url)
        return r.status_code, page.content  
