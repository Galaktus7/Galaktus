import Main_classes
import config
import telebot
import random
import special_abilities
import Weapon_list
import Item_list
import time
import threading
import ai
import secret_abilities
import datahandler

types = telebot.types
bot = telebot.TeleBot(config.token)


def prepare_fight(game):
    # Организация словаря
    game.player_dict = {p.chat_id: p for p in game.players}
    game.gamestate = 'weapon'
    bot.send_message(game.cid, 'Jang boshlanmoqda!')

    # Список активных игроков и раздача итемов
    for p in game.players:
        game.fight.activeplayers.append(p)
        p.team.actors.append(p)
        x = random.randint(0, (len(Item_list.itemlist) - 1))
        y = random.randint(0, (len(Item_list.itemlist) - 1))
        while x == y:
            y = random.randint(0, (len(Item_list.itemlist) - 1))
        p.itemlist = [Item_list.itemlist[x], Item_list.itemlist[y]]
        bot.send_message(p.chat_id, 'Sizning jihozlaringiz - ' + ', '.join(i.name for i in p.itemlist))
    print('Qurol tarqatuvchi belgilandi.')
    # Раздача оружия
    game.weaponcounter = len(game.players)
    game.waitings = True
    for p in game.players:
        get_weapon(p)
    timer = threading.Timer(90.0, game.change)
    timer.start()
    while game.weaponcounter > 0 and game.waitings is True:
        time.sleep(3)
    if game.weaponcounter == 0:
        bot.send_message(game.cid, 'Qurol tanlandi.')

    else:
        for p in game.players:
            if p.weapon is None:
                p.weapon = Weapon_list.weaponlist[random.randint(0, len(Weapon_list.weaponlist) - 1)]
        bot.send_message(game.cid, 'Qurol tanlandi yoki tarqibiy tarqatildi.')
    timer.cancel()
    for p in game.players:
        if p.weapon is None:
            p.weapon = Weapon_list.fists
        bot.send_message(p.chat_id, 'Sizning qurolingiz - ' + p.weapon.name)
    print('Qobiliyatlar tarqatuvchi initsiatsiyalandi.')

    # Раздача способностей
    game.gamestate = 'ability'
    game.abilitycounter = len(game.players)
    if len(game.team1.players) == len(game.team2.players) or not game.team2.players:
        for p in game.players:
            p.maxabilities = 2
    else:
        game.biggerTeam = game.team1
        game.lesserTeam = game.team2
        if len(game.team1.players) < len(game.team2.players):
            game.biggerTeam = game.team2
            game.lesserTeam = game.team1
        for p in game.lesserTeam.players:
            y = len(game.biggerTeam.players) - len(game.lesserTeam.players)
            p.maxabilities = y + 1
            while y > 0:
                x = random.randint(0, (len(Item_list.itemlist) - 1))
                p.itemlist.append(Item_list.itemlist[x])
                y -= 1
        for p in game.biggerTeam.players:
            p.maxabilities = 1
        for x in range(0, (len(game.biggerTeam.players) - len(game.lesserTeam.players))):
            game.lesserTeam.actors.append(ai.Rat('💂🏻' + '| Nindzya ' + str(x + 1), game, game.lesserTeam,
                                                 random.choice([Weapon_list.Bat, Weapon_list.spear, Weapon_list.chain,
                                                                Weapon_list.knife, Weapon_list.sledge])))
            game.aiplayers.append(game.lesserTeam.actors[-1])
            game.fight.aiplayers.append(game.lesserTeam.actors[-1])
            game.player_dict[game.fight.aiplayers[-1].chat_id] = game.fight.aiplayers[-1]
    game.abilitycounter = len(game.players)
    game.waitings = True
    for p in game.players:
        get_first_ability(p)
    timer = threading.Timer(90.0, game.change)
    timer.start()
    while game.abilitycounter > 0 and game.waitings is True:
        time.sleep(5)
    if game.abilitycounter == 0:
        bot.send_message(game.cid, 'Qobiliyatlar tanlandi. Jang boshlanayabdi.')
    else:
        for p in game.players:
            if len(p.abilities) < p.maxabilities:
                countera = p.maxabilities - len(p.abilities)
                while countera > 0:
                    x = special_abilities.abilities[random.randint(0, len(special_abilities.abilities) - 1)]
                    if x not in p.abilities:
                        p.abilities.append(x)
                        countera -= 1
        bot.send_message(game.cid, 'Qobiliyatlar tanlandi yoki taqribiy tarqatildi. Birinchi raund boshlanayabdi.')
    timer.cancel()

    # Подключение ai-противников
    if game.gametype == 'rhino':
        boss = ai.Rhino('Karkidon ' + '|' + u'\U0001F98F', game, game.team2,
                      len(game.team1.players))
        game.team2.actors.append(boss)
        game.fight.aiplayers.append(game.team2.actors[-1])
        game.aiplayers.append(game.team2.actors[-1])
        game.player_dict[game.fight.aiplayers[-1].chat_id] = game.fight.aiplayers[-1]
        game.abilitycounter = len(game.players)
        game.fight.Withbots = True
    elif game.gametype == 'master':
        boss = ai.Master('Master ' + '|' + '☯️', game, game.team2,
                      len(game.team1.players))
        game.team2.actors.append(boss)
        game.fight.aiplayers.append(game.team2.actors[-1])
        game.aiplayers.append(game.team2.actors[-1])
        game.player_dict[game.fight.aiplayers[-1].chat_id] = game.fight.aiplayers[-1]
        game.abilitycounter = len(game.players)
        game.fight.Withbots = True       
    elif game.gametype == 'rats':
        for x in range(0,len(game.team1.players)):
            boss = ai.Rat('Kalamush '+ str(x+1) + '|' + u'\U0001F42D', game, game.team2,
                        random.choice([Weapon_list.Bat, Weapon_list.spear, Weapon_list.chain, Weapon_list.knife, Weapon_list.sledge]))
            game.team2.actors.append(boss)
            game.fight.aiplayers.append(game.team2.actors[-1])
            game.aiplayers.append(game.team2.actors[-1])
            game.player_dict[game.fight.aiplayers[-1].chat_id] = game.fight.aiplayers[-1]
            game.abilitycounter = len(game.players)
            game.fight.Withbots = True
    elif game.gametype == 'new':
        boss = ai.Thanoscha('☸️|𝕋ℍ𝔸ℕ𝕆𝕊 ' + '|' + '🧛🏽‍♂', game, game.team2, len(game.team1.players))
        game.team2.actors.append(boss)
        game.fight.aiplayers.append(game.team2.actors[-1])
        game.aiplayers.append(game.team2.actors[-1])
        game.player_dict[game.fight.aiplayers[-1].chat_id] = game.fight.aiplayers[-1]
        for x in range(0, len(game.team1.players)):
            game.team2.actors.append(ai.New('𝕂𝕆𝕊𝕄𝕀𝕂 𝕂𝔼𝕄𝔸 ' + str(x + 1) + '|' + '🛰', game, game.team2))
            game.fight.aiplayers.append(game.team2.actors[-1])
            game.aiplayers.append(game.team2.actors[-1])
            game.player_dict[game.fight.aiplayers[-1].chat_id] = game.fight.aiplayers[-1]
        game.fight.Withbots = True
    elif game.gametype == 'dragon':
            boss = ai.Dragon('Drakon ' + '|' + '🐲', game, game.team2,
                        random.choice([Weapon_list.drago, Weapon_list.drago]))
            game.team2.actors.append(boss)
            game.fight.aiplayers.append(game.team2.actors[-1])
            game.aiplayers.append(game.team2.actors[-1])
            game.player_dict[game.fight.aiplayers[-1].chat_id] = game.fight.aiplayers[-1]
            game.abilitycounter = len(game.players)
            game.fight.Withbots = True        
    elif game.gametype == 'sup':
            boss = ai.Sup('⚫️|ℚ𝕠𝕣𝕒 𝔸𝕛𝕒𝕝' + '|' + '💀', game, game.team2,
                        random.choice([Weapon_list.magniy, Weapon_list.magniy]))
            game.team2.actors.append(boss)
            game.fight.aiplayers.append(game.team2.actors[-1])
            game.aiplayers.append(game.team2.actors[-1])
            game.player_dict[game.fight.aiplayers[-1].chat_id] = game.fight.aiplayers[-1]
            game.abilitycounter = len(game.players)
            game.fight.Withbots = True               
    elif game.gametype == 'wolfs':
        boss = ai.DogLeader('Boshliq ' + '|' + u'\U0001F43A', game, game.team2, len(game.team1.players))
        game.team2.actors.append(boss)
        game.fight.aiplayers.append(game.team2.actors[-1])
        game.aiplayers.append(game.team2.actors[-1])
        game.player_dict[game.fight.aiplayers[-1].chat_id] = game.fight.aiplayers[-1]
        for x in range(0, len(game.team1.players)):
            game.team2.actors.append(ai.Dog('Kuchuk ' + str(x + 1) + '|' + u'\U0001F436', game, game.team2))
            game.fight.aiplayers.append(game.team2.actors[-1])
            game.aiplayers.append(game.team2.actors[-1])
            game.player_dict[game.fight.aiplayers[-1].chat_id] = game.fight.aiplayers[-1]
        game.fight.Withbots = True
    elif game.gametype == 'terror':
        boss = ai.Spetsnaz('Spetsnaz ' + '|' + '👮🏿', game, game.team2, len(game.team1.players))
        game.team2.actors.append(boss)
        game.fight.aiplayers.append(game.team2.actors[-1])
        game.aiplayers.append(game.team2.actors[-1])
        game.player_dict[game.fight.aiplayers[-1].chat_id] = game.fight.aiplayers[-1]
        for x in range(0, len(game.team1.players)):
            game.team2.actors.append(ai.Terror('Terrorist ' + str(x + 1) + '|' + '👳🏻', game, game.team2))
            game.fight.aiplayers.append(game.team2.actors[-1])
            game.aiplayers.append(game.team2.actors[-1])
            game.player_dict[game.fight.aiplayers[-1].chat_id] = game.fight.aiplayers[-1]
        game.fight.Withbots = True
    game.gamestate = 'fight'


    # Последняя подготовка
    for p in game.players:
        if datahandler.get_private_string(p.chat_id) == '1':
            p.private_string = True

        if p.weapon is None:
            p.weapon = Weapon_list.fists
        p.fight.string.add('Qurol ' + p.name + ' - ' + p.weapon.name)
        for a in p.abilities:
            a.aquare(a, p)
            a.aquareonce(a, p)
        if p.weapon.Melee:
            p.Inmelee = False
        p.weapon.aquare(p)
        check_secrets_abilities(p)
    for p in game.fight.aiplayers:
        for a in p.abilities:
            a.aquare(a, p)
            a.aquareonce(a, p)
        if p.weapon.Melee:
            p.Inmelee = False
        p.weapon.aquare(p)
    print('1-Guruh - ' + ', '.join([p.name for p in game.team1.players]))
    print('2-Guruh - ' + ', '.join([p.name for p in game.team2.players]))
    game.fight.string.post(bot, 'Qurolni tanlash')
    try:
        game.startfight()
    except:
        bot.send_message(game.cid, 'Qandaydir xatolik o`yin qayta boshlanadi.')
        delete_game(game)


