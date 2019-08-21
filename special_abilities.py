import utils
import config
import telebot
import Item_list
import random
import sys
import Weapon_list


bot = telebot.TeleBot(config.token)
types = telebot.types

abilities = []
usual_abilities = []
unique_abilities =[]

class Ability(object):
    effect = None
    name = None
    info = None

    def aquareonce(self, user):
        pass

    def aquare(self, user):
        pass

    def fightstart(self, user):
        pass

    def special_used(self, user):
        pass

    def special_first(self, user):
        pass

    def special_second(self, user):
        pass

    def special_last(self, user):
        pass

    def special_end(self, user):
        pass

    def stop(self, user):
        pass

    def onhit(self, n, user):
        return n

    def onhitdesc(self, d, user):
        return d

    def ondamage(self, source, target, damage, type):
        pass

sys.path.insert(0, '/abilities')
from abilities import Sturdy


class Sadist(Ability):
    name = 'Sadist'
    info = 'Raqibingiz yo`qotgan har bir jon uchun siz energiya olasiz.'
    MeleeOnly = False
    RangeOnly = False
    TeamOnly = False

    def special_end(self, user):
        n = 0
        if user.target is not None and user.target.damagetaken > 0 and user.target.team.damagetaken != 0 \
                and user.team.damagetaken <= user.target.team.damagetaken:
            n = user.target.hploss
        user.energy += n
        if n != 0:
            user.fight.string.add(u'\U0001F603' + "|" + "Sadist " + user.name + ' oldi ' + str(n) + ' energiya.')


class Gasmask(Ability):
    name = 'Gazgi qarshi Niqob'
    info = 'Sizga zaxarli gazlar ta`sir etmaydi. Olovga qarshiligingiz ortgan.'
    MeleeOnly = False
    RangeOnly = False
    TeamOnly = False

    def aquare(self, user):
        user.passive.append('Gasmask')

    def special_first(self, user):
        if user.firecounter > 0:
            if user.offfire > user.fight.round:
                user.offfire > user.fight.round


class Target(Ability):
    name = 'Nishon'
    info = 'O`q otuvchi quroldan nishonga tegish ehtimolligi siz uchun ortadi.'
    MeleeOnly = False
    RangeOnly = True
    TeamOnly = False

    def aquare(self, user):
        if not user.weapon.Melee:
            user.accuracy += 2


class Strength(Ability):
    name = 'Biseps'
    info = 'Siz 33% ehtimollikda ikki karrali zarb bera olasiz.'
    MeleeOnly = True
    RangeOnly = False
    TeamOnly = False

    def aquare(self, user):
        if user.weapon.Melee:
            user.Crit = False

    def onhit(self, n, user):
        if random.randint(1, 3) == 2 and user.weapon.Melee:
            print('Crit')
            n *= 2
            user.Crit = True
        return n

    def onhitdesc(self, d, user):
        if user.Crit and user.weapon.Melee:
            d += u'\U00002757'
        return d

    def special_end(self, user):
        if user.weapon.Melee:
            user.Crit = False


class Shields(Ability):
    name = 'Shitlar Generatori'
    info = 'Siz 3ta yurishdan so`ng yangilanadigan qalqonni olasiz.'
    MeleeOnly = False
    RangeOnly = False
    TeamOnly = False

    def aquare(self, user):
        user.shieldrefresh = 3

    def special_end(self, user):
        if user.Alive:
            if Item_list.shieldg not in user.itemlist and user.shieldrefresh == user.fight.round:
                user.itemlist.append(Item_list.shieldg)
                bot.send_message(user.chat_id, '"Shit" qobiliyati yangilandi!')
            else:
                if user.shieldrefresh - user.fight.round > 0:
                    bot.send_message(user.chat_id, '"Shit" qobiliyati '
                                                   + str(user.shieldrefresh - user.fight.round) + " ta yurishdan so`ng yangilanadi.")


