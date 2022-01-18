
def followers():
    # !pip install bs4

    from bs4 import BeautifulSoup
    import requests

    url = 'https://www.instagram.com/imvickykumar999/'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')
    # m = soup.find_all(['meta'])
    a = soup.find('meta', attrs = {'name':'description'})
    d = a['content']
    l = d.split(',')
    return l
