from asyncio.windows_events import NULL
import json
import psycopg2
import pandas as pd
import anvil.server
from sklearn.preprocessing import RobustScaler
from sklearn.neighbors import KNeighborsClassifier

anvil.server.connect('server_HESCYNF3RFWGIVTJF4RMIUZL-3OWQ7IJAYB3TUII7')

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
def column(column, param = 'WHERE nsfw = false'):
  query = 'SELECT DISTINCT ' + column + ' FROM japanimator.animes ' + param
  print(query)
  try:
    conn = connection()
    cur = conn.cursor()
    cur.execute(query)
    df = pd.DataFrame(cur.fetchall(), columns = [column])
    if column == 'genres':
      result = sorted(list(set([x for xs in df[column].apply(lambda x: eval(x)) for x in xs])))
    else :
      result = sorted(list(df[column]))
    cur.close()
    conn.close()
    print('La connexion PostgreSQL est fermée')
  except (Exception, psycopg2.Error) as error:
    print ('Erreur lors de la connexion à PostgreSQL', error)
  return result

@anvil.server.callable
def elements(param = ''):
  query = 'SELECT COUNT(*) FROM japanimator.animes ' + param
  print(query)
  try:
    conn = connection()
    cur = conn.cursor()
    cur.execute(query)
    elements = cur.fetchone()
    cur.close()
    conn.close()
    print('La connexion PostgreSQL est fermée')
  except (Exception, psycopg2.Error) as error :
    print ('Erreur lors de la connexion à PostgreSQL', error)
  return elements[0]

@anvil.server.callable
def fetch_anime_db(param = '', recom = False):
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
  if recom == False:
    result = df.to_json(orient = 'records', date_format = 'iso')
    parsed = json.loads(result)
    print(parsed)
    return parsed
  else:
    return df

@anvil.server.callable
def recommandation(anime):
  df = fetch_anime_db('Order by id ASC', True)
  genre = sorted(list(set([x for xs in df['genres'].apply(lambda x: eval(x)) for x in xs])))
  cols_to_scale = ['mean', 'num_scoring_users', 'num_episodes', 'num_list_users', 'popularity', 'num_favorites', 'rank']
  df[cols_to_scale] = df[cols_to_scale].fillna(0)
  df['genres'] = df['genres'].apply(lambda x: eval(x))
  df['genres'] = df['genres'].apply(lambda x: ','.join(x))
  genres_dummies = df['genres'].str.get_dummies(',').astype(bool)
  df_new = pd.concat([df, genres_dummies], axis = 1)
  #create and fit scaler
  scaler = RobustScaler()
  scaler.fit(df_new[cols_to_scale])
  #scale selected data
  df_new[cols_to_scale] = scaler.transform(df_new[cols_to_scale])
  y = df_new['title']
  X = df_new[genre + ['mean', 'num_scoring_users']]
  meta_df_model_KNN = KNeighborsClassifier(n_neighbors=11, weights='distance')
  meta_df_model_KNN.fit(X, y)
  reco_id = list(df[df.index.isin(meta_df_model_KNN.kneighbors(df_new[df_new.id == anime][genre + ['mean', 'num_scoring_users']])[1][0])]['id'])
  reco_id.remove(anime)
  return fetch_anime_db('WHERE ID IN (' + str(reco_id).strip('[]') + ')')

@anvil.server.callable
def upsert_anime(insert, anime_id , title, media_type, mean, num_scoring_users, status, num_episodes, start_date, end_date, source, num_list_users, popularity, num_favorites, rank, average_episode_duration, rating, start_season_year, start_season_season, broadcast_day_of_the_week, broadcast_start_time, genres, studios, synopsis, nsfw, main_picture_medium, main_picture_large, alternative_titles_en, alternative_titles_ja, alternative_titles_synonyms):
  q_update = f"""UPDATE japanimator.animes
              SET
                title = '{title}',
                media_type = '{media_type}',
                mean = {mean},
                num_scoring_users = {num_scoring_users},
                status = '{status}',
                num_episodes = {num_episodes},
                start_date = '{start_date}',
                end_date = '{end_date}',
                source = '{source}',
                num_list_users = {num_list_users},
                popularity = {popularity},
                num_favorites = {num_favorites},
                rank = {rank},
                average_episode_duration = '{average_episode_duration}',
                rating = '{rating}',
                start_season_year = {start_season_year},
                start_season_season = '{start_season_season}',
                broadcast_day_of_the_week = '{broadcast_day_of_the_week}',
                broadcast_start_time = '{broadcast_start_time}',
                genres = '{genres}',
                studios = '{studios}',
                synopsis = '{synopsis}',
                nsfw = '{nsfw}',
                updated_at = NOW(),
                main_picture_medium = '{main_picture_medium}',
                main_picture_large = '{main_picture_large}',
                alternative_titles_en = '{alternative_titles_en}',
                alternative_titles_ja = '{alternative_titles_ja}',
                alternative_titles_synonyms = '{alternative_titles_synonyms}'
              WHERE id = {str(anime_id)}
              """
  q_insert = f"""INSERT INTO japanimator.animes
              (
                title,
                media_type,
                mean,
                num_scoring_users,
                status,
                num_episodes,
                start_date,
                end_date,
                source,
                num_list_users,
                popularity,
                num_favorites,
                rank,
                average_episode_duration,
                rating,
                start_season_year,
                start_season_season,
                broadcast_day_of_the_week,
                broadcast_start_time,
                genres,
                studios,
                synopsis,
                nsfw,
                created_at,
                main_picture_medium,
                main_picture_large,
                alternative_titles_en,
                alternative_titles_ja,
                alternative_titles_synonyms
              )
              VALUES
              (
                '{title}',
                '{media_type}',
                {mean},
                {num_scoring_users},
                '{status}',
                {num_episodes},
                '{start_date}',
                '{end_date}',
                '{source}',
                {num_list_users},
                {popularity},
                {num_favorites},
                {rank},
                '{average_episode_duration}',
                '{rating}',
                {start_season_year},
                '{start_season_season}',
                '{broadcast_day_of_the_week}',
                '{broadcast_start_time}',
                '{genres}',
                '{studios}',
                '{synopsis}',
                {nsfw},
                NOW(),
                '{main_picture_medium}',
                '{main_picture_large}',
                '{alternative_titles_en}',
                '{alternative_titles_ja}',
                '{alternative_titles_synonyms}'
              ) RETURNING id;
              """
  try:
    conn = connection()
    cur = conn.cursor()
    if insert:
      cur.execute(q_insert.replace("'None'", 'null'))
      last_id = cur.fetchone()[0]
    else:
      cur.execute(q_update.replace("'None'", 'null'))
    conn.commit()
    cur.close()
    conn.close()
  except (Exception, psycopg2.Error) as error :
    print ('Erreur lors de la connexion à PostgreSQL', error)
  return last_id

@anvil.server.callable
def delete_anime(id):
  query = 'DELETE FROM japanimator.animes WHERE id = ' + str(id)
  print(query)
  try:
    conn = connection()
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()
  except (Exception, psycopg2.Error) as error :
    print ('Erreur lors de la connexion à PostgreSQL', error)

anvil.server.wait_forever()