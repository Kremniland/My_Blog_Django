from django.utils.deprecation import MiddlewareMixin

import threading # Для работы с многопоточностью


# Создаем файловое хранилище
_local_storage = threading.local()


class CurrentRequestMiddlewareUser(MiddlewareMixin):
    '''Переопределяем process_request из MiddlewareMixin
    получаем request страницы на которой находимся'''
    def process_request(self, request):
        '''Сохраняем request в файловое хранилище'''
        _local_storage.request = request


def get_current_request():
    '''Если в хранилище нет request вернем None'''
    return getattr(_local_storage, 'request', None)


def get_current_user():
    '''Получаем request если содержит None вернем None,
    а если есть вернем user из request'''
    request = get_current_request()
    if request is None:
        return None
    return getattr(request, 'user', None)
