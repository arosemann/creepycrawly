# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        database_setup.py
# Purpose:     Helper class to set up the database with the help of SQLAlchemy.
#              http://www.sqlalchemy.org/
#
# Author:      Elisabeth Rosemann
#
# Created:     15.08.2015
# Copyright:   (c) scintillation e.U. 2015
# -------------------------------------------------------------------------------
import configparser

from sqlalchemy import create_engine

from creepycrawly.database.model import Base


# Required packages:
#  SQLAlchemy: http://www.sqlalchemy.org/
#  MySQL Connector (MySQLdb): https://dev.mysql.com/downloads/connector/python/ - install the zip
#                 "mysql-connector-python-2.0.4.zip" with "python setup.py build" and "python setup.py install")
class DatabaseSetup:
    def __init__(self):
        self.engine = None

    def __dropDatabase(self):
        """ Private method. Drops all database tables."""
        print("Dropping all database tables.")
        Base.metadata.drop_all(self.engine)
        print("Successfully dropped all database tables.")

    def __createDatabase(self):
        """ Private method.Creates all database tables according to the definition in the model.py file. If no prefix,
        creates the whole database. """
        print("Creating all database tables.")
        Base.metadata.create_all(self.engine)
        print("Successfully created all database tables.")

    def setupDatabase(self, option, configFile):
        """ Public method. The only method required to be called from the outside to set up the database.
        :param option: String specifying which option should be executed
        :type option: str or unicode or None
        :param configFile: location of the properties file
        :type configFile: str or unicode or None
        :rtype: None """
        config = configparser.ConfigParser()
        config.read(configFile)
        dbString = 'mysql+mysqlconnector://%s:%s@%s/%s' % (config["creepy-crawly-db"]["user"],
                                                           config["creepy-crawly-db"]["pwd"],
                                                           config["creepy-crawly-db"]["host"],
                                                           config["creepy-crawly-db"]["schema"])
        self.engine = create_engine(dbString, echo=False)
        if len(option) == 0:
            print(u'Option has to be one of the following: [all|drop_db|create_db]')
        else:
            if option == u'all':
                self.__dropDatabase()
                self.__createDatabase()
            elif option == u'drop_db':
                self.__dropDatabase()
            elif option == u'create_db':
                self.__createDatabase()
            else:
                print(u'Invalid option. Please use one of the following: all, drop_create_db, drop_db, create_lookups')


if __name__ == '__main__':
    setup = DatabaseSetup()
    setup.setupDatabase("all", '../properties.cfg')

