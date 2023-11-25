from aiogram.fsm.state import State, StatesGroup


class StepsForm(StatesGroup):
    """Состояния для машины состояний."""
    CHOOSE_CAFE = State()
    CAFE_INFO = State()
    MENU_WATCH = State()
    CAFE_ADDRESS = State()
    CHOOSE_DATE = State()
    PERSON_AMOUNT = State()
    NO_FREE_TABLE = State()
    CHOOSE_ANOTHER_CAFE = State()
    NAME_STATE = State()
    PHONE_STATE = State()
    ORDER_STATE = State()
    IN_ORDER_STATE = State()
    ORDER_CHECK_PAY = State()
    PAY_STATE = State()
    FINAL_STATE = State()
    REMINDER_STATE = State()
    ERROR = State()
