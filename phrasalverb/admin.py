from django.contrib import admin
from .models import *

# Register your models here.
class ParticleInline(admin.TabularInline):
    model = Particle
    extra = 1


@admin.register(Verb)
class VerbAdmin(admin.ModelAdmin):
    inlines = [ParticleInline]
    search_fields = ['word']


@admin.register(Particle)
class ParticleAdmin(admin.ModelAdmin):
    list_display = ['verb', 'preposition']
    list_filter = ['verb']


class MeaningInline(admin.TabularInline):
    model = Meaning
    extra = 1


@admin.register(GrammarPattern)
class GrammarPatternAdmin(admin.ModelAdmin):
    inlines = [MeaningInline]
    list_display = ['pattern', 'particle']


admin.site.register(Meaning)