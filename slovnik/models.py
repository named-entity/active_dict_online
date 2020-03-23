from django.conf import settings
from django.db import models
from django.utils import timezone


class Lexeme(models.Model):
    lexema = models.TextField()
    part_of_speech = models.TextField()
    gram = models.TextField()
    synopsis = models.TextField()

    def publish(self):
        self.save()

    def __str__(self):
        return "\t".join((self.lexema, self.part_of_speech, self.gram, self.synopsis))


class LexemeDescr(models.Model):
    lexema_id = models.ForeignKey(Lexeme, on_delete=models.CASCADE)
    num = models.CharField(max_length=50)
    stylistic = models.TextField()
    examples = models.TextField()
    definition = models.TextField()
    comment_to_def = models.TextField()
    subcategorization = models.TextField()
    comment_to_subc = models.TextField()
    constr = models.TextField()
    comp = models.TextField()
    illustrations = models.TextField()
    lexical = models.TextField()
    phraseology = models.TextField()