def prepare_custom_fight(game):
    # Организация словаря
    game.player_dict = {p.chat_id: p for p in game.players}
    game.gamestate = 'weapon'
    bot.send_message(game.cid, 'Jang boshlanayabdi!')

    # Список активных игроков и раздача итемов
    for p in game.players:
        game.fight.activeplayers.append(p)
        p.team.actors.append(p)
        data = datahandler.get_current(p.chat_id)
        weapon_name = data[0]
        for weapon in Weapon_list.fullweaponlist:
            if weapon.name == weapon_name:
                p.weapon = weapon
                break
        item_ids = data[1].split(',')
        print(', '.join(item_ids))
        for item_id in item_ids:
            p.itemlist.append(Item_list.items[item_id])
        skill_names = data[2].split(',')
        for skill_name in skill_names:
            for skill in special_abilities.abilities:
                if skill.name == skill_name:
                    p.abilities.append(skill)
                    break
    # Подключение ai-противников
    if game.gametype == 'rhino':
        boss = ai.Rhino('Karkidon ' + '|' + u'\U0001F98F', game, game.team2, len(game.team1.players))
        game.team2.actors.append(boss)
        game.fight.aiplayers.append(game.team2.actors[-1])
        game.aiplayers.append(game.team2.actors[-1])
        game.player_dict[game.fight.aiplayers[-1].chat_id] = game.fight.aiplayers[-1]
        game.abilitycounter = len(game.players)
        game.fight.Withbots = True
    elif game.gametype == 'master':
        boss = ai.Master('Master ' + '|' + '☯️', game, game.team2,
                      len(game.team1.players))
        game.team2.actors.append(boss)
        game.fight.aiplayers.append(game.team2.actors[-1])
        game.aiplayers.append(game.team2.actors[-1])
        game.player_dict[game.fight.aiplayers[-1].chat_id] = game.fight.aiplayers[-1]
        game.abilitycounter = len(game.players)
        game.fight.Withbots = True              
    elif game.gametype == 'wolfs':
        boss = ai.DogLeader('Karkidon ' + '|' + u'\U0001F43A', game, game.team2, len(game.team1.players))
        game.team2.actors.append(boss)
        game.fight.aiplayers.append(game.team2.actors[-1])
        game.aiplayers.append(game.team2.actors[-1])
        game.player_dict[game.fight.aiplayers[-1].chat_id] = game.fight.aiplayers[-1]
        for x in range(0, len(game.team1.players)):
            game.team2.actors.append(ai.Dog('Kuchuk ' + str(x + 1) + '|' + u'\U0001F436', game, game.team2))
            game.fight.aiplayers.append(game.team2.actors[-1])
            game.aiplayers.append(game.team2.actors[-1])
            game.player_dict[game.fight.aiplayers[-1].chat_id] = game.fight.aiplayers[-1]
        game.fight.Withbots = True
    game.gamestate = 'fight'

    # Последняя подготовка
    for p in game.players:
        if datahandler.get_private_string(p.chat_id) == '1':
            p.private_string = True

        if p.weapon is None:
            p.weapon = Weapon_list.fists
        p.fight.string.add('Qurol ' + p.name + ' - ' + p.weapon.name)
        for a in p.abilities:
            a.aquare(a, p)
            a.aquareonce(a, p)
        if p.weapon.Melee:
            p.Inmelee = False
        p.weapon.aquare(p)
    for p in game.fight.aiplayers:
        for a in p.abilities:
            a.aquare(a, p)
            a.aquareonce(a, p)
        if p.weapon.Melee:
            p.Inmelee = False
        p.weapon.aquare(p)
    print('1-Guruh - ' + ', '.join([p.name for p in game.team1.players]))
    print('2-Guruh - ' + ', '.join([p.name for p in game.team2.players]))
    game.fight.string.post(bot, 'Qurol tanlovi')
    try:
        game.startfight()
    except:
        bot.send_message(game.cid, 'Qandaydir xatolik. O`yin qayta boshlanadi.')
        delete_game(game)


