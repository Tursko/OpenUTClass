import requests
import json
from bs4 import BeautifulSoup


with open('login_info.json') as file:
    login_info = json.load(file)


def get_course_page(url, login_creds):

    session = requests.session()

    login_url = 'https://login.utexas.edu/login/UI/Login'

    request = session.post(login_url, data=login_creds)

    request_soup = BeautifulSoup(request.text, 'html.parser')

    if request_soup.title.string != "The University of Texas at Austin":
        raise ValueError("Login failed: " + request_soup.title.string)

    request = session.get(url, allow_redirects=True)

    request_soup = BeautifulSoup(request.text, 'html.parser')

    AuthURL = request_soup.body.form['action']
    AuthParamKey = request_soup.body.form.input['name']
    AuthParamVal = request_soup.body.form.input['value']

    request = session.post(AuthURL, data={AuthParamKey: AuthParamVal})

    request_soup = BeautifulSoup(request.text, 'html.parser')

    course_url = request_soup.body.form['action']

    request = session.get(course_url)

    return request


def get_course_status(course_id, semester_id=20189):

    page = get_course_page(
        'https://utdirect.utexas.edu/apps/registrar/course_schedule/{0}/{1}/'.format(semester_id, course_id),
        login_info)

    page_soup = BeautifulSoup(page.text, 'html.parser')

    return page_soup.find("td", {"data-th": "Status"}).string