class Revenge(Ability):
    name = 'Qast'
    info = 'Agarda do`stingiz o`lsa sizning kuchingiz ortadi.'
    MeleeOnly = False
    RangeOnly = False
    TeamOnly = True

    def aquare(self, user):
        user.deadteammates = []
        user.revengecounter = 2

    def special_first(self, user):
        print('O`lik bormi?')
        if user.deadteammates != user.team.deadplayers:
            print('O`lik aniqlandi! ')
            deadbodies = len(user.team.deadplayers) - len(user.deadteammates)
            user.deadteammates = list(user.team.deadplayers)
            counter = 1

            while deadbodies != 0:
                if user.revengecounter != 0:
                    user.fight.string.add(u'\U0001F621' + "|" + 'Harakatsiz '
                                          + user.team.deadplayers[-counter].name +
                                          ' tanasini ko`rib, ' + user.name + ' g`azabga to`ldi! + 1 jon va zarb ortdi.')
                    deadbodies -= 1
                    user.bonusdamage += 1
                    user.hp += 1
                    counter += 1
                    user.revengecounter -= 1
                else:
                    break
        else:
            print('O`liklar!')


class Hoarder(Ability):
    name = 'Saqlovchi'
    info = 'Siz 2taga ko`proq jihoz ola olasiz.'
    MeleeOnly = False
    RangeOnly = False
    TeamOnly = False

    def aquare(self, user):
        counter = 2
        defcounter = 0
        while defcounter < counter:
            item = Item_list.itemlist[random.randint(0, len(Item_list.itemlist)-1)]
            if item not in user.itemlist:
                user.itemlist.append(item)
                defcounter += 1


class Mentalist(Ability):
    name = 'Kuzatuvchi'
    info = 'Dushmanlariz haqidagi ma`lumotni ola olasiz!'
    MeleeOnly = False
    RangeOnly = False
    TeamOnly = False

    def aquare(self, user):
        if not user.weapon.Melee:
            user.accuracy += 1
        user.mentalrefresh = 0
        user.itemlist.append(Item_list.mental)

    def special_end(self, user):
        print('Kuzatuv ' + user.name)
        if user.Alive:
            if user.mentalrefresh == user.fight.round:
                user.itemlist.append(Item_list.mental)
                bot.send_message(user.chat_id, '"Kuzatish" qobiliyati yangilandi!')
            elif user.mentalrefresh - user.fight.round > 0:
                bot.send_message(user.chat_id, '"Kuzatish" qobiliyati '
                                               + str(user.mentalrefresh - user.fight.round) + " yurishdan so`ng yangilanadi.")


class Hypnosyser(Ability):
    name = 'Gipnozchi'
    info = 'Siz raqib nishonini o`z do`stiga tomon o`zgartirishiz mumkin! Albatta agar u shu yurishda otsa.'
    MeleeOnly = False
    RangeOnly = False
    TeamOnly = False

    def aquare(self, user):
        user.hypnosysrefresh = 0
        user.itemlist.append(Item_list.hypnosys)

    def special_end(self, user):
        print('Гипноз ' + user.name)
        if user.Alive:
            if user.hypnosysrefresh == user.fight.round:
                user.itemlist.append(Item_list.hypnosys)
                bot.send_message(user.chat_id, '"Gipnoz" qobiliyati yangilandi!')
            elif user.hypnosysrefresh - user.fight.round > 0:
                bot.send_message(user.chat_id, '"Gipnoz" qobiliyati'
                                               + str(user.hypnosysrefresh - user.fight.round) + " yurishdan so`ng yangilanadi.")



class Armorer(Ability):
    name = 'Qattiq Bosh'
    info = 'Sizdan bir vaqtda bir nechta jonni ketkazib bo`lmaydi.'
    MeleeOnly = False
    RangeOnly = False
    TeamOnly = False
    def aquare(self, user):
        user.toughness += 4


class West(Ability):
    name = 'Bronjilet'
    info = '30% ehtimollikda 1ta zarbni qaytara olasiz.'
    MeleeOnly = False
    RangeOnly = False
    TeamOnly = False

    def aquare(self, user):
        user.armor += 1
        user.armorchance += 30


