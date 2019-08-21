import Weapon_list
import utils
import random
import Main_classes
import special_abilities
import Item_list
import secret_abilities


class AI_player(object):
    def __init__(self, name, game, team):
        # Переменные для бота
        self.bot = True
        self.lostweapon = None
        self.toughness = 6
        self.weapon = None
        self.name = name
        self.game = game
        self.fight = game.fight
        self.chat_id = random.randint(1,1000)
        self.info = Main_classes.Actionstring(self.chat_id)
        self.turn = None
        # Переменные для боя
        self.maxhp = 3
        self.maxenergy = 4
        self.truedamage = 0
        self.accuracy = 0
        self.mult = 1
        self.armor = 0
        self.evasion = 0
        self.armorchance = 0
        self.itemlist = []
        self.passive = []
        self.abilities = []
        self.targets = []
        self.Blocked = False
        self.Losthp = False
        self.hypnosysresist = 40
        self.Suicide = False
        # Временные переменные боя
        self.hp = 3
        self.energy = 4
        self.tempaccuracy = 0
        self.firecounter = 0
        self.bleedcounter = 0
        self.stuncounter = 0
        self.Hit = False
        self.Hitability = False
        self.accuracyfix = 0
        self.damagefix = 0
        self.Inmelee = False
        self.Disabled = False
        self.Drugged = False
        # особые эффекты, которые срабатывают после удара
        self.weaponeffect = []
        self.damagetaken = 0
        self.hploss = 1
        self.bonusdamage = 0
        self.extinguish = False
        self.turn = None
        self.target = None
        self.healtarget = None
        self.itemtarget = None
        self.team = team
        self.Alive = True
        self.useditems = []
        self.enditems = []
        self.attackers = []
        self.dropweapons =[]

    def attack(self):
            n = self.weapon.hit(self)
            if n != 0: self.Hit = True
            return self.weapon.getDesc(n, self)

    def aiaction1q(self, fight):
            pass
    def aiaction2q(self, fight):
        pass
    def aiactionlastq(self, fight):
        pass
    def aiactionend(self, fight):
        pass
    def appear(self, fight):
        pass


class Dog(AI_player):

    def __init__(self, name, game, team):
        AI_player.__init__(self, name, game, team)
        self.abilities = [Bloodthurst]
        self.weapon = Weapon_list.fangs
        self.servant = False
        self.leader = None
        self.offfire = None

    def rest(self):
        self.energy = self.maxenergy
        return u'\U0001F624' + "|" + self.name + ' chuqur nafas olyabdi. Energiya to`liq tiklandi.'

    def get_turn(self, Fight):
        if self.Disabled:
            self.turn = 'disabled'
        elif self.firecounter > 1 and self.offfire != Fight.round:
                Fight.string.add(self.name + ' yerda dumalab o`tni o`chiryabdi.')
                self.extinguish = True
                self.turn = 'skip' + str(Fight.round)

        elif self.Inmelee:
                self.target = utils.get_other_team(self).actors[
                random.randint(0, len(utils.get_other_team(self).actors) - 1)]
                for player in utils.get_other_team(self).actors:
                    if 0 < player.hp < self.target.hp:
                        self.target = player
                if random.randint(1, 3) == 1 and self.energy > 1:
                    self.target = utils.get_other_team(self).actors[random.randint(0,len(utils.get_other_team(self).actors) - 1)]
                    self.turn = 'attack' + str(Fight.round)
                elif self.target.hp == 1 and self.energy > 0:
                    self.tempaccuracy += 3
                    self.turn = 'attack' + str(Fight.round)
                elif self.energy > 2:
                    self.turn = 'attack' + str(Fight.round)
                elif self.firecounter > 0:
                    Fight.string.add(self.name + ' yerda dumalab o`tni o`chiryabdi.')
                    self.extinguish = True
                    self.turn = 'skip' + str(Fight.round)
                else:
                    self.turn = 'dog_rest' + str(Fight.round)

        else:
            self.turn = 'move' + str(Fight.round)

    def aiaction2q(self, Fight):
        if self.turn == 'dog_rest' + str(Fight.round):
            Fight.string.add(self.rest())

    def appear(self, Fight):
        for actor in self.team.actors:
            if isinstance(actor, DogLeader):
                self.servant = True
                self.leader = actor

    def aiactionend(self, Fight):
        x = random.randint(1,5)
        print(str(x))
        if self.leader != None:
            if self.leader.hp <= 0 and x > 3 and len(utils.get_other_team(self).actors) > 0\
                    and len(utils.get_other_team(self).actors) >= len(self.team.actors) and self.hp > 0 and self.hp < 3:
                self.Alive = False
                Fight.string.add(u'\U00002620' + ' |' + self.name + ' qo`rqoqlardek jang maydonidan qochib ketyabdi.')
                self.team.actors.remove(self)
                Fight.aiplayers.remove(self)
                Fight.actors.remove(self)



class Bloodthurst(special_abilities.Ability):
    name = 'Qonxo`rlik'


