import pandas as pd
from pyscopus import Scopus
from models import Author, Author_Fullname
from app import db

key = 'a984477cf9a275a464a4c083b80ae499'

scopus = Scopus(key)
result = scopus.search_author("AF-ID (60105103)", count=2000, view='COMPLETE')
d = result.to_dict(orient='list')
for i in range(0, len(d.get('author_id'))):
    print(i)
    author_id = d.get('author_id')[i]
    surname = d.get('surname')[i]
    given_name = d.get('given_name')[i]
    initials = d.get('initials')[i]
    document_count = d.get('document_count')[i]
    affiliation_id = d.get('affiliation_id')[i]
    author = Author(author_id=author_id, document_count=document_count, affiliation_id=affiliation_id)
    db.session.add(author)
    db.session.commit()
    author_fullname = Author_Fullname(author_id=author_id, surname=surname, given_name=given_name, initials=initials, is_preferred=1)
    db.session.add(author_fullname)
    db.session.commit()
    name_variant_list = d.get('name_variant_list')[i]
    if name_variant_list != []:
        for item in name_variant_list:
            nv_surname = item[0]
            nv_given_name = item[1]
            nv_initials = item[2]
            author_fullname = Author_Fullname(author_id=author_id, surname=nv_surname, given_name=nv_given_name, initials=nv_initials, is_preferred=0)
            db.session.add(author_fullname)
            db.session.commit()
    
    

