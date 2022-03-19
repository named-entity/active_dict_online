import sqlite3
from typing import List, Dict

from flask import g
import logging

DATABASE = 'AS1.db'


def _get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def get_words():
    cur = _get_db().cursor()
    query = "SELECT id FROM dictionary"
    logging.debug("executing query: '%s'", query)
    cur.execute(query)
    total_words = len(cur.fetchall())
    return total_words


def find_all_html_by_sql(query: str, search_values: List[str]) -> List[str]:
    cur = _get_db().cursor()
    logging.debug("executing query: '%s'", query)
    cur.execute(query, search_values)
    return [i[0] for i in cur.fetchall()]


def find_all_lexemes(max_results: int, start: int) -> List[Dict[str, str]]:
    cur = _get_db().cursor()
    query = "SELECT id, lexeme FROM dictionary LIMIT ? OFFSET ?"
    logging.debug("executing query: '%s'", query)
    cur.execute(query, [max_results, start])
    return [{'id': l[0], 'lexeme': l[1]} for l in cur.fetchall()]


def find_all_html_by_word_id(word_id: str) -> List[Dict[str, str]]:
    cur = _get_db().cursor()
    query = "SELECT id, new_html FROM dictionary WHERE id=?"
    logging.debug("executing query: '%s'", query)
    cur.execute(query, [word_id])
    return [{'id': l[0], 'new_html': l[1]} for l in cur.fetchall()]
