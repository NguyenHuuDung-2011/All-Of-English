from django.test import TestCase
from django.urls import reverse
from .models import *

# Create your tests here.
class ModelTest(TestCase):
    def setUp(self):
        self.verb = Verb.objects.create(word="first")
        self.particle = Particle.objects.create(verb=self.verb, preposition="second")
        self.grammar = GrammarPattern.objects.create(particle=self.particle, pattern="first + second")

    def test_verb_creation(self):
        verb = Verb.objects.get(word="first")
        self.assertEqual(verb.word, "first")

    def test_particle_creation(self):
        particle = Particle.objects.get(preposition="second")
        self.assertEqual(particle.preposition, "second")
        self.assertEqual(particle.verb, self.verb)

    def test_grammar_pattern_creation(self):
        grammar = GrammarPattern.objects.get(pattern="first + second")
        self.assertEqual(grammar.pattern, "first + second")
        self.assertEqual(grammar.particle, self.particle)

class ViewTest(TestCase):
    def setUp(self):
        self.verb = Verb.objects.create(word="first")
        self.particle = Particle.objects.create(verb=self.verb, preposition="second")
        self.grammar = GrammarPattern.objects.create(particle=self.particle, pattern="first + second")

    def test_view_url_exists_at_proper_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_by_name(self):
        response = self.client.get(reverse('phrasalverb'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'phrasalverb/phrasalverb.html')