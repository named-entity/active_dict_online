import logging

from flask import Flask, request, render_template
from flask_bootstrap import Bootstrap
from flask_paginate import Pagination

from pymorphy2 import MorphAnalyzer

from flaskr import service

logging.basicConfig(level="DEBUG", format="%(levelname)s: %(asctime)s %(message)s")

app = Flask(__name__, instance_relative_config=True)

bootstrap = Bootstrap(app)
morph = MorphAnalyzer()


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/search', methods=["GET", "POST"])
def search():
    if request.method == 'POST':
        results, title = service.search(request)
        if not results:
            return render_template("search.html", message="По запросу ничего не найдено!")
        return render_template('results.html', results=results, title=title)
    if request.method == 'GET':
        return render_template('search.html')


@app.route('/slovnik', defaults={'page': 1})
@app.route('/content/page/<int:page>')
def slovnik(page):
    results, total, per_page = service.get_slovnik(page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4', href='/content/page/{0}',
                            display_msg="")
    return render_template('slovnik.html', results=results, pagination=pagination)


@app.route('/content/<word_id>')
def word_page(word_id):
    results = service.get_word_page(word_id)
    return render_template('word.html', results=results)
