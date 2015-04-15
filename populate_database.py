from app import db, models
import csv

models.Sales.query.delete()
models.Taxonomy.query.delete()
db.session.commit()


def insert_from_csv(fname, model, batch_size=None):
    with open(fname) as csvfile:
        r = csv.DictReader(csvfile)
        count = 0

        for row in r:
            for key in row:
                row[key] = row[key].decode(encoding='Utf-8')
    
            db.session.add(model(**row))
            
            count += 1
            if batch_size is not None and count % batch_size == 0:
                db.session.commit()
    
    db.session.commit()


if __name__ == '__main__':
    insert_from_csv('backend-taxonomy.csv', models.Taxonomy)
    insert_from_csv('sales by size.csv', models.Sales)
