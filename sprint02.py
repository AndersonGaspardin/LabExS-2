import requests
from json import dump
from json import loads
import os
import errno
import json
from csv import DictWriter
import gc
gc.collect()

token = input("Informe seu token do github: ")
headers = {"Authorization": "Bearer " + token} 

#Funcao para , atraves da funcao requests.post da biblioteca requests, fazer uma chamada da API do graphql
def run_query(query, headers): 
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

query = """
query lab2S2 {
  search(query: "stars:>1", type: REPOSITORY, first: 100{AFTER}) {
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
#preparando o cabecalho do arquivo csv
with open("d:/LAB-Exp-Software/LAB02/repos-python.csv", 'w') as arquivo_repositorios_gvan:

  cabecalho = ['name', 'nameWithOwner','stargazers','watchers','forks','releases','createdAt','primaryLanguage','url', 'isFork']
  writer = DictWriter(arquivo_repositorios_gvan, fieldnames=cabecalho)
  writer.writeheader()


  while (conta_repositorios_python < 1000):
      
      #montando as query apos a primeira, detectando o cursor da ultima entrada da query anterior
      # adicionando o campo after na query do graphql
      # rodando o script com a nova query 
      #carregando o json em um dicionario python
      cursor = resultado["data"]["search"]["pageInfo"]["endCursor"]
      next_query = query.replace("{AFTER}", ", after: \"%s\"" % cursor)
      resultado = run_query(next_query, headers)
      nodes = resultado['data']['search']['nodes']
      next_page  = resultado["data"]["search"]["pageInfo"]["hasNextPage"]
      total_pages += 1

      
      for node in nodes:
        
        linguagem_primaria = node['primaryLanguage']
        #se linguagem primary (primaryLanguage) for igual a Python entao escreve no csv
        if linguagem_primaria == {'name':'Python'}:

            writer.writerow(node)
            conta_repositorios_python += 1
            print(f"arquivos encontrados {node['name']} {conta_repositorios_python}")

      

print("Execucao encerrada!")
