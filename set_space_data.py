from app import db, models

models.SalesBySize.query.delete()
models.Taxonomy.query.delete()
db.session.commit()


space_types = [
        'Property',
        'Go',
        'Community Chest',
        'Tax',
        'Chance',
        'Jail',
        'Free Parking',
        'Go To Jail'
        ]

[db.session.add(models.SpaceType(space_type)) for space_type in space_types]

odd_spaces = [
        {'name': 'Go', 'location': 0, 'type': 'Go'},
        {'name': 'Community Chest #1', 'location': 2, 'type': 'Community Chest'},
        {'name': 'Chance #1', 'location': 7, 'type': 'Chance'},
        {'name': 'Jail', 'location': 10, 'type': 'Jail'},
        {'name': 'Community Chest #2', 'location': 17, 'type': 'Community Chest'},
        {'name': 'Free Parking', 'location': 20, 'type': 'Free Parking'},
        {'name': 'Chance #2', 'location': 22, 'type': 'Chance'},
        {'name': 'Got to Jail', 'location': 30, 'type': 'Go to Jail'},
        {'name': 'Community Chest #3', 'location': 33, 'type': 'Community Chest'},
        {'name': 'Chance #3', 'location': 36, 'type': 'Chance'}
        ]
[db.session.add(models.Space(location=space['location'],
    type=space['type'], name=space['name'])) for space in odd_spaces]

taxes = [
        {'name': 'Income Tax', 'location': 4},
        {'name': 'Luxury Tax', 'location': 38}
        ]
[db.session.add(models.Tax(location=tax['location'],
    name=tax['name'])) for tax in taxes]


p = models.Property(name='Mediterranean Ave.', location=1, price=60,
        color_group='Purple') 
db.session.add(p)

p = models.Property(name='Baltic Ave.',location=3,
    price=60,color_group='Purple')
db.session.add(p)

p = models.Property(name='Reading Railroad',location=5,
    price=200, color_group='Railroad')
db.session.add(p)

p = models.Property(name='Oriental Ave.',location=6,
        price=100,color_group='Light-Green')
db.session.add(p)

p = models.Property(name='Vermont Ave.',location=8,
    price=100, color_group='Light-Green')
db.session.add(p)

p = models.Property(name='Connecticut Ave.',location=9,
    price=120, color_group='Light-Green')
db.session.add(p)

p = models.Property(name='St. Charles Place',location=11,
    price=140, color_group='Violet')
db.session.add(p)

p = models.Property(name='Electric Company',location=12,
    price=150, color_group='Utilities')
db.session.add(p)

p = models.Property(name='States Ave.',location=13,
    price=140, color_group='Violet')
db.session.add(p)

p = models.Property(name='Virginia Ave.',location=14,
    price=160, color_group='Violet')
db.session.add(p)

p = models.Property(name='St. James Place',location=16,
    price=180, color_group='Orange')
db.session.add(p)

p = models.Property(name='Tennessee Ave.',location=18,
    price=180, color_group='Orange')
db.session.add(p)

p = models.Property(name='New York Ave.',location=19,
    price=200, color_group='Orange')
db.session.add(p)

p = models.Property(name='Kentucky Ave.',location=21,
    price=220, color_group='Red')
db.session.add(p)

p = models.Property(name='Indiana Ave.',location=23,
    price=220, color_group='Red')
db.session.add(p)

p = models.Property(name='Illinois Ave.',location=24,
    price=240, color_group='Red')
db.session.add(p)

p = models.Property(name='B. & O. Railroad', location=25,
    price=200, color_group='Railroad')
db.session.add(p)


p = models.Property(name='Atlantic Ave.',location=26,
    price=260, color_group='Yellow')
db.session.add(p)

p = models.Property(name='Ventnor Ave.',location=27,
    price=260, color_group='Yellow')
db.session.add(p)

p = models.Property(name='Water Works',location=28,
    price=150, color_group='Utilities')
db.session.add(p)

p = models.Property(name='Marvin Gardens',location=29,
    price=280, color_group='Yellow')
db.session.add(p)

p = models.Property(name='Pacific Ave.',location=31,
    price=300, color_group='Dark-Green')
db.session.add(p)

p = models.Property(name='North Carolina Ave.',location=32,
    price=300, color_group='Dark-Green')
db.session.add(p)

p = models.Property(name='Pennsylvania Ave.',location=34,
    price=320, color_group='Dark-Green')
db.session.add(p)

p = models.Property(name='Short Line Railroad', location=35,
    price=200, color_group='Railroad')
db.session.add(p)

p = models.Property(name='Park Place',location=37,
    price=350, color_group='Dark-Blue')
db.session.add(p)

p = models.Property(name='Boardwalk',location=39,
    price=400, color_group='Dark-Blue')
db.session.add(p)

db.session.commit()
