# coding: utf8

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
#########################################################################

if request.env.web2py_runtime_gae:            # if running on Google App Engine
    db = DAL('gae')                           # connect to Google BigTable
    session.connect(request, response, db=db) # and store sessions and tickets there
    ### or use the following lines to store sessions in Memcache
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db=MEMDB(Client())
else:                                         # else use a normal relational database
    db = DAL('sqlite://sqlite.storage')       # if not, use SQLite or other DB
## if no need for session
# session.forget()

from gluon.tools import *
auth=Auth(globals(),db)                      # authentication/authorization
auth.settings.hmac_key='sha512:32b6c31c-d643-408f-8415-e7e07efb91e0'
auth.define_tables()                         # creates all needed tables
crud=Crud(globals(),db)                      # for CRUD helpers using auth
service=Service(globals())                   # for json, xml, jsonrpc, xmlrpc, amfrpc

# crud.settings.auth=auth                      # enforces authorization on crud
# mail=Mail()                                  # mailer
# mail.settings.server='smtp.gmail.com:587'    # your SMTP server
# mail.settings.sender='you@gmail.com'         # your email
# mail.settings.login='username:password'      # your credentials or None
# auth.settings.mailer=mail                    # for user email verification
# auth.settings.registration_requires_verification = True
# auth.settings.registration_requires_approval = True
# auth.messages.verify_email = \
#  'Click on the link http://.../user/verify_email/%(key)s to verify your email'

# options for select fields

GENRE_CHOICES = (
    'Sci-Fi/Fantasy',
    'Textbook',
    'Religious',
    'Self-Help',
    'Comic',
    'Poetry',
    'Action/Adventure',
    'General',
    'Writing Reference',
    'General Reference',
    'Cookbook'
)

CLASSIF_CHOICES = [
    'Adult',
    'Young Adult',
    'Child - Chapter',
    'Child - Picture']
    
AGELVL_CHOICES = [
    'Adult',
    'Young Adult',
    'Intermediate',
    'Primary']

COND_CHOICES = [
    'Excellent',
    'Good',
    'Fine',
    'Poor']

#table definitions

db.define_table("books",
    Field("isbn", "string", label="ISBN", length=20, default=None),
    Field("author", "string", length=50, notnull=True, default=None),
    Field("title", "string", length=100, notnull=True, default=None),
    Field("illustrator", "string", length=50, default=None),
    Field("series", "string", length=100, default=None),
    Field("publisher", "string", length=30, default=None),
    Field("genre", "string", length=20, notnull=True, default=None, requires=IS_IN_SET(GENRE_CHOICES)),
    Field("classification", "string", notnull=True, default=None, requires=IS_IN_SET(CLASSIF_CHOICES)),
    Field("age_level", "string", notnull=True, default=None, requires=IS_IN_SET(AGELVL_CHOICES)),
    Field("copyright", "integer", length=4, default=None),
    Field("edition", "integer", length=2, default=None),
    Field("num_copies", "integer", label='No. of Copies', notnull=True, default=1),
    Field("awards", "string", length=50, default=None),
    Field("language", "string", length=20, notnull=True, default=None),
    Field("condition", "string", length=10, notnull=True, default=None, requires=IS_IN_SET(COND_CHOICES)),
    Field("signed", "boolean", label='Signed', notnull=True, default=False),
    Field("antique", "boolean", label='Antique', notnull=True, default=False),
    Field("comments", "text", default=None))

from datetime import datetime

db.define_table("loans",
    Field("id_books", db.books),
    Field("name", "string", length=50, notnull=True, default=None),
    Field("lndate", "date", label='Date of Loan:', notnull=True, default=datetime.now()),
    Field("comments", "text", default=None))

# foreign key relation for loans and books.
db.loans.id_books.requires=IS_IN_DB( db, 'books.id', ' %(isbn)s %(author)s %(title)s')