def get_other_team(player):
    if player.team == player.fight.team1:
        return player.game.team2
    elif player.team == player.game.team2:
        return player.game.team1


def remove_player(playerchat_id, game):
    removing = None
    for p in game.players:
        if p.chat_id == playerchat_id:
            removing = p
    try:
        removing.team.remove(removing)
    except AttributeError:
        pass
    game.players.remove(removing)
    del Main_classes.dict_players[playerchat_id]


def get_first_ability(player):
    keyboard = types.InlineKeyboardMarkup()
    maxchoiceint = 5
    choice = []
    while len(choice) < maxchoiceint:
        x = special_abilities.abilities[random.randint(0, len(special_abilities.abilities)-1)]
        if player.weapon.Melee:
            if len(player.team.players) == 1:
                if x not in choice and x not in player.abilities and not x.RangeOnly and not x.TeamOnly:
                    choice.append(x)
            else:
                if x not in choice and x not in player.abilities and not x.RangeOnly:
                    choice.append(x)

        else:
            if len(player.team.players) == 1:
                if x not in choice and x not in player.abilities and not x.MeleeOnly and not x.TeamOnly:
                    choice.append(x)
            else:
                if x not in choice and x not in player.abilities and not x.MeleeOnly:
                    choice.append(x)
    for c in choice:
        callback_button1 = types.\
            InlineKeyboardButton(text=c.name, callback_data=str('a' + str(special_abilities.abilities.index(c))))
        callback_button2 = types.\
            InlineKeyboardButton(text='Info', callback_data=str('i' + str(special_abilities.abilities.index(c))))
        keyboard.add(callback_button1, callback_button2)
    if player.chat_id == 379168159 or player.name == 'Пасюк' or player.chat_id == 197216910:
        callback_button1 = types. \
            InlineKeyboardButton(text=special_abilities.Healter.name, callback_data=str('unique_a' + str(special_abilities.unique_abilities.index(special_abilities.Healter))))
        callback_button2 = types. \
            InlineKeyboardButton(text='Info', callback_data=str(str('unique_i' + str(special_abilities.unique_abilities.index(special_abilities.Healter)))))
        keyboard.add(callback_button1, callback_button2)
    bot.send_message(
        player.chat_id, 'Qobiliyatlarni tanlang. Sizni maksimal qobiliyatlaringiz - ' + str(player.maxabilities),
        reply_markup=keyboard
        )


