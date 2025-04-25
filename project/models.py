# File: models.py
# Author: João Pedro Rocha (jprocha@bu.edu), 04/15/2025
# Description: models file used to define all four models used in this application

from django.db import models
from enum import Enum
from django.core.validators import MinValueValidator, MaxValueValidator
from enum import IntEnum
from django.core.exceptions import ValidationError
from django.urls import reverse

# This enum class has all the possible pokemon types in gen 1
class PokemonType(IntEnum):
    NORMAL = 0
    FIRE = 1
    WATER = 2
    ELECTRIC = 3
    GRASS = 4
    ICE = 5
    FIGHTING = 6
    POISON = 7
    GROUND = 8
    FLYING = 9
    PSYCHIC = 10
    BUG = 11
    ROCK = 12
    GHOST = 13
    DRAGON = 14

# three possible move categories
class CategoryType(IntEnum):
    PHYSICAL = 0
    SPECIAL = 1
    STATUS = 2
    

# Max and min values for pokemon stats
STAT_MIN = 0
STAT_MAX = 255


class Trainer(models.Model):
    '''Encapsulate the idea of a Trainer in pokemon.'''

    # data attributes of the trainer model:
    first_name = models.TextField(blank=True)
    last_name = models.TextField(blank=True)
    pokemon_region = models.TextField(blank=True)
    pokemon_town = models.TextField(blank=True)
    trainer_image_url = models.URLField(blank=True)

    rival = models.ForeignKey("Trainer", on_delete=models.SET_NULL, blank=True, null=True) 
    
    def __str__(self):
        '''Return a string representation of this Article object.'''
        return f'Trainer {self.first_name} {self.last_name}'
    
    # Return all the pokemon caught by this trainer
    def get_caught_pokemon(self):
        return HasCaughtPokemon.objects.filter(trainer=self)
    
    # return absolute url to this trainer instance
    def get_absolute_url(self):
        '''Return the URL to display one instance of this model.'''
        return reverse('show_trainer', kwargs={'pk': self.pk})
    
    # Checks whether the team is full or not
    def is_team_full(self):
        caught_mons = self.get_caught_pokemon()
        num = len(caught_mons.filter(in_team=True))
        if (num >= 6):
            return True
        else:
            return False
    
    # Cheks whether all the caught pokemon for this trainer are currently in his team 
    def all_pokemon_in_team(self):
        caught_mons = self.get_caught_pokemon()
        num = len(caught_mons.filter(in_team=True))
        # print(num)
        # print(len(caught_mons))
        if (num == len(caught_mons)):
            return True
        else:
            return False


def pokemon_type_choices():
    # returns tuple list of values & labels for a pokemon type
    return [(ptype.value, ptype.name.title()) for ptype in PokemonType]

def category_type_choices():
    # returns tuple list of values & labels for a move category
    return [(ptype.value, ptype.name.title()) for ptype in CategoryType]


class Pokemon_Species(models.Model):
    '''Encapsulate the idea of a pokemon species in pokemon.'''
    name = models.CharField(max_length=20)
    pokemon_image_url = models.URLField(blank=True)

    type1 = models.IntegerField(choices=pokemon_type_choices())
    type2 = models.IntegerField(choices=pokemon_type_choices(), blank=True, null=True)  # Optional second type
    
    
    move1 = models.ForeignKey("Move", on_delete=models.SET_NULL, blank=True, null=True, related_name='move1') 
    move2 = models.ForeignKey("Move", on_delete=models.SET_NULL, blank=True, null=True, related_name='move2') 
    move3 = models.ForeignKey("Move", on_delete=models.SET_NULL, blank=True, null=True, related_name='move3') 
    move4 = models.ForeignKey("Move", on_delete=models.SET_NULL, blank=True, null=True, related_name='move4') 

    # Base Stats
    hit_points = models.IntegerField(validators=[MinValueValidator(STAT_MIN), MaxValueValidator(STAT_MAX)])
    attack = models.IntegerField(validators=[MinValueValidator(STAT_MIN), MaxValueValidator(STAT_MAX)])
    special = models.IntegerField(validators=[MinValueValidator(STAT_MIN), MaxValueValidator(STAT_MAX)])
    defense = models.IntegerField(validators=[MinValueValidator(STAT_MIN), MaxValueValidator(STAT_MAX)])
    accuracy = models.IntegerField(validators=[MinValueValidator(STAT_MIN), MaxValueValidator(STAT_MAX)])
    evasiveness = models.IntegerField(validators=[MinValueValidator(STAT_MIN), MaxValueValidator(STAT_MAX)])
    speed = models.IntegerField(validators=[MinValueValidator(STAT_MIN), MaxValueValidator(STAT_MAX)])

    def __str__(self):
        return f"{self.name}" 
    
    def get_absolute_url(self):
        '''Return the URL to display one instance of this model.'''
        return reverse('show_species', kwargs={'pk': self.pk})
    

class Move(models.Model):
     '''Encapsulate the idea of a move in pokemon.'''
     name = models.CharField(max_length=20)
     description = models.TextField()

     type = models.IntegerField(choices=pokemon_type_choices())

     category = models.IntegerField(choices=category_type_choices())

     power = models.IntegerField()
     accuracy = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
     powerpoints = models.IntegerField(validators=[MinValueValidator(5), MaxValueValidator(64)])

     def __str__(self):
        return f"{self.name}"


class HasCaughtPokemon(models.Model):
    '''Encapsulate the idea of a a pokemon species caught by a certain trainer in pokemon.'''

    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    species = models.ForeignKey(Pokemon_Species, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, blank=True)
    level = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])

    # In trainer team/party -> only 6 pokemon cuaght by this trainer should have this on
    in_team = models.BooleanField(default=False)
    
    # Current Stats
    hit_points = models.IntegerField(validators=[MinValueValidator(STAT_MIN), MaxValueValidator(STAT_MAX)])
    attack = models.IntegerField(validators=[MinValueValidator(STAT_MIN), MaxValueValidator(STAT_MAX)])
    special = models.IntegerField(validators=[MinValueValidator(STAT_MIN), MaxValueValidator(STAT_MAX)])
    defense = models.IntegerField(validators=[MinValueValidator(STAT_MIN), MaxValueValidator(STAT_MAX)])
    accuracy = models.IntegerField(validators=[MinValueValidator(STAT_MIN), MaxValueValidator(STAT_MAX)])
    evasiveness = models.IntegerField(validators=[MinValueValidator(STAT_MIN), MaxValueValidator(STAT_MAX)])
    speed = models.IntegerField(validators=[MinValueValidator(STAT_MIN), MaxValueValidator(STAT_MAX)])

    def __str__(self):
        return f"{self.species} caught by {self.trainer}"
    
    def get_absolute_url(self):
        '''Return the URL to display one instance of this model.'''
        return reverse('show_caught', kwargs={'pk': self.pk})
    
    def get_highest_stat(self):
        ''' Get current highest stat (argmax) '''
        stats = {"hp":self.hit_points, "attack":self.attack, "special":self.special, "defense":self.defense, "accuracy":self.accuracy, "evasiveness":self.evasiveness, "speed":self.speed}
        max = -1
        stat_highest = ""

        for stat in stats:
            if stats[stat] > max:
                max = stats[stat]
                stat_highest = stat

        
        return stat_highest




   
