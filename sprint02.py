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
query lab2S2 {
  search(query: "stars:>100 language:Python", type: REPOSITORY, first: 20{AFTER}) {
    nodes {
      ... on Repository {
        forks {
          totalCount
        }
        createdAt
        watchers {
          totalCount
        }
        url
        stargazers {
          totalCount
        }
        releases {
          totalCount
        }
        nameWithOwner
        name
        isFork
        primaryLanguage {
          name
        }
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}

"""


#substituindo o comando after na consulta inicial
finalQuery = query.replace("{AFTER}", "")

#obtendo a primeira query
resultado = run_query(finalQuery, headers)

#carregando o json em um dicionario python
nodes = resultado['data']['search']['nodes']

conta_repositorios_python = 0

total_pages =0
next_page  = resultado["data"]["search"]["pageInfo"]["hasNextPage"] 


while (total_pages < 1000 and next_page): 
    
    #montando as query apos a primeira, detectando o cursor da ultima entrada da query anterior
    # adicionando o campo after na query do graphql
    # rodando o script com a nova query 
    #carregando o json em um dicionario python
    cursor = resultado["data"]["search"]["pageInfo"]["endCursor"]
    next_query = query.replace("{AFTER}", ", after: \"%s\"" % cursor)
    resultado = run_query(next_query, headers)
    nodes += resultado['data']['search']['nodes']
    next_page  = resultado["data"]["search"]["pageInfo"]["hasNextPage"]
    total_pages += 1
      
      
#preparando o cabecalho do arquivo csv
with open("d:/LAB-Exp-Software/LAB02/repos-python.csv", 'w') as arquivo_repositorios_gvan:

  cabecalho = ['name', 'nameWithOwner','stargazers','watchers','forks','releases','createdAt','primaryLanguage','url', 'isFork']
  writer = DictWriter(arquivo_repositorios_gvan, fieldnames=cabecalho)
  writer.writeheader()

  #escrevendo no arquivo csv
  for node in nodes:
    writer.writerow(node)    

print("Execucao encerrada!")