class Piromant(Ability):
    name = 'Piroman'
    info = 'Har bir yonayotgan odam uchun 1ta qo`shimcha energiya olasiz.'
    MeleeOnly = False
    RangeOnly = False
    TeamOnly = False

    def special_last(self, user):
        fire = False
        user.bonusdamage = 0
        for p in user.fight.activeplayers:
            if p.firecounter > 0:
                fire = True
                user.bonusdamage += 1
        for p in user.fight.aiplayers:
            if p.firecounter > 0:
                fire = True
                user.bonusdamage += p.firecounter
        if fire is True:
            user.fight.string.add(u'\U0001F47A' + '| Piroman ' + user.name + ' bonusga +'
                                  + str(user.bonusdamage) + " zarb kuchi olayabdi.")
        else:
            pass


class Berserk(Ability):
    name = 'Bersker'
    info = 'Sizning maksimum energiyangiz 2ga kamayadi. U har bir yetishmayotgan jon uchun oshadi. Sizda 1ta jon qolmaguncha' \
           ' qo`shimcha zarba berasiz.'
    MeleeOnly = True
    RangeOnly = False
    TeamOnly = False

    def aquare(self, user):
        user.energy -= 2
        user.maxenergy -= 2
        user.berserkenergy = user.maxenergy
        user.Rage = False

    def special_end(self, user):
        berserkenergy = user.berserkenergy + user.maxhp - user.hp
        if user.hp < 1:
            user.energy = user.berserkenergy
        elif berserkenergy < user.maxenergy:
            user.maxenergy = berserkenergy
        elif berserkenergy > user.maxenergy:
            newenergy = berserkenergy - user.maxenergy
            user.maxenergy = berserkenergy
            user.energy += newenergy
            user.fight.string.add(u'\U0001F621' + "| Bersker " + user.name + ' olayabdi ' + str(newenergy) + ' energiya')
        if user.hp == 1 and not user.Rage:
            user.Rage = True
            user.bonusdamage += 2
            user.fight.string.add(u'\U0001F621' + "| Bersker " + user.name + ' jangovor transga kirayabdi!')
        elif user.hp != 1 and user.Rage == True:
            user.Rage = False


class Healer(Ability):
    name = 'Medik'
    info = 'Siz qo`shimcha stimulyator olasiz va joningizni 2taga ko`paytira olasiz.'
    MeleeOnly = False
    RangeOnly = False
    TeamOnly = False

    def aquare(self, user):
        user.itemlist.append(Item_list.heal)


class Healter(Ability):
    name = 'Doktor'
    info = 'Siz qo`shimcha stimulyator olasiz va joningizni 3taga ko`paytira olasiz.'
    MeleeOnly = False
    RangeOnly = False
    TeamOnly = False

    def aquare(self, user):
        user.itemlist.append(Item_list.healt)


class Undead(Ability):
    name = 'Zombi'
    info = 'O`lganizdan so`ng qasd olish imkoniga ega bo`lasiz.'
    MeleeOnly = False
    RangeOnly = False
    TeamOnly = False

    def aquare(self, user):
        if 'Zombie' not in user.passive:
            user.passive.append('Zombie')

    def stop(self, user):
        if user.Alive:
            user.passive.remove('Zombie')


class Engineer(Ability):
    name = 'Qurolchi'
    info = 'Siz do`stingizni qurolini qayta o`qlashingiz mumkin. Uning otish aniqligi keyingi yurishda ortadi.' \
           'Faqat masofada ishlatuvchi qurollarga nisbatan ishlatiladi.'
    MeleeOnly = False
    RangeOnly = False
    TeamOnly = True

    def aquare(self, user):
        user.engineerrefresh = 0
        user.itemlist.append(Item_list.engineer)

    def stop(self, user):
        user.engineerrefresh = 0

    def special_end(self, user):
        print('Qayta o`qlash ' + user.name)
        if user.Alive:
            if user.engineerrefresh == user.fight.round:
                user.itemlist.append(Item_list.engineer)
                bot.send_message(user.chat_id, '"Qurolchi" qobiliyati yangilandi!')
            elif user.engineerrefresh - user.fight.round > 0:
                bot.send_message(user.chat_id, '"Qurolchi" qobiliyati '
                                               + str(user.engineerrefresh - user.fight.round) + " yurishdan so`ng yangilanadi.")


class Impaler(Ability):
    name = 'Taran'


