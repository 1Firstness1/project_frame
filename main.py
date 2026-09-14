from datetime import date


EVENT_NAME = "День рождения"
EVENT_DATE = date(2026, 10, 15)
EVENT_PLACES = 10


def get_invitation_status(is_confirmed):
    if is_confirmed:
        return "Приглашение подтверждено"
    return "Приглашение ожидает подтверждения"


def can_add_guest(current_guests, places):
    if current_guests < places:
        return True
    return False


def build_guest_card(name, age, is_confirmed, current_guests, places):
    status = get_invitation_status(is_confirmed)

    if age < 18:
        age_note = "Гость несовершеннолетний — нужен сопровождающий"
    else:
        age_note = "Гость совершеннолетний"

    if can_add_guest(current_guests, places):
        place_note = "Место доступно"
    else:
        place_note = "Свободных мест нет"

    return (
        f"Гость: {name}\n"
        f"Возраст: {age}\n"
        f"Статус: {status}\n"
        f"Примечание: {age_note}\n"
        f"Места: {place_note}"
    )


def main():
    print(f"Событие: {EVENT_NAME}")
    print(f"Дата: {EVENT_DATE}")
    print(f"Всего мест: {EVENT_PLACES}")
    print("-" * 30)

    guest_name = "Иван Петров"
    guest_age = int("17")
    is_confirmed = True
    current_guests = 5

    card = build_guest_card(
        guest_name, guest_age, is_confirmed, current_guests, EVENT_PLACES
    )
    print(card)
    print("-" * 30)

    guest_name_2 = "Мария Смирнова"
    guest_age_2 = int("25")
    is_confirmed_2 = False
    current_guests_2 = 10

    card_2 = build_guest_card(
        guest_name_2, guest_age_2, is_confirmed_2, current_guests_2, EVENT_PLACES
    )
    print(card_2)


if __name__ == "__main__":
    main()