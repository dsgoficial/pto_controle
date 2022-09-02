# -*- coding: utf-8 -*-
"""
/***************************************************************************
Name                 : Atualiza banco de dados de ponto de controle
Description          : Atualiza a situação dos pontos medidos no banco de dados de ponto de controle
Version              : 1.0
copyright            : 1ºCGEO / DSG
reference:
 ***************************************************************************/
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from pathlib import Path
import psycopg2

class HandleCreateDB():
    def __init__(self, servidor, porta, nome_bd, usuario, senha):
        self.server = servidor
        self.port = porta
        self.bdname = nome_bd
        self.user = usuario
        self.password = senha
        conn_string = "host='{0}' port='{1}' dbname='postgres' user='{2}' password='{3}'".format(
            servidor, porta, usuario, senha)
        self.conn = psycopg2.connect(conn_string)
        self.cursor = self.conn.cursor()
        self.conn.autocommit = True

    def create(self):
        self.cursor.execute(u"""
                    CREATE DATABASE {}
                """.format(self.bdname))
        sqlPath = Path(__file__).parent / 'new_db.sql'
        new_conn_str = "host='{0}' port='{1}' dbname='{2}' user='{3}' password='{4}'".format(
            self.server, self.port, self.bdname, self.user, self.password)
        new_conn = psycopg2.connect(new_conn_str)
        cursor = new_conn.cursor()
        with open(sqlPath, 'rb') as sql:
            file = sql.read()
            cursor.execute(file)
            new_conn.commit()