class DogLeader(AI_player):
    def __init__(self, name, game, team, teambonus):
        AI_player.__init__(self, name, game, team)
        self.abilities = [special_abilities.Gasmask, Bloodthurst, Howl, special_abilities.Armorer, Leader]
        self.teambonus = teambonus
        self.maxhp = 3 + teambonus
        self.hp = 3 + teambonus
        self.maxenergy = 3 + teambonus
        self.energy = 3 + teambonus
        self.bonusdamage += teambonus
        self.howlcounter = 0
        self.weapon = leaderfangs
        self.final = False
        self.wonpic = 'BQADAgADBwQAAhLFcEpL99FOxg2FwQI'
    def rest(self):
        self.energy = self.maxenergy
        return u'\U0001F624' + "|" + self.name + ' chuqur nafas olyabdi. Energiya to`liq tiklandi.'

    def get_turn(self, Fight):
        if float(self.hp)<=self.maxhp/2 and self.final is False:
            self.fight.string.add(u'\U00002757' + "|"+self.name + ' jahl bilan o`kirayabdi!')
            self.bonusdamage += self.teambonus - 1
            self.armor += 2
            self.armorchance += 20
            self.accuracy += 2
            self.maxenergy += self.teambonus
            self.final = True
        if self.Disabled:
            self.turn = 'disabled'
        elif self.howlcounter is 0 and self.energy > 0 and random.randint(1,3) == 1 and Fight.round != 1 and len(self.team.actors) != 1 \
                and not any(x.energy==0 for x in self.team.actors) and self.hp != 1:
            self.turn = 'howl' + str(Fight.round)
            self.energy -= 1

        elif self.Inmelee:
                self.target = utils.get_other_team(self).actors[
                random.randint(0, len(utils.get_other_team(self).actors) - 1)]
                for player in utils.get_other_team(self).actors:
                    if 0 < player.hp < self.target.hp:
                        self.target = player
                if random.randint(1,3) == 1 and self.energy > 1:
                    self.target = utils.get_other_team(self).actors[random.randint(0,len(utils.get_other_team(self).actors) - 1)]
                    self.turn = 'attack' + str(Fight.round)
                elif self.target.hp == 1 and self.energy > 0:
                    self.tempaccuracy += 3
                    self.turn = 'attack' + str(Fight.round)
                elif self.energy > 2:
                    self.turn = 'attack' + str(Fight.round)

                else:
                    self.turn = 'dog_rest' + str(Fight.round)

        else:
            self.turn = 'move' + str(Fight.round)
    def aiaction1q(self, Fight):
        if self.howlcounter > 0:
            self.howlcounter -= 1
    def aiaction2q(self, Fight):
        if self.turn == 'dog_rest' + str(Fight.round):
            Fight.string.add(self.rest())
        if self.turn == 'howl' + str(Fight.round):
            Fight.string.add(u'\U00002757' + "|"+self.name + ' o`tkir o`kirish eshitildi! Itlar kuchi ortdi!')
            self.howlcounter = 3

    def aiactionend(self, Fight):
        if self.turn == 'howl' + str(Fight.round):
            for actor in self.team.actors:
                if isinstance(actor, Dog):
                    actor.energy += 2
                    actor.accuracy += 2
                    actor.accuracyfix += 2
                    actor.bonusdamage += 1
                    actor.damagefix += 1

leaderfangs = Weapon_list.Bleeding(3, 1, 2, 1, 1, True, True, True, 'Tirnoqlar', '1-5' + u'\U0001F4A5' + "|" + '2' + u'\U000026A1', 4, standart = False,natural=True)
leaderfangs.desc1 = 'O`yinchi Raqibiga qarab tashlanayabdi.'
leaderfangs.desc2 = 'O`yinchi Raqibiga qarab tashlanayabdi.'
leaderfangs.desc3 = 'O`yinchi Raqibiga qarab tashlanayabdi.'
leaderfangs.desc4 = 'O`yinchi Raqibiga qarab tashlanayabdi, lekin tekkiza olmadi.'
leaderfangs.desc5 = 'O`yinchi Raqibiga qarab tashlanayabdi, lekin tekkiza olmadi.'
leaderfangs.desc6 = 'O`yinchi Raqibiga qarab tashlanayabdi, lekin tekkiza olmadi.'


