import requests


REQUEST_USERDATA = 'https://api.worldoftanks.eu/wot/account/list/?application_id=84eadd715b6a76c74b542268fc56d2c4'
REQUEST_USER_TANKS = 'https://api.worldoftanks.eu/wot/account/tanks/?application_id=84eadd715b6a76c74b542268fc56d2c4'
REQUEST_TANK_NAME = 'https://api.worldoftanks.eu/wot/encyclopedia/vehicles/?application_id=84eadd715b6a76c74b542268fc56d2c4'
REQUEST_CLAN_INFO = 'https://api.worldoftanks.eu/wot/account/info/?application_id=84eadd715b6a76c74b542268fc56d2c4'
REQUEST_CLAN_STATS = 'https://api.worldoftanks.eu/wot/globalmap/claninfo/?application_id=84eadd715b6a76c74b542268fc56d2c4'


def get_userid(name):
    response = requests.get(REQUEST_USERDATA + f'&search={name}').json()
    try:
        if (len(response['data']) > 1):
            print(response['data'])
            account_id = int(input('Add meg az account id-jét a találtak közül:\n'))
        else:
            account_id = int(response['data'][0]['account_id'])

        while (True):
            for value in response['data']:
                if value['account_id'] == account_id:
                    return account_id
            print('Hibás account id-t adott meg.')
            print('Kérem adja meg helyesen az account id-t.')
            print(response['data'])
            account_id = int(input())

    except:
        print('Nincs ilyen felhasználó')
        user_name = input('Adja meg helyesen a Játékos nevét:\n')
        return get_userid(user_name)


def get_mastery_class(number):
    if int(number) == 4:
        return "Ace Tanker"
    elif int(number) == 3:
        return "First Class"
    elif int(number) == 2:
        return "Second Class"
    elif int(number) == 1:
        return "Third Class"
    else:
        return "None"


def get_Tank_name_by_id(name):
    index = name.find('_')
    return name[index + 1:]


def get_statistics_by_Tanks(response):
    tank_names = list()
    mark_of_mastery = list()
    all_battle = list()
    winrate = list()
    tank_id=set()

    for values in response:
        all_battle.append(str(values['statistics']['battles']))
        mark_of_mastery.append(get_mastery_class(values['mark_of_mastery']))
        tank_id.add(str(values['tank_id']))
        if int(values['statistics']['wins']) == 0:
            winrate.append('0%')
        else:
            winrate.append(str(int((values['statistics']['wins'] / values['statistics']['battles']) * 100)) + '%')
    tank_id=list(tank_id)
    session= requests.Session()
    for x in range(len(tank_id)):
        response = session.get(REQUEST_TANK_NAME+f'&tank_id={tank_id[x]}').json()
        try:
            tank_names.append(get_Tank_name_by_id(response['data'][tank_id[x]]['tag']))
        except:
            print(end='')


    return tank_names, mark_of_mastery, winrate, all_battle


def create_table(tank_name, mark_of_mastery, winrate, all_battle):
    max_tank_name_len = 0
    max_winrate_len = 0
    max_allbattle_len = 0

    for x in range (0,len(tank_name)):
        if(max_tank_name_len<len(tank_name[x])):
            max_tank_name_len=len(tank_name[x])
        if (max_winrate_len < len(winrate[x])):
            max_winrate_len = len(winrate[x])
        if (max_allbattle_len < len(all_battle[x])):
            max_allbattle_len = len(all_battle[x])
    for x in range(0,len(tank_name)):
        while max_tank_name_len>len(tank_name[x]):
            tank_name[x]+=' '
        winrate[x]=str(winrate[x])
        while max_winrate_len > len(winrate[x]):
            winrate[x]+=' '
        all_battle[x]=str(all_battle[x])
        while max_allbattle_len> len(all_battle[x]):
            all_battle[x]+=' '
    for x in range(0, len(tank_name)):
        print(tank_name[x] + '\t ' + winrate[x] + '\t ' + all_battle[x] + '\t ' + mark_of_mastery[x] + '\n')


def user_tanks(account_id):
    response = requests.get(REQUEST_USER_TANKS + f'&account_id={account_id}').json()


    (tank_name, mark_of_mastery, winrate, all_battle) = get_statistics_by_Tanks(response['data'][account_id])
    create_table(tank_name, mark_of_mastery, winrate, all_battle)


def user_clan_info(account_id):
    response = requests.get(REQUEST_CLAN_INFO + f'&account_id={account_id}').json()
    clan_id = str(response['data'][account_id]['clan_id'])
    try:
        response = requests.get(REQUEST_CLAN_STATS + f'&clan_id={clan_id}').json()
        clan_name = response['data'][clan_id]['name']
        clan_tag = response['data'][clan_id]['tag']
        clan_t10_elo = response['data'][clan_id]['ratings']['elo_10']
        clan_t8_elo = response['data'][clan_id]['ratings']['elo_8']
        clan_t6_elo = response['data'][clan_id]['ratings']['elo_6']
        print("Klán név: " + clan_name)
        print("Klán rövidítés: " + clan_tag)
        print("Klán T10 elo: " + str(clan_t10_elo))
        print("Klán T8 elo: " + str(clan_t8_elo))
        print("Klán T6 elo: " + str(clan_t6_elo))
    except:
        print("A játékosnak nincs klánja!")


def main():
    ujra = 'yes'
    valasz_lista = ['Yes', 'yes', 'yep', 'y']
    while ujra in valasz_lista:
        user_name = input('Adja meg a Játékos nevét:\n')
        account_id = str(get_userid(user_name))
        valasz = input("Szeretné tudni a játékos tankjainak a listáját és a statisztikáit?[Yes, yes, yep, y]\n")

        if (valasz in valasz_lista):
            print("Tank name\t Winrate\t Battles\t Mark of mastery")
            print()
            user_tanks(account_id)
        valasz = input('Szeretné tudni a játékos Klánjának a statisztikáit?[Yes, yes, yep, y]\n')
        if valasz in valasz_lista:
            user_clan_info(account_id)
        ujra = input("Szeretne új játékost keresni?[Yes, yes, yep, y]\n")


if __name__ == '__main__':
    main()
