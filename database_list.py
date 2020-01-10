#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Genre, Film

engine = create_engine("sqlite:///films.db")
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Create dummy user

User1 = User(
    name="Atefeh Mohammadi",
    email="atefeh.mohammadi@liberation.fr",
    picture="https://www.neatorama.com/images/2014-06/mobile-relationship-manu-cornet.jpg",
)
session.add(User1)
session.commit()

genre1 = Genre(user_id=1, name="Comedy")
session.add(genre1)
session.commit()

genre2 = Genre(user_id=1, name="Sci-Fi")
session.add(genre2)
session.commit()

genre3 = Genre(user_id=1, name="Horror")
session.add(genre3)
session.commit()

genre4 = Genre(user_id=1, name="Fantasy")
session.add(genre4)
session.commit()

genre5 = Genre(user_id=1, name="Romance")
session.add(genre5)
session.commit()

genre6 = Genre(user_id=1, name="Thriller")
session.add(genre6)
session.commit()

genre7 = Genre(user_id=1, name="Drama")
session.add(genre7)
session.commit()

genre8 = Genre(user_id=1, name="Mystery")
session.add(genre8)
session.commit()

genre9 = Genre(user_id=1, name="Documentary")
session.add(genre9)
session.commit()

film1 = Film(
    user_id=1,
    title="Pleasantville",
    year=1998,
    description="Two 1990s teenagers enter a 1950s sitcom, where they influence change in the society",
    poster_image="https://m.media-amazon.com/images/M/MV5BYTRlYzk4NDktODE3Ni00YjFkLWFjYmUtNjg1MzdmYmFmOTJkXkEyXkFqcGdeQXVyMTAwMzUyOTc@._V1_.jpg",
    genre=genre1,
)
session.add(film1)
session.commit()

film2 = Film(
    user_id=1,
    title="Serial Mom",
    year=1994,
    description="A sweet mother finds herself participating in homicidal activities when she sees the occasion call for it.",
    poster_image="https://m.media-amazon.com/images/M/MV5BYjM0N2ViMzUtMTc1OS00YmEzLWE2NWYtNjU5NTY4NjRlOTI0XkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SY1000_CR0,0,670,1000_AL_.jpg",
    genre=genre1,
)
session.add(film2)
session.commit()

film3 = Film(
    user_id=1,
    title="The Last Supper",
    year=1995,
    description="A group of idealistic, but frustrated, liberals succumb to the temptation of murdering rightwing pundits for their political beliefs.",
    poster_image="https://m.media-amazon.com/images/M/MV5BZjY5MjY3MjktM2QyMy00ZTNmLWFkYTctOTVlNjljYzExNjI5XkEyXkFqcGdeQXVyNjU0NTI0Nw@@._V1_.jpg",
    genre=genre1,
)
session.add(film3)
session.commit()

film4 = Film(
    user_id=1,
    title="Donnie Darko",
    year=2001,
    description="A troubled teenager is plagued by visions of a man in a large rabbit suit who manipulates him to commit a series of crimes, after he narrowly escapes a bizarre accident.",
    poster_image="https://m.media-amazon.com/images/M/MV5BZjZlZDlkYTktMmU1My00ZDBiLWFlNjEtYTBhNjVhOTM4ZjJjXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg",
    genre=genre2,
)
session.add(film4)
session.commit()

film5 = Film(
    user_id=1,
    title="I Origins",
    year=2014,
    description="A molecular biologist and his laboratory partner uncover evidence that may fundamentally change society as we know it.",
    poster_image="https://m.media-amazon.com/images/M/MV5BMTQ0MTAwMDI1OF5BMl5BanBnXkFtZTgwNjUwMTA2MTE@._V1_SY1000_CR0,0,666,1000_AL_.jpg",
    genre=genre2,
)
session.add(film5)
session.commit()

