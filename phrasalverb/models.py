from django.db import models
import re

# Create your models here.
class Verb(models.Model):
    word = models.CharField(max_length=100, unique=True, db_index=True)

    class Meta:
        ordering = ['word']

    def __str__(self):
        return self.word
    
    def save(self, *args, **kwargs):
        self.word = self.word.strip().lower()
        super().save(*args, **kwargs)


class Particle(models.Model):
    verb = models.ForeignKey(
        Verb,
        on_delete=models.CASCADE,
        related_name='particles'
    )

    preposition = models.CharField(max_length=50, db_index=True)

    class Meta:
        ordering = ['preposition']
        constraints = [
            models.UniqueConstraint(fields=['verb', 'preposition'], name='unique_verb_preposition')
        ]

    def __str__(self):
        return f"{self.verb.word} {self.preposition}"

    def save(self, *args, **kwargs):
        self.preposition = self.preposition.strip().lower()
        super().save(*args, **kwargs)


class GrammarPattern(models.Model):
    particle = models.ForeignKey(
        Particle,
        on_delete=models.CASCADE,
        related_name='grammars'
    )

    pattern = models.CharField(
        max_length=200,
        help_text='vd: take up + noun'
    )

    class Meta:
        ordering = ['pattern']
        constraints = [
            models.UniqueConstraint(fields=['particle', 'pattern'], name='unique_particle_pattern')
        ]

    def __str__(self):
        return self.pattern
    
    def save(self, *args, **kwargs):
        pattern = self.pattern.strip().lower()

        pattern = re.sub(r'\s+', ' ', pattern)
        pattern = re.sub(r'\s*\+\s*', ' + ', pattern)

        self.pattern = pattern.strip()

        super().save(*args, **kwargs)


class Meaning(models.Model):
    grammar = models.ForeignKey(
        GrammarPattern,
        on_delete=models.CASCADE,
        related_name='meanings'
    )

    meaning = models.TextField()
    example = models.TextField(blank=True)

    def __str__(self):
        return self.meaning[:50]
    
    def save(self, *args, **kwargs):
        self.meaning = self.meaning.strip()
        self.example = self.example.strip()
        super().save(*args, **kwargs)