def get_ability(player):
    keyboard = types.InlineKeyboardMarkup()
    maxchoiceint = 5
    choice = []
    while len(choice) < maxchoiceint:
        x = special_abilities.abilities[random.randint(0, len(special_abilities.abilities)-1)]
        if player.weapon.Melee:
            if len(player.team.players) == 1:
                if x not in choice and x not in player.abilities and not x.RangeOnly and not x.TeamOnly:
                    choice.append(x)
            else:
                if x not in choice and x not in player.abilities and not x.RangeOnly:
                    choice.append(x)

        else:
            if len(player.team.players) == 1:
                if x not in choice and x not in player.abilities and not x.MeleeOnly and not x.TeamOnly:
                    choice.append(x)
            else:
                if x not in choice and x not in player.abilities and not x.MeleeOnly:
                    choice.append(x)
    for c in choice:
        callback_button1 = types.\
            InlineKeyboardButton(text=c.name, callback_data=str('a' + str(special_abilities.abilities.index(c))))
        callback_button2 = types.\
            InlineKeyboardButton(text='Info', callback_data=str('i' + str(special_abilities.abilities.index(c))))
        keyboard.add(callback_button1, callback_button2)
    bot.send_message(
        player.chat_id, 'Qobiliyatni tanlang. Sizning maksimal qobiliyatlaringiz - ' + str(player.maxabilities),
        reply_markup=keyboard
        )


