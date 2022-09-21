import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime
import bcrypt

##############################
############ Main ############
##############################

# Get current user row from users data table.
@anvil.server.callable
def get_user():
  return anvil.users.get_user()

# Check current user access (administrator or not)
#@anvil.server.callable
def check_admin(user):
  if user is None or not user['admin']:
    raise Exception("Accès non autorisé") 

######################################
############ User Profile ############
######################################

# Set avatar on current user row into users data table.
@anvil.server.callable
def set_avatar(user, img):
  if app_tables.users.has_row(user):
    user['avatar'] = img
  else:
    raise Exception("Compte inexistant")

# Set new password on current user row into users data table.
@anvil.server.callable
def set_password(user, new_password):
  if app_tables.users.has_row(user):
    user['password_hash'] = bcrypt.hashpw(
      new_password.encode(),
      bcrypt.gensalt()
    ).decode()
    user['confirmed_email'] = True
  else:
    raise Exception("Compte inexistant")  

# Delete row of current user from users data table.
@anvil.server.callable
def delete_account(user):
  table = app_tables.contacts.search(email = user['email'])
  if table != None:
    for row in table:
      row['email'] = 'utilisateur supprimé'
  if app_tables.users.has_row(user):
    user.delete()
  else:
    raise Exception("Compte inexistant")
    
#################################
############ Contact ############
#################################

# Get the last id.
#@anvil.server.callable
def get_last_row_id(rows):
  if len(rows):
    last_id = rows[0]['id'] + 1
  else:
    last_id = 1
  return last_id

# create new email into contacts data table.
@anvil.server.callable
def create_email(user, category, topic, message):
  rows = app_tables.contacts.search(tables.order_by(
    'id',
    ascending = False
  ))
  app_tables.contacts.add_row(
    id = get_last_row_id(rows),
    email = user['email'],
    created = datetime.now(),
    year = datetime.now().year,
    category = category.lower(),
    topic = topic.strip(),
    message = message.strip(),
    status = False
  )

###############################
############ Inbox ############
###############################

# Update row of current email into contacts data table.
@anvil.server.callable
def update_email(user, email, category, topic, message, status):
  check_admin(user = user)
  if app_tables.contacts.has_row(email):
    email.update(
      category = category.lower(),
      topic = topic.strip(),
      message = message.strip(),
      status = status
    )
  else:
    raise Exception("Email inexistant")

# Get row of current email id from contacts data table.
@anvil.server.callable
def get_email_by_id(user, i):
  check_admin(user = user)
  return app_tables.contacts.get(id = int(i))

# Delete row of current email from contacts data table.
@anvil.server.callable
def delete_email(user, email):
  check_admin(user = user)
  if app_tables.contacts.has_row(email):
    email.delete()
  else:
    raise Exception("Email inexistant")
    
##############################
############ Tags ############
##############################

# Create new tag name into tags data table.
@anvil.server.callable
def create_tag(user, name):
  check_admin(user = user)
  if app_tables.tags.get(name = name) == None:
    return app_tables.tags.add_row(
      name = name.strip().lower(),
      parent = 'sans categorie',
      description = 'default',
      color = 'white'
    )
  else:
    raise Exception("Tag existant")
    
# Update row of current tag into tags data table.
@anvil.server.callable
def update_tag(user, tag, parent, description, color):
  check_admin(user = user)
  if app_tables.tags.has_row(tag):
    tag.update(
      parent = parent.strip().lower(),
      description = description.strip(),
      color = color.strip().lower()
    )
  else:
    raise Exception("Tag inexistant")
    
# Delete row of current tag from tags data table.
@anvil.server.callable
def delete_tag(user, tag):
  check_admin(user = user)
  table = None
  if tag['parent'] == 'contact':
    table = app_tables.contacts.search(category = tag['name'])
    if table != None:
      for row in table:
        row['category'] = 'sans categorie'
  if tag['parent'] == 'tag':
    table = app_tables.tags.search(parent = tag['name'])
    if table != None:
      for row in table:
        row['parent'] = 'sans categorie'
  if app_tables.tags.has_row(tag):
    tag.delete()
  else:
    raise Exception("Tag inexistant")

#########################################
############ User Management ############
#########################################

# Update row of current user into users data table.
@anvil.server.callable
def update_user(user, row, confirmed, enabled, admin):
  check_admin(user = user)
  if app_tables.users.has_row(row):
    row.update(
      confirmed_email = confirmed,
      enabled = enabled,
      admin = admin,
    )
  else:
    raise Exception("Compte inexistant")

@anvil.server.callable
def get_anime_by_id(i):
  return app_tables.contacts.client_writable().get(id = int(i))

@anvil.server.callable
def get_article_by_id(i):
  return app_tables.news.client_writable().get(id = int(i))
    
#################################
############ Article ############
#################################

@anvil.server.callable
def create_new_article():
  rows = app_tables.news.search(tables.order_by('id',ascending=False))
  
  if len(rows):
    last_id = rows[0]['id']  + 1
  else:
    last_id = 1
  
  return app_tables.news.client_writable().add_row(
    id=last_id,
    genre='genre',
    title=f'Article {last_id}', created=datetime.now(),
    body="""#Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam vulputate massa vitae diam rhoncus, non dictum ante efficitur. Vivamus varius mattis dignissim. Praesent sed metus dui. Vestibulum et augue varius, efficitur est pulvinar, suscipit quam. Vestibulum id magna enim. Etiam interdum arcu viverra malesuada lobortis. Sed porttitor a enim vel congue. Ut vestibulum id risus ac posuere. Nam in lacinia ligula. Sed commodo justo id elit venenatis pretium. Phasellus dictum nunc vel arcu feugiat pellentesque. Aenean vitae turpis placerat, imperdiet lectus at, efficitur erat."""
  )