from transitions import Machine


class StateManager:
    states = ['choice_pizza', 'choice_payment', 'confirmation']

    def __init__(self, chat_id: int = 0):
        self.chat_id = chat_id
        self.payment = None
        self.pizza = None
        self.message = None

        self.machine = Machine(model=self, states=StateManager.states,
                               initial='choice_pizza')

        self.machine.add_transition(trigger='chose_pizza',
                                    source='choice_pizza',
                                    dest='choice_payment')
        self.machine.add_transition(trigger='chose_payment',
                                    source='*', dest='confirmation')
        self.machine.add_transition(trigger='confirmed',
                                    source='confirmation', dest='choice_pizza')
        self.machine.add_transition(trigger='restart',
                                    source='*', dest='choice_pizza')