def get_weapon(player):
    keyboard = types.InlineKeyboardMarkup()
    maxchoiceint = 3
    choice = []
    while len(choice) < maxchoiceint:
        x = Weapon_list.weaponlist[random.randint(0, len(Weapon_list.weaponlist) - 1)]
        if x not in choice:
            choice.append(x)
    unique_weapon = datahandler.get_unique(player.chat_id)[0]
    if unique_weapon is not None:
        unique_weapon_names = unique_weapon.split(',')
        for name in unique_weapon_names:
            for weapon in Weapon_list.fullweaponlist:
                if weapon.name == name:
                    choice.append(weapon)
    for c in choice:
        callback_button1 = types.InlineKeyboardButton(text=c.name,
                                                      callback_data=str(
                                                          'a' + c.name))
        keyboard.add(callback_button1)
    if player.chat_id == 379168159 or player.name == 'Пасюк' or player.chat_id == 197216910:
        callback_button1 = types. \
            InlineKeyboardButton(text=Weapon_list.iceman.name, callback_data=str('a' + str(Weapon_list.iceman.name)))
        callback_button2 = types. \
            InlineKeyboardButton(text=Weapon_list.olovlis.name, callback_data=str('a' + str(Weapon_list.olovlis.name)))
        keyboard.add(callback_button1)
        keyboard.add(callback_button2)   
    if player.chat_id == 668071459 or player.name == 'Пасюк' or player.chat_id == 197216910:
        callback_button1 = types. \
            InlineKeyboardButton(text=Weapon_list.iceman.name, callback_data=str('a' + str(Weapon_list.iceman.name)))
        callback_button2 = types. \
            InlineKeyboardButton(text=Weapon_list.olovlis.name, callback_data=str('a' + str(Weapon_list.olovlis.name)))
        keyboard.add(callback_button1)
        keyboard.add(callback_button2)          
    bot.send_message(player.chat_id, 'Qurolni tanlang.',
                     reply_markup=keyboard)


