from django.shortcuts import render
from .models import LexemeDescr, Lexeme

# Create your views here.


def lexeme_list(request):
    lex = Lexeme.objects.filter().order_by('lexema')
    return render(request, 'slovnik/lexeme_list.html', {'lexemes': lex})


def show_entry(request):
    title = request.GET['title']
    result = Lexeme.objects.filter(lexema__exact=title)
    if result:
        entry = result.first()
        return render(request, 'slovnik/entry.html', {'title': entry.lexema})
    # тут должна быть страница с ошибкой: статья не найдена
    return render(request, 'slovnik/entry.html', {'title': "-"})
