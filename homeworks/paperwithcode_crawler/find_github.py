

import sys
import time
import crawler
from requests.utils import requote_uri

search_base_url = 'https://paperswithcode.com/search?q_meta=&q_type=&q='


args = sys.argv
if len(args) <= 1:
    print("require Paper Title to start processing process.")
    exit()
    
paper_title = sys.argv[1]
paper_word = crawler.paper_title_find_githubto_words(paper_title)
encoded_url = search_base_url + requote_uri(paper_title)
result = crawler.crawl_by_search_result_url(encoded_url)
if len(result) > 0:
    for i in result:
        print(f"title: {i['title']}")
        print("github urls: ")
        for idx, j in enumerate(i['github_links']):
            print(f'{idx+1}: {j}')
else:
    print("not found any code")