class Rhino(AI_player):

    # Основные параметра Носорога

    def __init__(self, name, Game, team, teambonus):
        AI_player.__init__(self, name, Game, team)
        self.abilities = [special_abilities.Impaler, Stun, Leader]
        self.teambonus = teambonus
        self.maxhp = 4 + teambonus
        self.hp = 4 + teambonus
        self.maxenergy = 2 + int(teambonus/2)
        self.energy = 2 + int(teambonus/2)
        self.bonusdamage += teambonus
        self.weapon = horn
        self.armor = teambonus + 1
        self.armorchance = 60
        self.final = False
        self.highest_damagedealer = None
        self.highest_damage = 0
        self.lasthploss = None
        self.circlecd = 0
        self.trumpcd = 0

        self.hypnosysresist = 70

    # Определение хода Носорога

    def get_target(self):
        if self.highest_damagedealer != None and self.highest_damagedealer.Alive:
            target = self.highest_damagedealer
        else:
            target = utils.get_other_team(self).actors[random.randint(0, len(utils.get_other_team(self).actors) - 1)]
        return target

    def get_turn(self, fight):
        if float(self.hp) <= self.maxhp/2 and self.final is False:
            self.fight.string.add(u'\U00002757' + "| Ko`zlari qonga to`ldi "+self.name + '! U jahlda!')
            self.bonusdamage += self.teambonus - 1
            self.armorchance += 40
            self.accuracy += 2
            self.maxenergy += self.teambonus
            self.final = True
        meleecounter = 0
        for x in utils.get_other_team(self).actors:
            if x.weapon.Melee and x.Inmelee:
                meleecounter += 1
        # Застанен
        if self.Disabled:
            self.turn = 'disabled'
        # Влететь в мили
        elif not self.Inmelee:
            self.target = self.get_target()
            self.turn = 'rhino_tramp' + str(fight.round)
            self.Inmelee = True
        elif self.energy < 1:
            self.turn = 'rhino_rest' + str(fight.round)
        # Раскидать милишников
        elif float(meleecounter) >= len(utils.get_other_team(self).actors)/2 and random.randint(1,2) == 1 and self.circlecd < 1:
            self.turn = 'rhino_circle' + str(fight.round)
        # Отомстить за удар
        else:
            self.target = self.get_target()
            if not self.target.weapon.Melee and self.trumpcd < 1 or not self.target.Inmelee and self.trumpcd < 1:
                self.turn = 'rhino_tramp' + str(fight.round)
            elif self.target.Disabled:
                self.turn = 'rhino_stomp' + str(fight.round)
            else: self.turn = 'attack' + str(fight.round)

    # Навыки Носорога

    def rest(self):
        self.energy = self.maxenergy
        return u'\U0001F624' + "|" + self.name \
               + ' baqirib hujum tayorlanayabdi. Energiya to`liq tiklandi.'

    def tramp(self):
        damage = self.bonusdamage*random.randint(2,3)
        self.target.damagetaken += damage
        self.energy -= 1
        if random.randint(1,3)!=3:
            self.target.stuncounter += 2
            self.trumpcd = 4
            return u'\U0001F300' + "|" + self.name + ' hujumga shaylandi va ' + self.target.name + 'ni yugurib kelib oyog`idan chaldi. ' \
                + self.target.name + ' karaxt bo`ldi. Yetkazildi ' + str(damage) + ' zarb!'
        else:
            self.trumpcd = 4
            return u'\U0001F4A2' + "|" + self.name + ' hujumga shaylandi va ' + self.target.name + 'ni yugurib kelib oyog`idan chaldi. ' \
                    ' Yetkazildi ' + str(damage) + ' zarb!'

    def stomp(self):
        damage = self.bonusdamage * random.randint(2, 3) + 3
        self.target.damagetaken += damage
        self.energy -= 1
        return u'\U0001F4A2' + "|" + self.name + ' yerda yotganni bosib tashlayabdi ' + self.target.name + ' !' \
               + ' Yetkazildi ' + str(damage) + ' zarb!'

    def poisoned(self):
        return u'\U0001F300' + "|" + self.name + ' zaxarli nafas chiqarayabdi. Energiya no`llandi!'

    def circle(self):
        damage = self.bonusdamage*random.randint(1,2)
        self.energy -= 1
        self.circlecd = 3
        for x in utils.get_other_team(self).actors:
            if x.weapon.Melee and x.Inmelee:
                x.damagetaken += damage
                x.Inmelee = False
        self.Inmelee = False
        return u'\U0001F4A5' + "|" + self.name + ' unga yaqinlashgan hamma raqiblarni itarib yuborib, ularga yetkazdi ' \
               + str(damage) + ' zarb!'


    # Определение хода Носорога

    def aiaction1q(self, fight):
        if self.turn == 'rhino_rest' + str(fight.round) or self.turn == 'rhino_poisoned' + str(fight.round):
            self.armor = 0
        else:
            self.armor = self.teambonus+1

    def aiaction2q(self, fight):
        if self.turn == 'rhino_poisoned' + str(fight.round):
            fight.string.add(self.poisoned())
        elif self.turn == 'rhino_tramp' + str(fight.round):
            fight.string.add(self.tramp())
        elif self.turn == 'rhino_stomp' + str(fight.round):
            if self.target.Disabled:
                fight.string.add(self.stomp())
            else:
                self.attack()
        elif self.turn == 'rhino_circle' + str(fight.round):
            fight.string.add(self.circle())

        elif self.turn == 'rhino_rest' + str(fight.round):
            fight.string.add(self.rest())

    def aiactionend(self, Fight):
        if self.circlecd > 0:
            self.circlecd -= 1
        if self.trumpcd > 0:
            self.trumpcd -= 1


