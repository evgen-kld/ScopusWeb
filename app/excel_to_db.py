import xlrd
from app import db
from models import Author
#открываем файл
rb = xlrd.open_workbook("database/authors.xls", formatting_info=True)

#выбираем активный лист
sheet = rb.sheet_by_index(0)

for i in range(0, 1735):
    author_id = sheet.row_values(i)[1]
    name = sheet.row_values(i)[2]
    document_count = int(sheet.row_values(i)[3])
    affiliation = sheet.row_values(i)[4]
    affiliation_id = sheet.row_values(i)[5]
    author = Author(author_id=author_id, name=name, document_count=document_count, affiliation=affiliation, affiliation_id=affiliation_id)
    try:
        db.session.add(author)
        db.session.commit()
        print(i)
    except:
        print('db error', i)
