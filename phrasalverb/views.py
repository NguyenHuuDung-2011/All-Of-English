from django.shortcuts import render
from django.db.models import Prefetch
from .models import *

# Create your views here.
def phrasalverb(request):
    verbs = Verb.objects.prefetch_related(
        "particles__grammars__meanings"
    )

    rows = []

    for verb in verbs:
        verb_rows = []

        for particle in verb.particles.all():
            for grammar in particle.grammars.all():
                meanings = grammar.meanings.all()

                if meanings:
                    for meaning in meanings:
                        verb_rows.append({
                            "verb": verb.word,
                            "preposition": particle.preposition,
                            "grammar": grammar.pattern,
                            "meaning": meaning.meaning,
                            "example": meaning.example,
                        })
                else:
                    verb_rows.append({
                        "verb": verb.word,
                        "preposition": particle.preposition,
                        "grammar": grammar.pattern,
                        "meaning": "",
                        "example": "",
                    })

        # gắn rowspan
        for i, row in enumerate(verb_rows):
            row["show_verb"] = (i == 0)
            row["rowspan"] = len(verb_rows)

        rows.extend(verb_rows)

    return render(request, "phrasalverb/phrasalverb.html", {
        "rows": rows
    })