film6 = Film(
    user_id=1,
    title="V for Vendetta",
    year=2005,
    description='In a future British tyranny, a shadowy freedom fighter, known only by the alias of "V", plots to overthrow it with the help of a young woman. ',
    poster_image="https://m.media-amazon.com/images/M/MV5BYzllMjJkODAtYjMwMi00YmNhLWFhYzAtZjZjODg5YzEwOGUwXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SY999_CR0,0,679,999_AL_.jpg",
    genre=genre2,
)
session.add(film6)
session.commit()

film7 = Film(
    user_id=1,
    title="Teeth",
    year=2007,
    description="Still a stranger to her own body, a high school student discovers she has a physical advantage when she becomes the object of male violence. ",
    poster_image="https://m.media-amazon.com/images/M/MV5BZjVjMjY4MzMtYzljNi00NDQ5LTk3NTYtNzY5NzYyY2FjZTZmXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_SY1000_CR0,0,676,1000_AL_.jpg",
    genre=genre3,
)
session.add(film7)
session.commit()

film8 = Film(
    user_id=1,
    title="Salo, or the 120 Days of Sodom",
    year=1975,
    description="In World War II Italy, four fascist libertines round up nine adolescent boys and girls and subject them to one hundred and twenty days of physical, mental and sexual torture.",
    poster_image="https://m.media-amazon.com/images/M/MV5BYTEzYTBiNWUtZDVkZS00OWYzLWEwYzAtOWJlNWM5MWU1M2Y4XkEyXkFqcGdeQXVyODc0OTEyNDU@._V1_SY1000_CR0,0,719,1000_AL_.jpg",
    genre=genre3,
)
session.add(film8)
session.commit()

film9 = Film(
    user_id=1,
    title="The Serpent and the Rainbow",
    year=1988,
    description="An anthropologist goes to Haiti after hearing rumors about a drug used by black magic practitioners to turn people into zombies. ",
    poster_image="https://m.media-amazon.com/images/M/MV5BNTM1ZDhiZmEtZmFiOS00ZTE4LTk1OTctOTBhOTFhMDBkODFjXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_.jpg",
    genre=genre3,
)
session.add(film9)
session.commit()

film10 = Film(
    user_id=1,
    title="Pan's Labyrinth",
    year=2006,
    description="In the Falangist Spain of 1944, the bookish young stepdaughter of a sadistic army officer escapes into an eerie but captivating fantasy world. ",
    poster_image="https://m.media-amazon.com/images/M/MV5BMDBjOWYyMDQtOWRmOC00MDgxLWIxM2UtMTNjYzFiN2RkYTBlXkEyXkFqcGdeQXVyMTAyOTE2ODg0._V1_SX725_CR0,0,725,999_AL_.jpg",
    genre=genre4,
)
session.add(film10)
session.commit()

film11 = Film(
    user_id=1,
    title="Ever After",
    year=1998,
    description='The Brothers Grimm arrive at the home of a wealthy Grande Dame who speaks of the many legends surrounding the fable of the cinder girl before telling the "true" story of her ancestor. ',
    poster_image="https://m.media-amazon.com/images/M/MV5BN2FhYTY5ODItOGU4OC00MTkyLTlmYTMtYjIxN2Y4MmVlMDVhXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_.jpg",
    genre=genre5,
)
session.add(film11)
session.commit()

film12 = Film(
    user_id=1,
    title="Moulin Rouge!",
    year=2001,
    description="A poet falls for a beautiful courtesan whom a jealous duke covets.",
    poster_image="https://m.media-amazon.com/images/M/MV5BMWFhYjliNjYtYjNhNS00OGExLWFhMjQtNDgwOWYyNWJiYzhmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SY1000_CR0,0,674,1000_AL_.jpg",
    genre=genre5,
)
session.add(film12)
session.commit()

film13 = Film(
    user_id=1,
    title="I Stand Alone",
    year=1998,
    description="A horse meat butcher's life and mind begins to breakdown as he lashes out against various factions of society while attempting to reconnect with his estranged daughter.",
    poster_image="https://m.media-amazon.com/images/M/MV5BMGI5MmI3YjAtYmM4NC00ODJlLTk1OWEtNTcyM2MzYmIwNzdjXkEyXkFqcGdeQXVyMjQ1MjYzOTQ@._V1_SY1000_CR0,0,666,1000_AL_.jpg",
    genre=genre6,
)
session.add(film13)
session.commit()

