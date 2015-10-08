title: Построение связей в SQLAlchemy
date: 2015-03-04 9:30:00
status: published
tags: sqlalchemy, orm

Связи в sqlachemy бывают 4-х видов:

- OTM (one-to-many) - один к многим
- MTO (many-to-one) - многие к одному
- OTO (one-to-one) - один к одному
- MTM (many-to-many) - многие к многим

Релизация этих связей:

### OTM :

Для указания связи OTM, создается колонка с ForeignKey в дочернем классе. При этом сама связь (relationship()) объявляется в Родителе. Для того что-бы получить по Ребенку Родителя, необходимо указать в relationship, свойство backref.

    :::python
    class Parent(Base):
		__tablename__ = 'parents'
		id = Column(Integer, primary_key=True)
		child = relationship("Child", backfer='parents')

    class Child(Base):
		__tablename__ = 'childrens'
		id = Column(Integer, primary_key=True)
		parent_id = Column(Integer, ForeignKey('parents.id')

### MTO :

Здесь построение отношения похоже на предыдущий, только ForeignKey указывается в Родителе, вместе с relationship()

	:::python
	class Parent(Base):
		__tablename__ = 'parents'
		id = Column(Integer, primary_key=True)
		child_id = Column(Integer, ForeignKey('childs.id'))
		child = relationship("Child", backref='parents')

		
	class Child(Base):
		__tablename__ = 'childs'
		id = Column(Integer, primary_key=True)

### OTO :

Со связью один-к-одному вообще всё просто, это та же связь один-к-многим, только в relationship добавляется еще одно свойство, которое вытягивает из другой таблицы только 1 элемент

	:::python
	class Parent(Base):
		__tablename__ = 'parents'
		id = Column(Integer, primary_key=True)
		child = relationship("Child", uselist=False, backref='parents')

	class Child(Base):
		__tablename__ = 'childs'
		id = Column(Integer, primary_key=True)
		parent = Column(Integer, ForegnKey(parents.id))

Или 

	:::python 
	class Parent(Base):
		__tablename__ = 'parents'
		id = Column(Integer, primary_key=True)
		child_id = Column(Integer, ForeignKey('childs.id'))
		child = relationship("Child", backref=backref("parents", uselist=False))

	class Child(Base):
		__tablename__ = 'childs'
		id = Column(Integer, primary_key=True)


### MTM :

Данная связь реализуется при помощи вспомагательной ассоциативной таблицы, которую необходимо создать до создания связанных таблиц.

	:::python
	association_table = Table('association', Base.metadata,
    	Column('left_id', Integer, ForeignKey('left.id')),
    	Column('right_id', Integer, ForeignKey('right.id'))

    class Parent(Base):
    __tablename__ = 'left'
    id = Column(Integer, primary_key=True)
    children = relationship("Child",
                    secondary=association_table)

	class Child(Base):
    	__tablename__ = 'right'
    	id = Column(Integer, primary_key=True)


стырено из официальной документации с вольным переводом [оф.документация](http://docs.sqlalchemy.org/en/rel_0_9/orm/basic_relationships.html)