class Rat(AI_player):

    # Основные параметра Носорога

    def __init__(self, name, Game, team, weapon):
        AI_player.__init__(self, name, Game, team)
        self.itemlist = [Item_list.firegrenade]
        self.maxhp = 4
        self.hp = 4
        self.maxenergy = 5
        self.energy = 5
        self.accuracy = 1
        self.weapon = weapon
        self.naturalweapon = Weapon_list.fangs
        self.dodgecd = 0
        self.ability_ready = True
        self.dodge_ready = True
        if self.weapon == Weapon_list.Bat:
            self.abilities = [special_abilities.Strength, special_abilities.Gasmask]
            self.bonusdamage += 1
        elif self.weapon == Weapon_list.spear:
            self.abilities = [special_abilities.Sturdy.Sturdy, special_abilities.Blocker, special_abilities.West]
            self.armor += 1
            self.accuracy += 1
        elif self.weapon == Weapon_list.chain:
            self.abilities = [special_abilities.Sadist, special_abilities.Armorer]
            self.maxenergy += 2
            self.energy += 2
        elif self.weapon == Weapon_list.knife:
            self.itemlist.append(Item_list.throwingknife)
            self.itemlist.append(Item_list.throwingknife)
            self.accuracy += 1
        elif self.weapon == Weapon_list.sledge:
            self.abilities = [special_abilities.Sadist, special_abilities.Gasmask]
            self.itemlist.append(Item_list.grenade)
            self.accuracy += 1
            self.hp += 1
            self.maxenergy += 1
            self.energy += 1


    # Определение хода Носорога

    def get_target(self):
        minhp = None
        for target in self.targets:
            if minhp is None:
                minhp = target.hp
                self.target = target
            else:
                if 0 < target.hp < minhp:
                    minhp = target.hp
                    self.target = target

    def get_turn(self, fight):
        self.get_target()
        readycounter = 0
        ranged = False
        for x in utils.get_other_team(self).actors:
            if x in self.targets and x.energy == x.maxenergy:
                readycounter += 1
            if not x.weapon.Melee:
                ranged = True
        # Застанен
        if self.Disabled:
            self.target = None
            self.turn = 'disabled'

        # Тушиться
        elif self.firecounter > 1 and special_abilities.Gasmask not in self.abilities or self.firecounter > 0 and not self.Inmelee and special_abilities.Gasmask not in self.abilities or self.firecounter > 0 and self.energy < 2 and special_abilities.Gasmask not in self.abilities:
            self.target = None
            self.turn = 'skip' + str(fight.round)

        # Подойти в мили
        elif not self.Inmelee and not self.targets:
            if Item_list.grenade in self.itemlist:
                self.target = None
                self.turn = Item_list.grenade.id
            elif random.randint(1,2) == 1 and Item_list.throwingknife in self.itemlist:
                self.itemtarget = utils.get_other_team(self).actors[random.randint(0, len(utils.get_other_team(self).actors) - 1)]
                self.turn = Item_list.throwingknife.id
            elif self.weapon == Weapon_list.knife and Item_list.throwingknife in self.itemlist:
                self.itemtarget = utils.get_other_team(self).actors[
                    random.randint(0, len(utils.get_other_team(self).actors) - 1)]
                self.turn = Item_list.throwingknife.id
            elif random.randint(1,2) == 1 and Item_list.firegrenade in self.itemlist:
                self.target = None
                self.turn = Item_list.firegrenade.id
            elif self.energy != self.maxenergy and not ranged:
                self.target = None
                self.turn = 'reload' + str(fight.round)
            else:
                self.target = None
                self.turn = 'move' + str(fight.round)
        # Спецатаки
        # Копье
        elif float(readycounter) >= len(self.targets)/2 and self.weapon == Weapon_list.spear and self.firecounter < 1 \
                and self.energy > 3 and random.randint(1, 3) != 1 and self.ability_ready and \
                        self.target.stuncounter == 0 and self.target.weapon != Weapon_list.sniper:
            if self.countercd == 0:
                self.target = None
                self.turn = 'aim'
                self.weapon.special(self, None)
            else:
                self.ability_ready = False
                self.get_turn(self.fight)
        # Цепь
        elif self.target.energy < 2 and self.weapon == Weapon_list.chain and random.randint(1, 4) != 1 and self.energy > 3 and self.ability_ready:
            print('drop')
            if self.dropcd == 0:
                self.turn = 'weaponspecial'
                self.weapon.special(self, self.target.chat_id)
            else:
                self.ability_ready = False
                self.get_turn(self.fight)
        # Кувалда
        elif self.target.maxenergy - self.target.energy > 1 and self.weapon == Weapon_list.sledge and random.randint(1,
                                                                                            4) != 1 and self.energy > 3 and self.ability_ready:
                if self.crushcd == 0:
                    self.turn = 'weaponspecial'
                    self.weapon.special(self, self.target.chat_id)
                else:
                    self.ability_ready = False
                    self.get_turn(self.fight)

        # Уворот
        elif self.target.stuncounter == 0 and self.target.weapon != Weapon_list.sniper and self.dodge_ready:
            if float(readycounter) >= len(self.targets)/2 and random.randint(1, 3) != 1 \
                    and self.dodgecd == 0 and self.energy != self.maxenergy and self.hp <= 2 or float(readycounter) >= len(self.targets)/2 \
                    and self.dodgecd == 0 and self.hp == 1:
                self.target = None
                self.turn = 'dodge' + str(fight.round)
            else:
                self.dodge_ready = False
                self.get_turn(self.fight)

        # Метательный нож
        elif self.energy > 3 and Item_list.throwingknife in self.itemlist and self.target.energy < 2:
            self.itemtarget = self.target
            self.target = None
            self.turn = Item_list.throwingknife.id

        elif 1 < self.energy < 4 and Item_list.firegrenade in self.itemlist and self.target.energy < 2:
            self.target = None
            self.turn = Item_list.firegrenade.id

        # Удар (Если больше 2 энергии или 50% если больше 1 энергии или есть энергия, 1 хп и тебя готовы ударить)
        elif self.energy > 2 or random.randint(1, 2) == 1 and self.energy > 1 or readycounter and self.hp==1 and self.energy > 0:
            self.turn = 'attack' + str(fight.round)

        # Отдых
        else:
            self.target = None
            self.turn = 'reload' + str(fight.round)

    def aiaction1q(self, fight):
        if self.turn == 'dodge' + str(fight.round):
            self.evasion += 5
            self.dodgecd += 2
            fight.string.add( u'\U0001F4A8' + '|' + self.name + ' xujumlardan chetlashishga urinayabdi!')

    def aiactionend(self, Fight):
        if self.dodgecd > 0:
            self.dodgecd -= 1
        self.ability_ready = True
        self.dodge_ready = True


