import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Table, Date, DateTime
from sqlalchemy import  create_engine, update
from sqlalchemy.orm import relationship, backref, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import Engine
from sqlalchemy import event


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# Creamos la base de datos
engine = create_engine('sqlite:///gardengrowenia.db')
# Creamos el mapeo para conectar con la base de datos
Session = sessionmaker(bind=engine)
session = Session()  
Base = declarative_base()


""" class Mantenimiento(Base):
    __tablename__ = "Mantenimiento"

    id_mantenimiento = Column(Integer, primary_key=True)
    nombre = Column(String(80), nullable=False)
    descripcion = Column(String(500))
    fecha_mantenimiento = Column(Date, nullable=False)

    def add_mantenimiento(self):
        session.add(self)
        session.commit()

    def get_mantenimientos(self):
        return session.query(Mantenimiento).all()

    def get_mantenimiento_by_id(self, id):
        mantenimiento = session.query(Mantenimiento).filter(Mantenimiento.id_mantenimiento == id).first()
        return mantenimiento

    def delete_mantenimiento(self, id):
        session.query(Mantenimiento).filter(Mantenimiento.id_mantenimiento == id).delete()
        session.commit() """


class Huerto(Base):
    __tablename__ = "Huerto"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(80), nullable=False)
    descripcion = Column(String(500), nullable=False)
    fecha_plantacion = Column(Date, nullable=False)
    created_at = Column(Date, nullable=False, default=datetime.date.today())
    plantas = relationship("Planta", back_populates="huertos", cascade="all, delete-orphan", passive_deletes=True)

    def get_huertos(self):
        return session.query(Huerto).all()        

    def get_huerto_by_id(self, id):
        huerto = session.query(Huerto).filter(Huerto.id == id).first()
        return huerto

    def add_huerto(self):
        session.add(self)
        session.commit()

    def update_huerto(self):
        session.query(Huerto).\
                filter(Huerto.id == self.id).\
                update({
                        "nombre": self.nombre,
                        "descripcion": self.descripcion,
                        "fecha_plantacion": self.fecha_plantacion,
                        "created_at": self.created_at
                        })
        session.commit()

    def delete_huerto(self, id):
        session.query(Huerto).filter(Huerto.id == id).delete()
        session.commit()

class Planta(Base):
    __tablename__ = "Planta"

    id = Column(Integer, primary_key=True)
    nombre = Column(String(80), nullable=False)
    anotaciones = Column(String(500), nullable=False)
    fecha_plantacion = Column(Date, nullable=False)
    created_at = Column(Date(), nullable=False, default=datetime.date.today())
    huerto_id = Column(Integer, ForeignKey("Huerto.id", ondelete="cascade"), nullable=False)
    huertos = relationship("Huerto", back_populates="plantas")

    def __repr__(self):
        return self.nombre, self.fecha_plantacion

    def get_plantas(self, id_huerto):
        return session.query(Planta).filter(Planta.huerto_id == id_huerto).all()

    def get_planta_by_id(self, id):
        planta = session.query(Planta).filter(Planta.id == id).first()
        return planta

    def add_planta(self):
        session.add(self)
        session.commit()

    def update_planta(self):
        session.query(Planta).\
                filter(Planta.id == self.id).\
                update({
                        "nombre": self.nombre,
                        "anotaciones": self.anotaciones,
                        "fecha_plantacion": self.fecha_plantacion,
                        })
        session.commit()

    def delete_planta(self, id):
        session.query(Planta).filter(Planta.id == id).delete()
        session.commit()


class DatabaseUtils:

    def create_database(self):
        Base.metadata.create_all(engine)
    
    def delete_database(self):
        Base.metadata.drop_all(engine)


Base.metadata.create_all(engine)

 # Para crear nuevo elemento:
#nueva_fila = Planta(nombre="Nombre de la planta", anotaciones="Bla, bla, bla", fecha_plantacion=datetime(2020, 2, 21).date(), created_at=datetime.today())

if __name__ == '__main__':
    # Creamos la sesión para comunicarnos con la base de datos
    Session = sessionmaker(bind=engine)
    session = Session()
    
    Base.metadata.create_all(engine)