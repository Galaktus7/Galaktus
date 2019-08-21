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
