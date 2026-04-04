
from models.register import RegisterModel


def test_form_valid(form_page, base_url):
    """Открывем страницу формы"""
    form_page.open(base_url)

    """Генерация тестовых данных Юзера через Faker"""
    user = RegisterModel().random()

    """Формируем текст для поля Message из списка Automation tools"""
    message_text = form_page.build_message_from_tools()

    """Заполняем форму данными"""
    form_page.fill_name(user["name"]) \
        .fill_password(user["password"]) \
        .select_milk() \
        .select_coffee() \
        .select_yellow() \
        .select_automation("undecided") \
        .fill_email(user["email"]) \
        .fill_message(message_text) \
        .submit()

    """Проверяем текст alert после отправки Submit"""
    assert form_page.get_alert_text() == "Message received!"

    """Закрываем alert"""
    form_page.accept_alert()
