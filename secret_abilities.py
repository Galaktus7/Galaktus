import special_abilities
import utils
import telebot
import config
import random
import Item_list

types = telebot.types
bot = telebot.TeleBot(config.token)

secret_abilities = []
def check_ability(player):
    for ability in secret_abilities:
        if ability.condition_1 in player.abilities and ability.condition_2 in player.abilities:
            player.abilities.append(ability)
            ability.aquare(ability, player)
            bot.send_message(player.chat_id, 'Sizga sirli qobiliyat berildi - ' + ability.name)


class Warlock(special_abilities.Ability):

    condition_1 = special_abilities.Necromancer
    condition_2 = special_abilities.Ritual
    name = 'Qora Sexrgar'
    info = 'Har bir o`lgan odam uchun 1tadan jon olasiz.'
    MeleeOnly = False
    RangeOnly = False
    TeamOnly = True

    def aquare(self, user):
        user.deadplayers = []
        user.corpsecounter = 0

    def special_first(self, user):
        if len(user.deadplayers) < len(user.team.deadplayers) + len(utils.get_other_team(user).deadplayers):
            print('O`lik aniqlandi! ')
            deadbodies = len(user.team.deadplayers) + len(utils.get_other_team(user).deadplayers) - len(user.deadplayers)
            user.deadplayers = list(user.team.deadplayers) + list(utils.get_other_team(user).deadplayers)

            while deadbodies != 0:
                deadbodies -= 1
                user.corpsecounter += 1
        if user.corpsecounter > 0 and Item_list.explode_corpse not in user.itemlist:
            user.itemlist.append(Item_list.explode_corpse)

class Regeneration(special_abilities.Ability):
    condition_1 = special_abilities.Sturdy.Sturdy
    condition_2 = special_abilities.Armorer
    name = 'Regeneratsiya.'
    info = 'Sizda 33% ehtimollikda zarbdan so`ng 1 jonni tiklab olishiz mumkin.'
    MeleeOnly = False
    RangeOnly = False
    TeamOnly = True

    def special_end(self, user):
        if user.Losthp and random.randint(1,6) == 1:
            user.hp += 1
            user.fight.string.add(u'\U00002757' + "|" + user.name + ' 1 jonini tiklab oldi.')


class Bloodlust(special_abilities.Ability):
    condition_1 = special_abilities.Berserk
    condition_2 = special_abilities.Sadist
    name = 'Qonxo`rlik.'
    info = 'Joni yarimdan kam bo`lgan o`yinchilarga ko`proq aniqlikda hujum qila olasiz.'
    MeleeOnly = False
    RangeOnly = False
    TeamOnly = False

    def special_first(self, user):
        if user.target is not None:
            if user.target.maxhp//user.hp >= 2:
                user.tempaccuracy += 1

secret_abilities.append(Warlock)
secret_abilities.append(Regeneration)
secret_abilities.append(Bloodlust)
