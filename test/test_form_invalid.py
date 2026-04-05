from models.register import RegisterModel


def test_form_invalid_required_name(form_page, base_url):
    form_page.open(base_url)

    user = RegisterModel().random()
    message_text = form_page.build_message_from_tools()

    form_page.fill_password(user["password"]) \
        .select_milk() \
        .select_coffee() \
        .select_yellow() \
        .select_automation("undecided") \
        .fill_email(user["email"]) \
        .fill_message(message_text) \
        .click_submit()

    assert form_page.has_alert() is False
    assert form_page.get_active_element_id() == "name-input"
    assert form_page.get_name_required_error_text() == "* Required"
    assert form_page.get_name_validation_message() != ""
