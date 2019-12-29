def load():
    path_settings = "settings.txt"
    file = open(path_settings, 'r')
    settings_str = file.read()
    settings_list = settings_str.split("\n")

    TWITCH_HOST = settings_list[0].split("=")[1]
    TWITCH_PORT = int(settings_list[1].split("=")[1])
    USERNAME = settings_list[2].split("=")[1]
    OAUTH = settings_list[3].split("=")[1]
    CHANNEL = settings_list[4].split("=")[1]
    LOGGING = settings_list[5].split("=")[1]
    LOCAL = settings_list[6].split("=")[1]
    LOCAL_IP = settings_list[7].split("=")[1]

    settings = {}
    settings['TWITCH_HOST'] = TWITCH_HOST
    settings['TWITCH_PORT'] = TWITCH_PORT
    settings['USERNAME'] = USERNAME
    settings['OAUTH'] = OAUTH
    settings['CHANNEL'] = CHANNEL
    settings['LOGGING'] = LOGGING
    settings['LOCAL'] = LOCAL
    settings['LOCAL_IP'] = LOCAL_IP

    return settings
