from models.register import RegisterModel

"""Генерация тестовых данных Юзера через Faker"""
def test_form_valid(form_page):
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
