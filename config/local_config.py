import ujson

with open("config/config.json", "r") as cfg_file:
    settings = ujson.load(cfg_file)

    generalSettings     = settings['general_settings']
    authUserList        = generalSettings['auth_user_list']
    prefix              = generalSettings['prefix']

    tokenSettings       = settings['tokens']
    masterToken         = tokenSettings['master']
    workerTokens        = tokenSettings['workers']
