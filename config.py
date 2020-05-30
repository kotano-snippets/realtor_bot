# RIELTOR_SPBSTU_BOT
# bot_username = '@rieltor_spbstu_bot'
# token = '1034733347:AAFFVYmKbVAVnz3GvTLXF5BOCOr8iCuTkzE'
# admin = 905484789  # TeaTskaya ID
# admin = 529665735  # Admin ID Telegram

# KOTPYBOT FOR TESTING
bot_username = '@kotpybot'
token = '821235624:AAFlR4yJHGaEYP725DRXBFHKqwV6uxA-DB0'
admin = 732101811


allow_proxy = True

with open('proxies.txt') as pf:
    lst = []
    for line in pf:
        lst.append(line.strip())
proxies = iter(lst)
