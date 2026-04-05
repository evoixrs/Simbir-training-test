from models.register import RegisterModel


def test_form_valid(form_page, base_url):
    form_page.open(base_url)

    user = RegisterModel().random()
    tools = form_page.get_automation_tools()
    expected_message_text = f"{len(tools)}, {max(tools, key=len)}"

    form_page.fill_name(user["name"]) \
        .fill_password(user["password"]) \
        .select_milk() \
        .select_coffee() \
        .select_yellow() \
        .select_automation("undecided") \
        .fill_email(user["email"]) \
        .fill_message(expected_message_text)

    assert form_page.build_message_from_tools() == expected_message_text
    assert form_page.get_message_value() == expected_message_text

    form_page.submit()

    assert form_page.get_alert_text() == "Message received!"
    form_page.accept_alert()