class Ritual(Ability):
    name = 'Ritualist'
    info = 'O`ljani tanlang. Agarda u 3ta yurish davomida o`lsa siz ' \
           ' har qanday o`yinchidan 2ta jonni tortib olishiz mumkin.'
    MeleeOnly = False
    RangeOnly = False
    TeamOnly = False

    def aquare(self, user):
        user.itemlist.append(Item_list.ritual)
        user.cursecounter = 0
        user.cursetarget = None

    def special_end(self, user):
        if user.cursetarget is not None:
            if not user.cursetarget.Alive:
                user.itemlist.append(Item_list.curse)
                bot.send_message(user.chat_id, 'Siz ritual shartini bajardingiz!')
                user.cursetarget = None
            user.cursecounter -= 1
            if user.cursecounter == 0 and user.cursetarget is not None:
                bot.send_message(user.chat_id, 'Siz ritualni bekorga sarfladingiz')
                user.cursetarget = None


class Blocker(Ability):
    name = 'Himoyachi'
    info = 'Siz tirik ekansiz - raqiblar qolgan do`stlaringizga yaqin masofada hujum qila olmaydi. Botga qarshi ta`sir etmaydi.'
    MeleeOnly = True
    RangeOnly = False
    TeamOnly = True


class Necromancer(Ability):
    name = 'Nekromant'
    info = 'Siz Zombilarni uyg`otishingiz mumkin.'
    MeleeOnly = True
    RangeOnly = False
    TeamOnly = True

    def aquare(self, user):
        user.itemlist.append(Item_list.zombie)
    def special_end(self, user):
        if Item_list.zombie not in user.itemlist:
            user.itemlist.append(Item_list.zombie)


class Zombie(Ability):
    name = 'O`lik'
    def aquare(self, user):
        user.energy = 0
        user.hp = 0

    def special_end(self, user):
        if user.Hit and user.target.Losthp:
            user.hungercounter = 2
        else:
            user.fight.string.add(u'\U0001F631' + '| O`lik ' + user.name + ' ochlikdan qiynalmoqda!')
            user.hungercounter -= 1
        if user.hungercounter == 0:
            user.abilities.remove(Zombie)
            user.team.actors.remove(user)
            user.team.players.remove(user)
            user.team.deadplayers.append(user)
            user.fight.activeplayers.remove(user)
            user.fight.actors.remove(user)
            user.fight.string.add(u'\U00002620' + '| Zombi ' + user.name + ' boshqa harakatlana olmaydi.')
        user.accuracy = 6 - user.hungercounter*2


class Isaev(Ability):
    name = 'Kachok'
    info = 'Dushmanni haqoratlaydi.'
    MeleeOnly = False
    RangeOnly = False
    TeamOnly = False

    def aquare(self, user):
        user.isaevrefresh = 0
        user.itemlist.append(Item_list.isaev)

    def special_end(self, user):
        if user.Alive:
            if user.isaevrefresh == user.fight.round:
                user.itemlist.append(Item_list.isaev)
                bot.send_message(user.chat_id, '"Kachok" qobiliyati yangilandi!')
            elif user.isaevrefresh - user.fight.round > 0:
                bot.send_message(user.chat_id, '"Kachok" qobiliyati '
                                 + str(user.isaevrefresh - user.fight.round) + " yurishdan so`ng yangilanadi.")


class Thieve(Ability):

    name = 'O`g`ri'
    info = 'Siz raqib ishlatyotgan jihozlarni o`g`irlashingiz mumkin.'
    MeleeOnly = False
    RangeOnly = False
    TeamOnly = False

    def aquare(self, user):
        user.accuracy += 1
        user.stealrefresh = 0
        user.itemlist.append(Item_list.steal)

    def special_end(self, user):
        if user.Alive:
            if user.stealrefresh == user.fight.round:
                user.itemlist.append(Item_list.steal)
                bot.send_message(user.chat_id, '"O`g`ri" qobiliyati yangilandi!')
            elif user.stealrefresh - user.fight.round > 0:
                bot.send_message(user.chat_id, '"O`g`ri" qobiliyati '
                                               + str(user.stealrefresh - user.fight.round) + " yurishdan so`ng yangilanadi.")


