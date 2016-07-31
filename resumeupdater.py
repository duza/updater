import requests
from lxml import html

def upresume(login, paswd, resume_name):
    ''' Do a update resume in jobs.tut.by
        upresume(login, password, resume_name) ->
            tuple(request.status_code, page.content)
        Function accept three arguments: user's login and
        password, name of the own resume on jobs.tut.by.
        It search the specified page of resume and try
        update it.
        Function returns tuple: the status code after
        try to update resume and content of page after 
        its try''' 
        
    with requests.Session() as c:
        url = 'https://jobs.tut.by/account/login'
        headers = {'Referer': 'https://jobs.tut.by/account/login',\
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',\
    'Host':'jobs.tut.by',\
    'Accept-Encoding':'gzip, deflate, br',\
    'Accept-Language':'en-US,en;q=0.5',\
    'Connection':'keep-alive',\
    'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:47.0) Gecko/20100101 Firefox/47.0',\
    'DNT':'1'
    }
        c.get(url,headers=headers)
        token = c.cookies['_xsrf']
        login_data = dict(username=login,\
    password=paswd,\
    backUrl='https://jobs.tut.by/',\
    failUrl='/account/login?backurl=%2F&role=',\
    _xsrf=token
    )
        c.post(url, data=login_data, headers=headers)
        c.get('https://jobs.tut.by/account/login')
        page = c.get('https://jobs.tut.by/applicant/resumes')
        page.encoding = "utf-8"
        tree = html.fromstring(page.content)
        all_links = tree.xpath('//a[@href]')
        for link in all_links:
            try:
                if resume_name in html.tostring(link):
                    resume_link = link
            except Exception as err:
                 raise err
        url = 'https://jobs.tut.by' + resume_link.attrib['href']
        id_resume = url.split('/')[-1]
        c.get(url)
        params_data = {'resume': id_resume, 'undirectable':'true'}
        url_update = 'https://jobs.tut.by/applicant/resumes/touch'
        changes = {
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',\
    'X-Xsrftoken': c.cookies['_xsrf'],\
    'X-Requested-With': 'XMLHttpRequest',\
    'Referer': url,\
    'Accept': '*/*',\
    'Content-Length': '63'
    }
        headers.update(changes)
        r = c.post(url=url_update, data=params_data, headers=headers)
        page = c.get(url)
        return r.status_code, page.content
