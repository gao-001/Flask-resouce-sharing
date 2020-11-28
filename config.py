# 定时任务配置
class Schedule():
    JOBS = [
        {
            'id': 'get_movie',
            'func': 'schedule:get_movie',
            'args': None,
            'trigger': 'interval',
            'days': 5
        },
        {
            'id': 'get_playlist',
            'func': 'schedule:get_playlist',
            'args': None,
            'trigger': 'interval',
            'days': 2
        },
        {
            'id': 'get_vip_music',
            'func': 'schedule:get_vip_music',
            'args': None,
            'trigger': 'interval',
            'hours': 10
        },

    ]
