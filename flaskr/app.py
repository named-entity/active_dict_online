# import configparser
# import os
import sqlite3

from flask import Flask, request, render_template, g
# from flaskext.mysql import MySQL
from flask_bootstrap import Bootstrap

from flask_paginate import Pagination, get_page_parameter

# import pymysql
from pymorphy2 import MorphAnalyzer

DATABASE = 'AS1.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def get_words():
    cur = get_db().cursor()
    cur.execute("SELECT id FROM dictionary")
    total_words = len(cur.fetchall())
    return total_words


app = Flask(__name__, instance_relative_config=True)

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
        pomety = request.form.get('tag', '')
        text = request.form.get('text', '')
        where_clauses = []
        results = []
        if title:
            title_condition = []
            title_condition.append(
                    # "lexema_lemmas LIKE '%%%s%%" % l
                "lexeme_lemmas='%s'" % title
            )
            where_clauses.append('(' + '  OR '.join(title_condition) + ')')
        if pomety:
            pomety_condition = []
            for p in pomety.split():
                p = p.strip('.')
                pomety_condition.append(
                    "text LIKE '%%%s.%%'" % p
                )
            where_clauses.append('(' + '  OR '.join(pomety_condition) + ')')
        if tags:
            tags_condition = []
            for t in tags.split(','):
                tags_condition.append(
                    # "part_of_speech LIKE '%%%s%%'" % t
                    "pos LIKE '%%%s%%'" % t
                )
            where_clauses.append('(' + ' OR '.join(tags_condition) + ')')
        if text:
            text_condition = []
            for t in text.split():
                text_condition.append(
                    "text_lemmas LIKE '%%%s%%'" % t
                )
            where_clauses.append('(' + ' OR '.join(text_condition) + ')')

        if not where_clauses:
            return render_template("search.html", message="Пустой запрос!")
        query = "SELECT * FROM for_search WHERE %s" % " AND ".join(where_clauses)
        print(query)
        cur.execute(query)
        for i in cur.fetchall():
            # results.append(i['html'].decode())
            results.append(i[-1])
        return render_template('results.html', results=results, title=title)
    if request.method == 'GET':
        return render_template('search.html')


@app.route('/slovnik', defaults={'page': 1})
@app.route('/content/page/<int:page>')
def slovnik(page):
    # connection = mysql.connect()
    # cur = connection.cursor(pymysql.cursors.DictCursor)
    cur = get_db().cursor()
    per_page = 50
    start = page * per_page - per_page
    cur.execute("SELECT id, lexeme FROM dictionary LIMIT %d OFFSET %d" % (per_page, start))
    results = [{'id': l[0], 'lexeme': l[1]} for l in cur.fetchall()]
    pagination = Pagination(page=page, per_page=per_page, total=get_words(),
                            css_framework='bootstrap4', href='/content/page/{0}',
                            display_msg="")
    return render_template('slovnik.html', results=results, pagination=pagination)


@app.route('/content/<word_id>')
def word_page(word_id):
    cur = get_db().cursor()
    cur.execute("SELECT id, html FROM dictionary WHERE id='%s'" % word_id)
    results = [{'id': l[0], 'html': l[1]} for l in cur.fetchall()]
    return render_template('word.html', results=results)
