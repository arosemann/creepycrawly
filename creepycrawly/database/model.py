# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        model.py
# Purpose:     Reflects all tables of the current database model.
#
# Author:      Elisabeth Rosemann
#
# Created:     15.08.2015
# Copyright:   (c) scintillation e.U. 2015
# -------------------------------------------------------------------------------
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, ForeignKey, Sequence, BIGINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class ToStringMixin:
    """ SQLAlchemy Mixin to have a toString method for all database model classes. """

    def __getValueAsString(self, key):
        return getattr(self, key).__str__()

    def __isPrivateOrEmptyValue(self, key):
        return key.startswith('_') and getattr(self, key)

    def __str__(self):
        return ' - '.join(key + ":'" + self.__getValueAsString(key) + "'" for key in self.__dict__ if
                          not self.__isPrivateOrEmptyValue(key))

    def __repr__(self):
        return str(self)


# Each class represents a database table. In order to generate the database, please use the database_setup.py file.


class Stock(ToStringMixin, Base):
    __tablename__ = 'share'
    id = Column(BIGINT, Sequence('share_seq'), primary_key=True, nullable=False)
    name = Column('name', String(250))
    isin = Column('isin', String(250))
    shareType = Column('share_type', String(250))  # shares, funds, bonds
    dividend = Column('dividend', Boolean)  # indicates only if there's a dividend or not
    currency = Column('currency', String(3))  # currency code, e.g. EUR, USD, ...
    industry = Column('industry', String(200))  # industry type, e.g. mining, banking, ....


# Maps to PDF chapter I. Customer Information
class ShareHistory(ToStringMixin, Base):
    __tablename__ = 'share_history'
    id = Column(Integer, Sequence('share_history_seq'), primary_key=True, nullable=False)
    shareId = Column('share_id', ForeignKey('share.id', name='fk_share'))
    share = relationship('Share', lazy='joined')

    currDate = Column('current_date', DateTime)  # date of the entry
    openValue = Column('open_value', Float)  # open value on that day
    closeValue = Column('close_value', Float)  # close value on that day
    tradeVolume = Column('trade_volume', Float)  # trade volume on that day

    # key performance indicators
    peg = Column('peg', Float)  # PEG = Price-Earning to Growth-Ratio = Kurs-Gewinn-Wachstums-Verhältnis
    equityRatio = Column('equity_ratio', Float)  # = Eigenkapitalquote
    growth = Column('growth', Float)  # growth in %
    priceBookRatio = Column('price_book_ratio', Float)  # = Preis-Buchwert-Verhältnis
    per = Column('per', Float)  # PER = Price-Earnings-Ratio (PER) = P/E Ratio = KGV = Kurs-Gewinn-Verhältnis