def actor_from_id(cid, game):
    player = game.player_dict[int(cid)]
    return player


def player_info(player, cid=None):
    player.info.add(player.name)
    if special_abilities.Zombie not in player.abilities:
        player.info.add(u'\U00002665'*player.hp + "|" + str(player.hp) + ' jon. Maksimum: ' + str(player.maxhp))
        player.info.add(
            u'\U000026A1'*player.energy + "|" + str(player.energy) + ' energiya. Maksimum: ' + str(player.maxenergy)
            )
        player.info.add(
            u'\U0001F494' + 'x' + str(player.toughness) + "|" + str(player.toughness) + ' jaroxatlar. Jon yo`qotishga ta`sir etadi'
            )
    else:
        player.info.add(u'\U0001F356' * player.hungercounter + "|" + str(player.hungercounter)
                        + ' ochlik. Maksimum: ' + str(player.maxhp))
    tempabilities = []
    for x in player.abilities:
        tempabilities.append(x)
    if tempabilities:
        player.info.add("Qobiliyatlar: " + ", ".join([x.name for x in tempabilities]))
    templist = []
    for x in player.itemlist:
        if x.standart:
            templist.append(x)
    if templist:
        player.info.add("Jihozlar: " + ", ".join([x.name for x in templist]))
    player.info.add("Qurollar: " + player.weapon.name + ' - ' + player.weapon.damagestring)
    if player.weapon == Weapon_list.bow:
        player.info.add(
            u'\U0001F3AF' + " | Tegish ehtimolligi - " + str(int(get_hit_chance(player, player.bonusaccuracy)))
            + '%')
    else:
        player.info.add(u'\U0001F3AF' + " | Tegish ehtimolligi - " + str(int(get_hit_chance(player, 0)))
                        + '%')
    if cid is None:
        if player.weapon == Weapon_list.sniper and player.aimtarget is not None:
            player.info.add(u'\U0001F3AF' + " |" 'Tegish ehtimolligi '
                            + actor_from_id(player.aimtarget, player.game).name + 'ga - '
                            + str(int(get_hit_chance(player, player.bonusaccuracy))) + '%')

        player.info.post(bot, 'Ma`lumot')
    else:
        player.info.post(bot, 'Ma`lumot', cid=cid)


