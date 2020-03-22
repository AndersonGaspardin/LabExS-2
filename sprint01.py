import requests
from json import dump
from json import loads
import os
import errno
import json
from csv import DictWriter


token = input("Informe seu token do github: ")
headers = {"Authorization": "Bearer " + token} 

def run_query(query, headers): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

query = """
query lab02 {
  user(login: "gvanrossum") {
    repositories(first: 50) {
      nodes {
        name
        stargazers(orderBy: {field: STARRED_AT, direction: DESC}) {
          totalCount
        }
        watchers {
          totalCount
        }
        forks {
          totalCount
        }
        releases {
          totalCount
        }
        createdAt
        primaryLanguage {
          name
        }
        url
        isFork
      }
      pageInfo {
        endCursor
        hasNextPage
      }
      totalCount
    }
  }
}


"""

resultado = run_query(query, headers)

nodes = resultado['data']['user']['repositories']['nodes']
"""next_page  = result["data"]["search"]["pageInfo"]["hasNextPage"]"""

#paginating
"""while (next_page and total_pages < 3):
    total_pages += 1
    cursor = result['data']['user']['repositries']['nodes']["endCursor"]
    next_query = query.replace("{AFTER}", ", after: \"%s\"" % cursor)
    json["query"] = next_query
    result = run_query(json, headers)
    nodes += result['data']['search']['nodes']
    next_page  = result["data"]["search"]["pageInfo"]["hasNextPage"]
"""

#saving data
with open("d:/LAB-Exp-Software/LAB02/repos-gvanrossum.csv", 'w') as arquivo_repositorios_gvan:

    cabecalho = ['name','stargazers','watchers','forks','releases','createdAt','primaryLanguage','url', 'isFork']
    writer = DictWriter(arquivo_repositorios_gvan, fieldnames=cabecalho)
    writer.writeheader()
     
    for node in nodes:
        writer.writerow(node)