horn = Weapon_list.Weapon(2, 1, 1, 5, 0, True, True, True, 'Shox', '?' + u'\U0001F4A5' + "|" + '1' + u'\U000026A1', standart = False,natural=True)
horn.desc1 = 'Raqibni shoxi bilan urayabdi.'
horn.desc2 = 'Raqibni shoxi bilan urayabdi.'
horn.desc3 = 'Raqibni shoxi bilan urayabdi.'
horn.desc4 = 'Raqibni shoxi bilan urayabdi, lekin tekkiza olmayabdi.'
horn.desc5 = 'Raqibni shoxi bilan urayabdi, lekin tekkiza olmayabdi.'
horn.desc6 = 'Raqibni shoxi bilan urayabdi, lekin tekkiza olmayabdi.'


class Howl(special_abilities.Ability):
    name = 'O`kirik'

class Stun(special_abilities.Ability):
    name = 'Itarib yuborish'

class Leader(special_abilities.Ability):
    name = 'Ho`jayin'


class New(AI_player):

    # Основные параметра Носорога

    def __init__(self, name, game, team):
        AI_player.__init__(self, name, game, team)
        self.maxhp = 2
        self.hp = 1
        self.maxenergy = 10
        self.energy = 10
        self.accuracy = 1
        self.weapon = Weapon_list.knifee
        self.naturalweapon = Weapon_list.fangs
        self.dodgecd = 0
        self.ability_ready = True
        self.dodge_ready = True
        self.itemlist.append(Item_list.raketa)
        self.itemlist.append(Item_list.raketa)
        self.itemlist.append(Item_list.raketa)
        self.itemlist.append(Item_list.raketa)
        self.itemlist.append(Item_list.raketa)
        self.itemlist.append(Item_list.raketa)
        self.itemlist.append(Item_list.raketa)
        self.itemlist.append(Item_list.raketa)
        self.itemlist.append(Item_list.raketa)
        self.itemlist.append(Item_list.raketa)
        self.itemlist.append(Item_list.raketa)
        self.itemlist.append(Item_list.raketa)
        self.itemlist.append(Item_list.raketa)
        self.itemlist.append(Item_list.raketa)
        self.itemlist.append(Item_list.raketa)
        self.itemlist.append(Item_list.raketa)
        self.itemlist.append(Item_list.raketa)
        self.itemlist.append(Item_list.raketa)
        self.itemlist.append(Item_list.raketa)
        self.itemlist.append(Item_list.raketa)
        self.itemlist.append(Item_list.raketa)
        self.itemlist.append(Item_list.raketa)
        self.itemlist.append(Item_list.raketa)
        self.itemlist.append(Item_list.raketa)        
        self.dropweapons.append(Weapon_list.elektrez)            

    # Определение хода Носорога

    def get_target(self):
        minhp = None
        for target in self.targets:
            if minhp is None:
                minhp = target.hp
                self.target = target
            else:
                if 0 < target.hp < minhp:
                    minhp = target.hp
                    self.target = target

    def get_turn(self, fight):
        self.get_target()
        readycounter = 0
        ranged = False
        for x in utils.get_other_team(self).actors:
            if x in self.targets and x.energy == x.maxenergy:
                readycounter += 1
            if not x.weapon.Melee:
                ranged = True
        # Застанен
        if self.Disabled:
            self.target = None
            self.turn = 'disabled'

        # Тушиться
        elif self.firecounter > 2:
                self.fight.string.add(self.name + ' "𝐎𝐥𝐨𝐯𝐧𝐢 𝐎`𝐜𝐡𝐢𝐫𝐢𝐬𝐡🧯" tizimini ishga tushurdi.') 
                self.turn = 'skip' + str(fight.round)

        # Подойти в мили
        elif not self.Inmelee and not self.targets:
            if Item_list.raketa in self.itemlist:
                self.target = None
                self.turn = Item_list.raketa.id
            elif random.randint(1,2) == 1 and Item_list.raketa in self.itemlist:
                self.itemtarget = utils.get_other_team(self).actors[random.randint(0, len(utils.get_other_team(self).actors) - 1)]
                self.turn = Item_list.raketa.id
            elif self.weapon == Weapon_list.knife and Item_list.raketa in self.itemlist:
                self.itemtarget = utils.get_other_team(self).actors[
                    random.randint(0, len(utils.get_other_team(self).actors) - 1)]
                self.turn = Item_list.raketa.id
            elif random.randint(1,2) == 1 and Item_list.firegrenade in self.itemlist:
                self.target = None
                self.turn = Item_list.firegrenade.id
            elif self.energy != self.maxenergy and not ranged:
                self.target = None
                self.turn = 'reload' + str(fight.round)
            else:
                self.target = None
                self.turn = 'move' + str(fight.round)
        # Спецатаки
        # Копье
        elif float(readycounter) >= len(self.targets)/2 and self.weapon == Weapon_list.spear and self.firecounter < 1 \
                and self.energy > 3 and random.randint(1, 3) != 1 and self.ability_ready and \
                        self.target.stuncounter == 0 and self.target.weapon != Weapon_list.sniper:
            if self.countercd == 0:
                self.target = None
                self.turn = 'aim'
                self.weapon.special(self, None)
            else:
                self.ability_ready = False
                self.get_turn(self.fight)
        # Цепь
        elif self.target.energy < 2 and self.weapon == Weapon_list.chain and random.randint(1, 4) != 1 and self.energy > 3 and self.ability_ready:
            print('drop')
            if self.dropcd == 0:
                self.turn = 'weaponspecial'
                self.weapon.special(self, self.target.chat_id)
            else:
                self.ability_ready = False
                self.get_turn(self.fight)
        # Кувалда
        elif self.target.maxenergy - self.target.energy > 1 and self.weapon == Weapon_list.sledge and random.randint(1,
                                                                                            4) != 1 and self.energy > 3 and self.ability_ready:
                if self.crushcd == 0:
                    self.turn = 'weaponspecial'
                    self.weapon.special(self, self.target.chat_id)
                else:
                    self.ability_ready = False
                    self.get_turn(self.fight)

        # Уворот
        elif self.target.stuncounter == 0 and self.target.weapon != Weapon_list.sniper and self.dodge_ready:
            if float(readycounter) >= len(self.targets)/2 and random.randint(1, 3) != 1 \
                    and self.dodgecd == 0 and self.energy != self.maxenergy and self.hp <= 2 or float(readycounter) >= len(self.targets)/2 \
                    and self.dodgecd == 0 and self.hp == 1:
                self.target = None
                self.turn = 'dodge' + str(fight.round)
            else:
                self.dodge_ready = False
                self.get_turn(self.fight)

        # Метательный нож
        elif self.energy > 3 and Item_list.throwingknife in self.itemlist and self.target.energy < 2:
            self.itemtarget = self.target
            self.target = None
            self.turn = Item_list.throwingknife.id

        elif 1 < self.energy < 4 and Item_list.firegrenade in self.itemlist and self.target.energy < 2:
            self.target = None
            self.turn = Item_list.firegrenade.id

        # Удар (Если больше 2 энергии или 50% если больше 1 энергии или есть энергия, 1 хп и тебя готовы ударить)
        elif self.energy > 2 or random.randint(1, 2) == 1 and self.energy > 1 or readycounter and self.hp==1 and self.energy > 0:
            self.turn = 'attack' + str(fight.round)

        # Отдых
        else:
            self.target = None
            self.turn = 'reload' + str(fight.round)

    def aiaction1q(self, fight):
        if self.turn == 'dodge' + str(fight.round):
            self.evasion += 5
            self.dodgecd += 2
            fight.string.add( '📡' + '|' + self.name + ' raqibni "𝐊𝐨`𝐫 𝐐𝐢𝐥𝐢𝐬𝐡🔋" tizimini yoqayabdi!')

    def aiactionend(self, Fight):
        if self.dodgecd > 0:
            self.dodgecd -= 1
        self.ability_ready = True
        self.dodge_ready = True

