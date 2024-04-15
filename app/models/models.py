from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.db import Base


class WordFile(Base):
    __tablename__ = 'word_file'
    left_id = Column(ForeignKey('files.id'), primary_key=True)
    right_id = Column(ForeignKey('words.id'), primary_key=True)
    tf = Column(Float(precision=10, decimal_return_scale=6, asdecimal=True),
                default=1.0)
    word = relationship('Word', back_populates='files')
    file = relationship('File', back_populates='words')


class Word(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    word = Column(String(254), unique=True, nullable=False)
    idf = Column(Float(precision=10, decimal_return_scale=6, asdecimal=True))
    files = relationship('WordFile', back_populates='word', lazy='selectin')

    def __repr__(self):
        return f'{self.word[:30]}'

    def dict(self):
        return dict(word=self.word)


class File(Base):
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(254), unique=True, nullable=False)
    words_qty = Column(Integer)
    uploaded_at = Column(DateTime(timezone=True), default=datetime.now)
    words = relationship('WordFile', back_populates='file', lazy='selectin')

    def __str__(self):
        return self.name[:30]

    def dict(self):
        return dict(name=self.name)
