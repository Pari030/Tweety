import configparser


class Config:
    _config = configparser.ConfigParser()
    _config.read('config.ini')
    _settings = _config['settings']

    debug = bool(_settings['debug'])
    session_id = _settings['ig_session_id']

    if debug:
        host = 'localhost'
        port = 80
    else:
        host = '0.0.0.0'
        port = 7777
