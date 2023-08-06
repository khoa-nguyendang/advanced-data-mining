from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup


base_url = 'https://paperswithcode.com'
ignore1 = "code implementation"
ignore2 = "\n Paper\n"
ignore3 = "\n Code\n"

#paper_title_to_words from title, split down to a list of words
def paper_title_to_words(title: str) -> list:
    if len(title) <= 0:
        return []
    
    return title.split(" ")

#crawl_by_search_result_url base on paper title => 
# step 1. from encoded URL, extract all possible result.
# step 2. get top 1 result base on number of matching title words, then go to that page.
# step 3. find element contains github url. 
# step 4. print github url if any, else return not found.
def crawl_by_search_result_url(url: str) -> list:
    result = []
    browser = webdriver.Chrome()
    browser.get(url)
    content = browser.page_source
    soup = BeautifulSoup(content, features="html.parser")
    all_a_tags = soup.find_all("a",attrs={'class': None}, href=True)
    paper_a_tags = [i for i in all_a_tags if '/paper/' in i['href']]
    if len(paper_a_tags) > 5:
        paper_a_tags = paper_a_tags[:5]
        
    for a_tag in paper_a_tags:
        paper_title = a_tag.get_text()
        if paper_title.strip() == "" or paper_title.find(ignore1) != -1  or paper_title.find(ignore2) != -1  or paper_title.find(ignore3) != -1:
            continue
        
        github_links = crawl_by_paper_page_url(a_tag['href'], browser=browser)
        result.append({
            "title": paper_title,
            "github_links": github_links
        })
        
    browser.quit()
    return result

#crawl_by_paper_page_url render then find github urls
def crawl_by_paper_page_url(url: str, browser: webdriver.Chrome) -> list:
    if not url.startswith(base_url):
        url = base_url + url
    browser.get(url)
    content = browser.page_source
    soup = BeautifulSoup(content, features="html.parser")
    all_a_tags = soup.find_all("a", attrs={"class": ["code-table-link"]}, href=True)
    github_a_tags = [i['href'] for i in all_a_tags if 'github.com' in i['href']]
    github_a_tags = list(set(github_a_tags))
    return github_a_tags