class Terror(AI_player):

    def __init__(self, name, game, team):
        AI_player.__init__(self, name, game, team)
        self.abilities = [Bloodthurst]
        self.weapon = kalashnikov
        self.servant = False
        self.leader = None
        self.offfire = None
        self.dropweapons.append(Weapon_list.sledge)
        
    def rest(self):
        self.energy = self.maxenergy
        return u'\U0001F624' + "|" + self.name + ' chuqur nafas olyabdi. Energiya to`liq tiklandi.'

    def get_turn(self, Fight):
        if self.Disabled:
            self.turn = 'disabled'
        elif self.firecounter > 1 and self.offfire != Fight.round:
                Fight.string.add(self.name + ' olov o`chirgichni ishlatayabdi.')
                self.extinguish = True
                self.turn = 'skip' + str(Fight.round)

        elif self.Inmelee:
                self.target = utils.get_other_team(self).actors[
                random.randint(0, len(utils.get_other_team(self).actors) - 1)]
                for player in utils.get_other_team(self).actors:
                    if 0 < player.hp < self.target.hp:
                        self.target = player
                if random.randint(1, 3) == 1 and self.energy > 1:
                    self.target = utils.get_other_team(self).actors[random.randint(0,len(utils.get_other_team(self).actors) - 1)]
                    self.turn = 'attack' + str(Fight.round)
                elif self.target.hp == 1 and self.energy > 0:
                    self.tempaccuracy += 3
                    self.turn = 'attack' + str(Fight.round)
                elif self.energy > 2:
                    self.turn = 'attack' + str(Fight.round)
                elif self.firecounter > 0:
                    Fight.string.add(self.name + ' olov o`chirgichni ishlatayabdi.')
                    self.extinguish = True
                    self.turn = 'skip' + str(Fight.round)
                else:
                    self.turn = 'dog_rest' + str(Fight.round)

        else:
            self.turn = 'move' + str(Fight.round)

    def aiaction2q(self, Fight):
        if self.turn == 'dog_rest' + str(Fight.round):
            Fight.string.add(self.rest())

    def appear(self, Fight):
        for actor in self.team.actors:
            if isinstance(actor, Spetsnaz):
                self.servant = True
                self.leader = actor

    def aiactionend(self, Fight):
        x = random.randint(1,5)
        print(str(x))
        if self.leader != None:
            if self.leader.hp <= 0 and x > 3 and len(utils.get_other_team(self).actors) > 0\
                    and len(utils.get_other_team(self).actors) >= len(self.team.actors) and self.hp > 0 and self.hp < 3:
                self.Alive = False
                Fight.string.add(u'\U00002620' + ' |' + self.name + ' qo`rqoqlardek jang maydonidan qochib ketyabdi.')
                self.team.actors.remove(self)
                Fight.aiplayers.remove(self)
                Fight.actors.remove(self)