class Jet(Ability):

    name = 'Djet'
    info = '3ta yurishdan so`ng energiya to`ladi.'
    MeleeOnly = False
    RangeOnly = False
    TeamOnly = False

    def special_end(self, user):
        if user.jetturn == user.fight.round:
            user.energy = user.maxenergy
            user.fight.string.add(u'\U0001F489' + " |" + 'Energiya ' + user.name
                                  + ' maksimalgacha tiklandi! (' + str(user.energy) + ')')

            user.tempabilities.append(self)


class Chitin(Ability):

    name = 'Xitin'
    info = '3 yurishga 2ta zarbni qaytarish olasiz so`ng karaxtalanasiz.'
    MeleeOnly = False
    RangeOnly = False
    TeamOnly = False

    def special_end(self, user):
        if user.chitinoff == user.fight.round:
            user.armor -= 2
            user.armorchance -= 100
            user.stuncounter += 1
            user.fight.string.add(u'\U0001F300' + " |" + user.name + ' Xitin efektini yo`qotdi. O`yinchi karaxtlandi!')
            user.tempabilities.append(self)


class Junkie(Ability):

    name = 'Narkoman'
    info = 'Siz 1 aniqlikni yo`qotasiz. Har safar Adrenalin, Xitin, Stimulyator yoki Djet - ' \
           'ishlatganizda 2 aniqlik va 1 zarb kuchi olasiz.'

    MeleeOnly = False
    RangeOnly = False
    TeamOnly = False

    def aquare(self, user):
        x = random.randint(1, 4)
        if x == 1:
            user.itemlist.append(Item_list.drug)
        elif x == 2:
            user.itemlist.append(Item_list.chitin)
        elif x == 3:
            user.itemlist.append(Item_list.heal)
        elif x == 4:
            user.itemlist.append(Item_list.jet)
        user.accuracy -= 1

    def special_used(self, user):
        if user.Drugged:
            user.tempaccuracy += 2
            user.bonusdamage += 1
            user.damagefix += 1
            user.fight.string.add(u'\U0001F643' + " |" + user.name + ' aniqlik va zarb kuchi oldi!')

class IronFist(Ability):

    name = 'Temir Qo`l'
    info = 'Siz o`z qurolingizni yo`qotasiz. Yalang`och mushtlar bilan olishasiz. Ma`lumotlarda qurol qayt qilinmaydi.'

    MeleeOnly = False
    RangeOnly = False
    TeamOnly = False

    def aquare(self, user):
        user.weapon = Weapon_list.master_fist

abilities.append(Piromant)
abilities.append(Armorer)
abilities.append(Revenge)
abilities.append(Hypnosyser)
abilities.append(Sadist)
abilities.append(Mentalist)
abilities.append(Gasmask)
abilities.append(Target)
abilities.append(Shields)
abilities.append(Strength)
abilities.append(Hoarder)
abilities.append(Undead)
abilities.append(Engineer)
abilities.append(West)
abilities.append(Healer)
abilities.append(Healter)
abilities.append(Ritual)
abilities.append(Blocker)
abilities.append(Berserk)
abilities.append(Necromancer)
abilities.append(Thieve)
abilities.append(Junkie)
unique_abilities.append(IronFist)
unique_abilities.append(Healter)
usual_abilities.append(Sturdy.Sturdy)
usual_abilities.append(Piromant)
usual_abilities.append(Armorer)
usual_abilities.append(Revenge)
usual_abilities.append(Sadist)
usual_abilities.append(Mentalist)
usual_abilities.append(Gasmask)
usual_abilities.append(Target)
usual_abilities.append(Shields)
usual_abilities.append(Strength)
usual_abilities.append(Hoarder)
usual_abilities.append(Undead)
usual_abilities.append(Engineer)
usual_abilities.append(West)
usual_abilities.append(Healer)
usual_abilities.append(Ritual)
usual_abilities.append(Blocker)
usual_abilities.append(Berserk)
usual_abilities.append(Necromancer)
usual_abilities.append(Thieve)
usual_abilities.append(Junkie)
unique_abilities.append(IronFist)
unique_abilities.append(Healter)
