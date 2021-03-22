# import configparser
# import os
import sqlite3

from flask import Flask, request, render_template, g
# from flaskext.mysql import MySQL
from flask_bootstrap import Bootstrap

from flask_paginate import Pagination, get_page_parameter

# import pymysql
from pymorphy2 import MorphAnalyzer

app = Flask(__name__, instance_relative_config=True)

DATABASE = 'AS1.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# cparser = configparser.RawConfigParser()
# cparser.read('%s/.my.cnf' % os.environ["HOME"])
# app.config.from_mapping(
#     DATABASE=cparser.get('db', 'name'),
#     MYSQL_DATABASE_DB=cparser.get('db', 'name'),
#     MYSQL_DATABASE_HOST=cparser.get('db', 'address'),
#     MYSQL_DATABASE_USER=cparser.get('db', 'user'),
#     MYSQL_DATABASE_PASSWORD=cparser.get('db', 'password').strip('"'),
# )
# mysql = MySQL(app)

bootstrap = Bootstrap(app)
morph = MorphAnalyzer()


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/search', methods=["GET", "POST"])
def search():
    # connection = mysql.connect()
    # cur = connection.cursor(pymysql.cursors.DictCursor)
    cur = get_db().cursor()
    if request.method == 'POST':
        title = request.form.get('title', '')
        tags = request.form.get('pos', '')
        text = request.form.get('text', '')
        where_clauses = []
        results = []
        if title:
            for a in morph.parse(title):
                l = a.normal_form
                where_clauses.append(
                    # "lexema_lemmas LIKE '%%%s%%" % l
                    "lexeme_lemmas LIKE '%%%s%%'" % l
                )

        if tags:
            for t in tags.split(','):
                where_clauses.append(
                    # "part_of_speech LIKE '%%%s%%'" % t
                    "pos LIKE '%%%s%%'" % t
                )
        if text:
            for t in text.split():
                where_clauses.append(
                    "text_lemmas LIKE '%%%s%%'" % t
                )
        if not where_clauses:
            return render_template("search.html", message="Пустой запрос!")
        query = "SELECT * FROM for_search WHERE %s" % " or ".join(where_clauses)
        print(query)
        cur.execute(query)
        for i in cur.fetchall():
            # results.append(i['html'].decode())
            results.append(i[-1])
        print(len(results))
        cur.execute("SELECT lexeme_lemmas FROM for_search")
        print(cur.fetchall())
        return render_template('results.html', results=results, title=title)
    if request.method == 'GET':
        return render_template('search.html')


@app.route('/slovnik', defaults={'page': 1})
@app.route('/content/page/<int:page>')
def slovnik(page):
    # connection = mysql.connect()
    # cur = connection.cursor(pymysql.cursors.DictCursor)
    cur = get_db().cursor()
    cur.execute("SELECT id FROM dictionary")
    total = len(cur.fetchall())
    per_page = 50
    start = page * per_page - per_page
    cur.execute("SELECT * FROM dictionary LIMIT %d OFFSET %d" % (per_page, start))
    results = [{'id': l[0], 'lexeme': l[1]} for l in cur.fetchall()]
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4', href='/content/page/{0}',
                            display_msg="")
    return render_template('slovnik.html', results=results, pagination=pagination)

