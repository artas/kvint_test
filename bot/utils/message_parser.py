from yargy import or_, rule, Parser, and_
from yargy.predicates import dictionary
from yargy.interpretation import fact


async def parse_message(message: str) -> dict:
    """
    Возращает распарсенные сущности
    :param message: Текст сообщения
    :return: словарь сущносте
    """
    Pizza = fact(
        'Pizza',
        ['size', 'payment']
    )
    _BIG = {
        'большая', 'большую'
    }
    _SMALL = {'маленькая', 'маленькую'}
    BIG = dictionary(_BIG)
    SMALL = dictionary(_SMALL)
    SIZE = or_(BIG, SMALL).interpretation(Pizza.size)
    _PAYMENT = ['наличкой', 'налом', 'безнал', 'картой', 'по карте']
    PAYMENT = dictionary(_PAYMENT).interpretation(Pizza.payment)
    PIZZA = or_(
        rule(SIZE),
        rule(SIZE, 'пицца', 'пиццу'),
        rule(SIZE, 'пицца', 'пиццу', 'оплата', PAYMENT),
        rule(PAYMENT),
        rule('оплата', PAYMENT)
    ).interpretation(Pizza)

    parser = Parser(PIZZA)
    matches = []
    for match in parser.findall(message):
        matches.append(match.fact)
    match_entity = {}
    for match in matches:
        if match.size:
            match_entity['size'] = match.size
        else:
            match_entity['payment'] = match.payment
    return match_entity
