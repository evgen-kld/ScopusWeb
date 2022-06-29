from flask import Flask, render_template, request, make_response, send_file, flash
from pyscopus import Scopus
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import re
import io 
import datetime
from transliterate import translit
import pandas as pd 
 
# Calling DataFrame constructor 
df = pd.DataFrame() 

key = 'a984477cf9a275a464a4c083b80ae499'
scopus = Scopus(key)


app = Flask(__name__)
app.config.from_pyfile('config.py')

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)

from models import Author_Fullname, Author


def generate_report(df):
    buffer = io.BytesIO()
    writer = pd.ExcelWriter(buffer, engine='xlsxwriter')
    df.to_excel(writer, startrow = 0, merge_cells = False, sheet_name = "Sheet_1")
    workbook = writer.book
    worksheet = writer.sheets["Sheet_1"]
    format = workbook.add_format()
    format.set_bg_color('#eeeeee')
    worksheet.set_column(0,9,28)
    writer.close()
    buffer.seek(0)
    return buffer

def search(list_id):
    result = scopus.search(" or ".join([f'AU-ID({i})' for i in list_id]), count=1000, view='COMPLETE')
    d = result.to_dict(orient='list')
    return list(zip(d.get('title'), d.get('scopus_id'), d.get('authors'), d.get('cover_date'), d.get('publication_name'), d.get('volume'), d.get('page_range'))), result

def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))

def id_search(id):
    id = id.replace(' ', '')
    list_id = id.split(',')
    list_id = list(set(list_id))
    search_result, df = search(list_id) 
    list_author = []
    for i in list_id:
        author = Author_Fullname.query.filter(Author_Fullname.author_id==i, Author_Fullname.is_preferred == 1).first()
        list_author.append(author.surname)
    print(list_author)
    return search_result, list_author, list_id, df

def surname_search(surname):
    surname_list = []   
    # surname = surname.split()
    # for i in range(0, len(surname)):
    #     if i % 3 == 0:
    #         surname_list.append(surname[i])
    for i in surname.split(','):
        s = i.split()[0]
        surname_list.append(s)
    list_author = []
    list_id = []
    for i in surname_list:
        s = i.split()[0]
        if has_cyrillic(s):
            s = translit(s, language_code='ru', reversed=True)
        author = Author_Fullname.query.filter(Author_Fullname.surname==s).first()
        if author:
            list_author.append(author.surname)
            list_id.append(author.author_id)
    search_result, df = search(list_id)
    return search_result, list_author, df



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/id_author_search')
def id_author_search():
    id = request.args.get('search_id')
    if not id:
        if id == '':
            flash('Введены некоректные данные.', 'danger')
        return render_template('id_author_search.html')
    articles, list_author, list_id, df = id_search(id)
    if request.args.get('download_xlsx'):
        f = generate_report(df)
        filename = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S') + '_scopus_info.xlsx'
        return send_file(f, attachment_filename=filename, as_attachment=True)
    return render_template('id_author_search.html', articles=articles, list_author=list_author, list_id=list_id)

@app.route('/surname_author_search')
def surname_author_search():
    surname = request.args.get('surname')
    if not surname:
        if surname == '':
            flash('Введены некоректные данные.', 'danger')
        return render_template('surname_author_search.html')
    articles, list_author, df = surname_search(surname)
    if request.args.get('download_xlsx'):
        f = generate_report(df)
        filename = datetime.datetime.now().strftime('%d_%m_%Y_%H_%M_%S') + '_scopus_info.xlsx'
        return send_file(f, attachment_filename=filename, as_attachment=True)
    return render_template('surname_author_search.html', articles=articles, list_author=list_author)


