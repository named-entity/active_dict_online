import logging
import dao


def search(request):
    title = request.form.get('title', '')
    poses = request.form.get('pos', '')
    tags = request.form.get('tag', '')
    text = request.form.get('text', '')
    where_clauses = []
    search_values = []
    results = []
    if title:
        logging.debug("title request value: '%s'", title)
        title_condition = "lexeme_lemmas=?"
        search_values.append(title.lower())
        where_clauses.append(title_condition)
    if tags:
        logging.debug("tags request values: '%s'", tags)
        poses_condition = []
        for p in tags.split():
            p = p.strip('.')
            poses_condition.append("tags LIKE '%' || ? || '.%'")
            search_values.append(p.lower())
        where_clauses.append('(' + '  OR '.join(poses_condition) + ')')
    if poses:
        logging.debug("POSes request values: '%s'", poses)
        poses_condition = []
        for t in poses.split(','):
            poses_condition.append("pos LIKE '%' || ? || '%'")
            search_values.append(t)
        where_clauses.append('(' + ' OR '.join(poses_condition) + ')')
    if text:
        logging.debug("text request values: '%s'", text)
        text_condition = []
        for t in text.split():
            text_condition.append("text_lemmas LIKE '%' || ? || '%'")
            search_values.append(t)
        where_clauses.append('(' + ' OR '.join(text_condition) + ')')

    if where_clauses:
        query = "SELECT new_html FROM for_search WHERE %s" % " AND ".join(where_clauses)
        results = dao.find_all_html_by_sql(query, search_values)
    return results, title


def get_slovnik(page):
    per_page = 50
    start = page * per_page - per_page
    results = dao.find_all_lexemes(per_page, start)
    total = dao.get_words()
    return results, total, per_page


def get_word_page(word_id):
    logging.debug("requested word_id: '%s'", word_id)
    return dao.find_all_html_by_word_id(word_id)
