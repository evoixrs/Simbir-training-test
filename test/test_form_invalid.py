from models.register import RegisterModel


def test_form_invalid_required_name(form_page, base_url):
    """Открываем страницу формы"""
    form_page.open(base_url)

    """Генерируем тестовые данные и текст для поля Message"""
    user = RegisterModel().random()
    message_text = form_page.build_message_from_tools()

    """Поле Name не заполняет, чтобы проверить обязательность поля"""
    form_page.fill_password(user["password"]) \
        .select_milk() \
        .select_coffee() \
        .select_yellow() \
        .select_automation("undecided") \
        .fill_email(user["email"]) \
        .fill_message(message_text) \
        .click_submit()

    """Форма не отправляется, alert не появляется,
    фокус остается в Name, есть ошибка"""
    assert form_page.has_alert() is False
    assert form_page.get_active_element_id() == "name-input"
    assert form_page.get_name_required_error_text() == "* Required"
    assert form_page.get_name_validation_message() != ""