class Bloodthurst(special_abilities.Ability):
    name = 'Qonxo`rlik'


class Spetsnaz(AI_player):
    def __init__(self, name, game, team, teambonus):
        AI_player.__init__(self, name, game, team)
        self.abilities = [special_abilities.Gasmask, Bloodthurst, Howl, special_abilities.Armorer, Leader]
        self.teambonus = teambonus
        self.maxhp = 3 + teambonus
        self.hp = 3 + teambonus
        self.maxenergy = 3 + teambonus
        self.energy = 3 + teambonus
        self.bonusdamage += teambonus
        self.howlcounter = 0
        self.weapon = vintovka
        self.final = False
        self.wonpic = 'BQADAgADBwQAAhLFcEpL99FOxg2FwQI'
    def rest(self):
        self.energy = self.maxenergy
        return u'\U0001F624' + "|" + self.name + ' chuqur nafas olyabdi. Energiya to`liq tiklandi.'

    def get_turn(self, Fight):
        if float(self.hp)<=self.maxhp/2 and self.final is False:
            self.fight.string.add(u'\U00002757' + "|"+self.name + ' yuqori kalibrli o`qlarni qo`ymoqda!')
            self.bonusdamage += self.teambonus - 1
            self.armor += 2
            self.armorchance += 20
            self.accuracy += 2
            self.maxenergy += self.teambonus
            self.final = True
        if self.Disabled:
            self.turn = 'disabled'
        elif self.howlcounter is 0 and self.energy > 0 and random.randint(1,3) == 1 and Fight.round != 1 and len(self.team.actors) != 1 \
                and not any(x.energy==0 for x in self.team.actors) and self.hp != 1:
            self.turn = 'howl' + str(Fight.round)
            self.energy -= 1

        elif self.Inmelee:
                self.target = utils.get_other_team(self).actors[
                random.randint(0, len(utils.get_other_team(self).actors) - 1)]
                for player in utils.get_other_team(self).actors:
                    if 0 < player.hp < self.target.hp:
                        self.target = player
                if random.randint(1,3) == 1 and self.energy > 1:
                    self.target = utils.get_other_team(self).actors[random.randint(0,len(utils.get_other_team(self).actors) - 1)]
                    self.turn = 'attack' + str(Fight.round)
                elif self.target.hp == 1 and self.energy > 0:
                    self.tempaccuracy += 3
                    self.turn = 'attack' + str(Fight.round)
                elif self.energy > 2:
                    self.turn = 'attack' + str(Fight.round)

                else:
                    self.turn = 'dog_rest' + str(Fight.round)

        else:
            self.turn = 'move' + str(Fight.round)
    def aiaction1q(self, Fight):
        if self.howlcounter > 0:
            self.howlcounter -= 1
    def aiaction2q(self, Fight):
        if self.turn == 'dog_rest' + str(Fight.round):
            Fight.string.add(self.rest())
        if self.turn == 'howl' + str(Fight.round):
            Fight.string.add(u'\U00002757' + "|"+self.name + ' yuqori darajada qurollanishga buyuruq berdi!')
            self.howlcounter = 3

    def aiactionend(self, Fight):
        if self.turn == 'howl' + str(Fight.round):
            for actor in self.team.actors:
                if isinstance(actor, Terror):
                    actor.energy += 2
                    actor.accuracy += 2
                    actor.accuracyfix += 2
                    actor.bonusdamage += 1
                    actor.damagefix += 1

