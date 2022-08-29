import json
import psycopg2
import pandas as pd
import anvil.server

"""anvil.server.connect('O7JRPIBIIGOEAOJOYBHUQAB3-FKG3AT46IPCV55OY')"""

anvil.server.connect('server_HESCYNF3RFWGIVTJF4RMIUZL-3OWQ7IJAYB3TUII7')

"""anvil.server.connect('server_LWZSPSXVA3I7FIKVGBUQ7GRX-TUFTWN7L4RPEW7MB')"""

def connection():

  conn = psycopg2.connect(
         user = 'postgres',
         password = 'admin',
         host = 'localhost',
         port = '5432',
         database = 'postgres'
  )

  return conn

@anvil.server.callable
def genres(param = 'WHERE nsfw = false'):

  query = 'SELECT DISTINCT genres FROM japanimator.animes ' + param
  print(query)

  try:
    conn = connection()
    cur = conn.cursor()
    cur.execute(query)
    df = pd.DataFrame(cur.fetchall(), columns = ['genres'])
    genres = sorted(list(set([x for xs in df['genres'].apply(lambda x: eval(x)) for x in xs])))
    cur.close()
    conn.close()
    print('La connexion PostgreSQL est fermée')

  except (Exception, psycopg2.Error) as error :
    print ('Erreur lors de la connexion à PostgreSQL', error)

  return genres

@anvil.server.callable
def elements(param = ''):

  query = 'SELECT COUNT(*) FROM japanimator.animes ' + param
  print(query)

  try:
    conn = connection()
    cur = conn.cursor()
    cur.execute(query)
    elements = cur.fetchall()
    cur.close()
    conn.close()
    print('La connexion PostgreSQL est fermée')

  except (Exception, psycopg2.Error) as error :
    print ('Erreur lors de la connexion à PostgreSQL', error)

  return elements[0][0]

@anvil.server.callable
def fetch_anime_db(param = ''):

  query = 'SELECT * FROM japanimator.animes ' + param
  print(query)

  try:
    conn = connection()
    cur = conn.cursor()

    #Récupération des colonnes
    cur.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'animes' ORDER BY ordinal_position ASC")
    columns = [item for t in cur.fetchall() for item in t]

    #Création du DataFrame
    cur.execute(query)
    df = pd.DataFrame(cur.fetchall(), columns = columns)

    #fermeture de la connexion à la base de données
    cur.close()
    conn.close()
    print('La connexion PostgreSQL est fermée')

  except (Exception, psycopg2.Error) as error :
    print ('Erreur lors de la connexion à PostgreSQL', error)

  result = df.to_json(orient='records')
  parsed = json.loads(result)

  print(parsed)

  return parsed

anvil.server.wait_forever()