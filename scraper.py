from bs4 import BeautifulSoup
from github import Github
import requests
import re

def scrape_github(search_term, num_pages):
    for k in range(1, num_pages+1):
        url = "https://github.com/search?p=" + str(k) + "&q=" + search_term
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")

        results = soup.find(id = "js-pjax-container")
        repo = results.find_all("li", class_ = "repo-list-item hx_hit-repo d-flex flex-justify-start py-4 public source")

        flag = 0
        scraped_info = []

        for repo in repo:
            #get the name of the repository
            repo_name = repo.find("a", class_= "v-align-middle").text.strip()
        
            #get the description of the repository
            find_repo_desc = repo.find("p", class_ = "mb-1")
            if find_repo_desc:
                repo_desc = find_repo_desc.text.strip()
            else:
                repo_desc = None
        
            #get tags
            all_tags = repo.find_all("a", class_= "topic-tag topic-tag-link f6 px-2 mx-0")
            tags = []
        
            for repot in all_tags:
                tags.append(repot.text.strip())
            if len(tags) == 0:
                tags = None    

            #get number of stars
            starref = "/github/" + repo_name + "/stargazers"
            find_stars = repo.find("a", href = starref)
            if find_stars:
                stars = find_stars.text.strip()
            else:
               stars = None

            #get the language
            find_language = repo.find("span", itemprop = "programmingLanguage")
            if find_language:
                language = find_language.text.replace("\n"," ").strip()
            else:
                language = None
           
            #get the license
            looklicen = repo.find_all("div", class_= "mr-3")
            for looklicen in looklicen:
                licen_check = looklicen.text.strip()
                if "license" in licen_check:
                   licen = licen_check
                   flag = 1
                if flag == 0:
                   licen = None
            flag = 0
            
            #get lasted updated 
            updated = repo.find("relative-time", class_= "no-wrap").text.strip()
            
            #get the number of issues
            try:
                find_issues = repo.find("a", class_ = "Link--muted f6").text.strip()
                list_issues = re.findall('(\d+?)\s', find_issues)
                if list_issues:
                    issues = int(list_issues[0])
            except AttributeError:
                issues = None
            
            repo_dict = {
            "repo_name": repo_name,
            "description": repo_desc,
            "tags": tags,
            "num_stars": stars,
            "language": language,
            "license": licen,
            "last_updated": updated,
            "num_issues": issues
            }
            
            scraped_info.append(repo_dict)
    return scraped_info
 
def github_api(search_term, num_pages):
    # pygithub object
    g = Github()

    repo_search = g.search_repositories(search_term)
  
    repo_info = []

    for repo in repo_search[0:10]:
        
        try:
            licen = repo.get_license().license.name
            if licen == "Other":
                licen = None
        except:
            licen = None
            
        repo_dic = {
        "repo_name": repo.full_name,
        "description": repo.description,
        "num_stars": repo.stargazers_count,
        "language": repo.language,
        "license": licen,
        "last_updated": repo.updated_at,
        "has_issues": repo.has_issues
        } 
        
        repo_info.append(repo_dic)
    
    return repo_info