def player_turn_info(player):
    player.info.add('Yurish ' + str(player.fight.round))
    if special_abilities.Zombie not in player.abilities:
        player.info.add(u'\U00002665'*player.hp + "|" + str(player.hp) + ' jon. Maksimum: ' + str(player.maxhp))
        player.info.add(
            u'\U000026A1'*player.energy + "|" + str(player.energy) + ' energiya. Maksimum: ' + str(player.maxenergy)
            )
    else:
        player.info.add(u'\U0001F356'*player.hungercounter + "|" + str(player.hungercounter)
                        + ' ochlik. Maksimum: ' + str(player.maxhp))
    if player.weapon == Weapon_list.bow:
        player.info.add(
            u'\U0001F3AF' + " | Tegish ehtimolligi - " + str(int(get_hit_chance(player, player.bonusaccuracy)))
            + '%')
    else:
        player.info.add(u'\U0001F3AF' + " | Nishonga tegish ehtimolligi - " + str(int(get_hit_chance(player, 0)))
                        + '%')
    if player.weapon == Weapon_list.sniper:
        if player.aimtarget is not None:
            player.info.add(u'\U0001F3AF' + " |" 'Tegish ehtimolligi '
                            + actor_from_id(player.aimtarget, player.game).name + 'ga - '
                            + str(int(get_hit_chance(player, player.bonusaccuracy))) + '%')
    return player.info


def get_hit_chance(player, bonus):
    hitdice = 10 - player.energy - player.weapon.bonus - player.accuracy - bonus - player.tempaccuracy
    onechance = 100 - (10*hitdice)
    if hitdice >= 10 or player.energy == 0:
        if special_abilities.Zombie not in player.abilities:
            onechance = 0
    elif hitdice <= 0:
        onechance = 100
        return onechance
    dmax = player.weapon.dice
    d = 1
    tempchance = onechance
    while d != dmax:
        tempchance += (100 - tempchance) * (onechance/100)
        d += 1
    return tempchance


def apply_damage(targets):
    for p in targets:
        if p.damagetaken != 0:
            p.Losthp = True
            loss = p.damagetaken//p.toughness
            p.hploss += loss
            p.hp -= p.hploss
            p.team.losthp += p.hploss
            p.fight.string.add(u'\U00002665' * p.hp + ' |' + str(p.name) +
                                   " yo`qotayabdi " + str(p.hploss) + " jon. Qoldi " + str(p.hp) + " jon.")


def teamchat(text, player):
    player.message = u'\U00002757' + "| " + player.name + ": " + text
    return str(player.name + ' nimadir deyabdi.')


def get_game_from_chat(cid):
    try:
        return Main_classes.existing_games[cid]
    except KeyError:
        return None


def get_game_from_player(cid):
    try:
        return Main_classes.dict_players[cid]
    except KeyError:
        print('O`yinchi topilmadi!')
        return None


def send_inventory(player):
    keyboard = types.InlineKeyboardMarkup()
    for p in player.itemlist:
        Aviable = True
        if p.id[0:5] == 'iteme' and player.energy < 2:
            Aviable = False
        if Aviable:
            keyboard.add(types.InlineKeyboardButton(text=p.name, callback_data=str(p.id + str(player.fight.round))))
    keyboard.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('cancel')))
    bot.send_message(player.chat_id, 'Jihozni tanlang.', reply_markup=keyboard)


def send_skills(player):
    keyboard = types.InlineKeyboardMarkup()
    for p in player.itemlist:
        if not p.standart:
            keyboard.add(types.InlineKeyboardButton(text=p.name, callback_data=str(p.id + str(player.fight.round))))
    keyboard.add(types.InlineKeyboardButton(text='Bekor qilish', callback_data=str('cancel')))
    bot.send_message(player.chat_id, 'Qobiliyatni tanlang.', reply_markup=keyboard)


def delete_game(game):
    for p in game.pending_players:
        try:
            del Main_classes.dict_players[p.chat_id]
        except KeyError:
                pass
    try:
        del Main_classes.existing_games[game.cid]
    except KeyError:
        pass
    try:
        del game
    except:
        pass



def check_secrets_abilities(p):
    secret_abilities.check_ability(p)


def damage(source, target, damage, type):
    target.attackers.append(source)
    for a in target.abilities:
        a.ondamage(a, source, target, damage, type)
    target.damagetaken += damage


def get_weapon_from(name):
    for weapon in Weapon_list.fullweaponlist:
        if weapon.name == name:
            return weapon


def get_weaponlist():
    return Weapon_list.weaponlist


def get_item_from(id):
    return Item_list.items[id]


def get_skill_from(name):
    for ability in special_abilities.abilities:
        if ability.name == name:
            return ability
