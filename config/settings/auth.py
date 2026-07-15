# Настройки самой регистрации 

#Типо устарело, поэтому пишут вместо него signup_fields(пока без первого параметра "email")
#ACCOUNT_EMAIL_REQUIRED = False # Пока не требуем email

ACCOUNT_SIGNUP_FIELDS = ['username*', 'password1*', 'password2*']
ACCOUNT_EMAIL_VERIFICATION = 'none' # Не отправляем письмо с подтверждением

# SOCIALACCOUNT_PROVIDERS = {
#     'vk': {
#         'SCOPE': ['email'], # Запрашиваем доступ к почте
#         'AUTH_PARAMS': {'v': '5.131'}, # Версия API ВК
#     }
# }

SOCIALACCOUNT_PROVIDERS = {
    'yandex': {
        'SCOPE': ['login:email', 'login:info', 'login:avatar'],
    }
}