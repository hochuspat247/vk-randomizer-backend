# Вспомогательные функции

def getRoleDisplayName(role: str) -> str:
    return {
        "owner": "Владелец",
        "admin": "Администратор",
        "editor": "Редактор",
        "moderator": "Модератор",
        "member": "Участник",
        "advertiser": "Рекламодатель"
    }.get(role, "Неизвестная роль")
