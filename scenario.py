from bot.utils.message_parser import parse_message


# Идея заключается в том, чтобы не привязывать объект TelegramBot к какому то
# конкретному сценарию, и можно было бы потом менять сценарии
async def message_handler(base, chat_id: int):
    message = base.memory_store[chat_id].message.lower()
    state = base.memory_store[chat_id].state
    parse = await parse_message(message)
    size = parse.get('size')
    payment = parse.get('payment')
    if message == '/start':
        await base.send_message(chat_id,
                                'Какую вы хотите пиццу? '
                                'Большую или маленькую?')

    elif state == 'choice_pizza':
        if size and payment:
            # тут подразумевается, что клиент
            # может сразу сказать в фразе необходимые сущности.
            # Тогда сразу переходим к финалу
            base.memory_store[chat_id].pizza = size
            base.memory_store[chat_id].payment = payment

            await base.send_message(chat_id,
                                    f'Вы хотите {base.memory_store[chat_id].pizza} пиццу,'
                                    f' оплата - {base.memory_store[chat_id].payment}?')
            base.memory_store[chat_id].chose_payment()
        elif size:
            base.memory_store[chat_id].pizza = size
            await base.send_message(chat_id,
                                    'Как вы будете платить?')
            base.memory_store[chat_id].chose_pizza()
        else:
            await base.send_message(chat_id,
                                    'Не понимаю.'
                                    'Какую вы хотите пиццу? '
                                    'Большую или маленькую?'
                                    )
    elif state == 'choice_payment':
        if payment:
            base.memory_store[chat_id].payment = payment
            await base.send_message(chat_id,
                                    f'Вы хотите {base.memory_store[chat_id].pizza} пиццу,'
                                    f' оплата - {base.memory_store[chat_id].payment}?')
            base.memory_store[chat_id].chose_payment()
        else:
            await base.send_message(chat_id, 'Не понимаю.'
                                             'Как вы будете платить?')
    elif state == 'confirmation':
        if message.lower() in ['да', 'ога', 'угу', 'верно']:
            await base.send_message(chat_id, 'Спасибо за заказ')
            base.memory_store[chat_id].confirmed()
            base.memory_store.pop(chat_id, None)
        elif message.lower() in ['нет', 'неа']:
            await base.send_message(chat_id,
                                    'Какую вы хотите пиццу? '
                                    'Большую или маленькую?')
            base.memory_store[chat_id].restart()
        else:
            await base.send_message(chat_id, 'Не понимаю.'
                                             f'Вы хотите {base.memory_store[chat_id].pizza} пиццу,'
                                             f' оплата - {base.memory_store[chat_id].payment}?')
