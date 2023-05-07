from django.db import models

# Create your models here.

class Quran_Suras(models.Model):
    sura_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.sura_name

class Quran_text_all(models.Model):
    sura = models.IntegerField()
    aya = models.IntegerField()
    text = models.TextField()

    def __str__(self):
        return str(self.sura)

class Quran_text_simple(models.Model):
    sura = models.IntegerField()
    aya = models.IntegerField()
    text = models.TextField()

    def __str__(self):
        return str(self.sura)