film14 = Film(
    user_id=1,
    title="The Skin I Live In",
    year=2011,
    description="A brilliant plastic surgeon, haunted by past tragedies, creates a type of synthetic skin that withstands any kind of damage. His guinea pig: a mysterious and volatile woman who holds the key to his obsession. ",
    poster_image="https://m.media-amazon.com/images/M/MV5BMjMwOTYyNDY4NV5BMl5BanBnXkFtZTcwNDI1ODk0Ng@@._V1_SY1000_CR0,0,669,1000_AL_.jpg",
    genre=genre6,
)
session.add(film14)
session.commit()

film15 = Film(
    user_id=1,
    title="Butterfly's Tongue",
    year=1999,
    description="A young boy develops a beautiful relationship with his teacher at the start of the Spanish Civil War",
    poster_image="https://m.media-amazon.com/images/M/MV5BZTAwNzQ1MTktZDRmMi00OTZjLWJmNjctMGM3ZTQxNjNlYTA4XkEyXkFqcGdeQXVyMTA0MjU0Ng@@._V1_SY1000_CR0,0,752,1000_AL_.jpg",
    genre=genre7,
)
session.add(film15)
session.commit()

film16 = Film(
    user_id=1,
    title="Hotel Rwanda",
    year=2004,
    description="Paul Rusesabagina was a hotel manager who housed over a thousand Tutsi refugees during their struggle against the Hutu militia in Rwanda.",
    poster_image="https://m.media-amazon.com/images/M/MV5BZGJjYmIzZmQtNWE4Yy00ZGVmLWJkZGEtMzUzNmQ4ZWFlMjRhXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_SY1000_CR0,0,677,1000_AL_.jpg",
    genre=genre7,
)
session.add(film16)
session.commit()

film17 = Film(
    user_id=1,
    title="The Fountain",
    year=2006,
    description="As a modern-day scientist, Tommy is struggling with mortality, desperately searching for the medical breakthrough that will save the life of his cancer-stricken wife, Izzi.",
    poster_image="https://m.media-amazon.com/images/M/MV5BMTU5OTczMTcxMV5BMl5BanBnXkFtZTcwNDg3MTEzMw@@._V1_SY1000_CR0,0,677,1000_AL_.jpg",
    genre=genre8,
)
session.add(film17)
session.commit()

film18 = Film(
    user_id=1,
    title="Seven",
    year=1995,
    description="Two detectives, a rookie and a veteran, hunt a serial killer who uses the seven deadly sins as his motives.",
    poster_image="https://m.media-amazon.com/images/M/MV5BOTUwODM5MTctZjczMi00OTk4LTg3NWUtNmVhMTAzNTNjYjcyXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_SY1000_CR0,0,639,1000_AL_.jpg",
    genre=genre8,
)
session.add(film18)
session.commit()

film19 = Film(
    user_id=1,
    title="The Corporation",
    year=2003,
    description="Documentary that looks at the concept of the corporation throughout recent history up to its present-day dominance.",
    poster_image="https://m.media-amazon.com/images/M/MV5BMTQxMjMzMTczM15BMl5BanBnXkFtZTcwNzg5MzUyMQ@@._V1_.jpg",
    genre=genre9,
)
session.add(film19)
session.commit()

film20 = Film(
    user_id=1,
    title="Bixa Travesty",
    year=2018,
    description="A documentary that follows Mc Linn Da Quebrada, a black trans woman, performer and activist living in impoverished Sao Paulo. Her electrifying performances (with plenty of nudity) brazenly take on Brazil's hetero-normative machismo.",
    poster_image="https://m.media-amazon.com/images/M/MV5BMDI5ODkzYTQtMzY3MS00ZjQ4LWJkMTQtYjVlMDRkNmJiOGQ2XkEyXkFqcGdeQXVyODIyOTEyMzY@._V1_.jpg",
    genre=genre9,
)
session.add(film20)
session.commit()

print "films added!"
