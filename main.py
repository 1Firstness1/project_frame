"""Точка запуска сервиса управления списком гостей."""

from typing import List

from storage import (
    load_events,
    save_events,
    load_guests,
    save_guests,
    load_statuses,
    save_statuses,
    load_invitations,
    save_invitations,
)
from utils import input_int
from models import Event, Guest, Status, Invitation
from models.events import (
    add_event,
    find_event_by_id,
    find_events,
    sort_events_by_places,
    show_events,
)
from models.guests import (
    add_guest,
    find_guest_by_id,
    find_guests,
    count_adults,
    sort_guests_by_age,
    show_guests,
)
from models.statuses import (
    find_status_by_code,
    show_statuses,
    CODE_PENDING,
    CODE_CONFIRMED,
    CODE_DECLINED,
)
from models.invitations import (
    create_invitation,
    confirm_invitation,
    decline_invitation,
    cancel_invitation,
    count_confirmed,
    find_invitations_by_event,
    show_invitations,
)

EVENTS_FILE = "data/events.json"
GUESTS_FILE = "data/guests.json"
STATUSES_FILE = "data/statuses.json"
INVITATIONS_FILE = "data/invitations.json"


def create_new_invitation(
    invitations: List[Invitation],
    events: List[Event],
    guests: List[Guest],
    statuses: List[Status],
) -> None:
    """Пользовательский сценарий создания приглашения."""
    event_id = input_int("ID события: ")
    event = find_event_by_id(events, event_id)
    if event is None:
        print("Событие не найдено.")
        return

    guest_id = input_int("ID гостя: ")
    guest = find_guest_by_id(guests, guest_id)
    if guest is None:
        print("Гость не найден.")
        return

    pending_status = find_status_by_code(statuses, CODE_PENDING)
    if pending_status is None:
        print("Статус 'ожидает' не найден.")
        return

    invitation = create_invitation(invitations, event, guest, pending_status)
    if invitation is None:
        print("Гость уже приглашён на это событие.")
        return

    save_invitations(INVITATIONS_FILE, invitations)
    print(f"Приглашение создано: {invitation}")


def show_event_statistics(
    invitations: List[Invitation],
    events: List[Event],
    guests: List[Guest],
) -> None:
    """Показать статистику по событию."""
    event_id = input_int("ID события: ")
    event = find_event_by_id(events, event_id)
    if event is None:
        print("Событие не найдено.")
        return

    confirmed = count_confirmed(invitations, event)
    all_inv = find_invitations_by_event(invitations, event)
    print(f"Событие: {event.name}")
    print(f"Всего приглашений: {len(all_inv)}")
    print(f"Подтверждено: {confirmed}")
    print(f"Свободных мест: {event.places - confirmed}")
    print(f"Совершеннолетних гостей: {count_adults(guests)}")


def menu(
    events: List[Event],
    guests: List[Guest],
    statuses: List[Status],
    invitations: List[Invitation],
) -> None:
    """Основной цикл меню приложения."""
    while True:
        print("\n=== Сервис управления списком гостей ===")
        print("1. Показать события")
        print("2. Показать гостей")
        print("3. Показать статусы")
        print("4. Показать приглашения")
        print("5. Добавить событие")
        print("6. Добавить гостя")
        print("7. Пригласить гостя на событие")
        print("8. Подтвердить приглашение")
        print("9. Отклонить приглашение")
        print("10. Отменить приглашение")
        print("11. Найти гостя")
        print("12. Статистика по событию")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_events(sort_events_by_places(events))
        elif choice == "2":
            show_guests(sort_guests_by_age(guests))
        elif choice == "3":
            show_statuses(statuses)
        elif choice == "4":
            show_invitations(invitations)
        elif choice == "5":
            name = input("Название события: ")
            date_str = input("Дата (ГГГГ-ММ-ДД): ")
            places = input_int("Количество мест: ")
            add_event(events, name, date_str, places)
            save_events(EVENTS_FILE, events)
            print("Событие добавлено.")
        elif choice == "6":
            name = input("Имя гостя: ")
            age = input_int("Возраст: ")
            add_guest(guests, name, age)
            save_guests(GUESTS_FILE, guests)
            print("Гость добавлен.")
        elif choice == "7":
            create_new_invitation(invitations, events, guests, statuses)
        elif choice == "8":
            invitation_id = input_int("ID приглашения: ")
            confirmed = find_status_by_code(statuses, CODE_CONFIRMED)
            if confirmed is None:
                print("Статус 'подтверждено' не найден.")
                continue
            if confirm_invitation(invitations, invitation_id, confirmed):
                save_invitations(INVITATIONS_FILE, invitations)
                print("Приглашение подтверждено.")
            else:
                print("Приглашение не найдено.")
        elif choice == "9":
            invitation_id = input_int("ID приглашения: ")
            declined = find_status_by_code(statuses, CODE_DECLINED)
            if declined is None:
                print("Статус 'отклонено' не найден.")
                continue
            if decline_invitation(invitations, invitation_id, declined):
                save_invitations(INVITATIONS_FILE, invitations)
                print("Приглашение отклонено.")
            else:
                print("Приглашение не найдено.")
        elif choice == "10":
            invitation_id = input_int("ID приглашения: ")
            if cancel_invitation(invitations, invitation_id):
                save_invitations(INVITATIONS_FILE, invitations)
                print("Приглашение отменено.")
            else:
                print("Приглашение не найдено.")
        elif choice == "11":
            query = input("Подстрока имени: ")
            show_guests(find_guests(guests, query))
        elif choice == "12":
            show_event_statistics(invitations, events, guests)
        elif choice == "0":
            print("Выход.")
            break
        else:
            print("Неизвестная команда.")


def main() -> None:
    """Точка входа приложения."""
    events = load_events(EVENTS_FILE)
    guests = load_guests(GUESTS_FILE)
    statuses = load_statuses(STATUSES_FILE)
    invitations = load_invitations(
        INVITATIONS_FILE, events, guests, statuses
    )

    try:
        menu(events, guests, statuses, invitations)
    finally:
        save_events(EVENTS_FILE, events)
        save_guests(GUESTS_FILE, guests)
        save_statuses(STATUSES_FILE, statuses)
        save_invitations(INVITATIONS_FILE, invitations)


if __name__ == "__main__":
    main()