vintovka = Weapon_list.Vintovka(3, 1, 3, 3, 2, False, False, False, 'Vintovka M4A1', '1-3' + u'\U0001F44A' + "|" + '2' +  u'\U000026A1', 3, standart=False)
vintovka.desc1 = 'O`yinchi Raqibiga Vintovkadan otayabdi.'
vintovka.desc2 = 'O`yinchi Raqibiga Vintovkadan otayabdi.'
vintovka.desc3 = 'O`yinchi Raqibiga Vintovkadan otayabdi.'
vintovka.desc4 = 'O`yinchi Raqibiga Vintovkadan otayabdi, lekin tekkiza olmayabdi.'
vintovka.desc5 = 'O`yinchi Raqibiga Vintovkadan otayabdi, lekin tekkiza olmayabdi.'
vintovka.desc6 = 'O`yinchi Raqibiga Vintovkadan otayabdi, lekin tekkiza olmayabdi.'

kalashnikov = Weapon_list.Kalashnikov(2, 1, 3, 3, 2, False, False, False, 'Kalashnikov AK-74','1' + u'\U0001F525' + "|" + '3' + u'\U000026A1', standart=False)
kalashnikov.desc1 = 'O`yinchi Raqibiga Kalashnikovadan otayabdi.'
kalashnikov.desc2 = 'O`yinchi Raqibiga Kalashnikovdan otayabdi.'
kalashnikov.desc3 = 'O`yinchi Raqibiga Kalashnikovdan otayabdi.'
kalashnikov.desc4 = 'O`yinchi Raqibiga Kalashnikovdan otayabdi, lekin tekkiza olmayabdi.'
kalashnikov.desc5 = 'O`yinchi Raqibiga Kalashnikovdan otayabdi, lekin tekkiza olmayabdi.'
kalashnikov.desc6 = 'O`yinchi Raqibiga Kalashnikovdan otayabdi, lekin tekkiza olmayabdi.'


class Master(AI_player):

 
    def __init__(self, name, Game, team, teambonus):
        AI_player.__init__(self, name, Game, team)
        self.abilities = [special_abilities.Impaler, special_abilities.Armorer, Stun, Leader, special_abilities.Berserk,
                          secret_abilities.Regeneration, secret_abilities.Warlock, secret_abilities.Bloodlust]
        self.teambonus = teambonus
        self.maxhp = 6 + teambonus
        self.hp = 4 + teambonus
        self.maxenergy = 5 + int(teambonus/2)
        self.energy = 4 + int(teambonus/2)
        self.bonusdamage += teambonus
        self.weapon = masters
        self.armor = teambonus + 1
        self.armorchance = 30
        self.final = False
        self.highest_damagedealer = None
        self.highest_damage = 0
        self.lasthploss = None
        self.circlecd = 0
        self.trumpcd = 0       
        self.dropweapons.append(Weapon_list.speareternal)        

        self.hypnosysresist = 777

    # Определение хода Носорога


    def get_target(self):
        if self.highest_damagedealer != None and self.highest_damagedealer.Alive:
            target = self.highest_damagedealer
        else:
            target = utils.get_other_team(self).actors[random.randint(0, len(utils.get_other_team(self).actors) - 1)]
        return target

    def get_turn(self, fight):
        if float(self.hp) <= self.maxhp/2 and self.final is False:
            self.fight.string.add(u'\U00002757' + "| In-Yan♋️ kuchlari qo`shilishi bilan "+self.name + ' elementlar kuchiga ega bo`ldi!')
            self.bonusdamage += self.teambonus - 1
            self.armorchance += 30
            self.accuracy += 3
            self.maxenergy += self.teambonus
            self.final = True
        meleecounter = 0
        for x in utils.get_other_team(self).actors:
            if x.weapon.Melee and x.Inmelee:
                meleecounter += 1
        
        
