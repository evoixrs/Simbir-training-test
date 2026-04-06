# Simbir Training Test

UI-автотесты для формы `https://practice-automation.com/form-fields/`, выполненные в рамках тестового задания SDET от SimbirSoft.

## Стек

- Python 3.12
- Pytest
- Selenium WebDriver
- Chrome
- Faker
- Allure
- GitHub Actions

## Покрытие

### Позитивный тест-кейс

Название: Успешная отправка формы с валидными данными

Шаги:
1. Открыть страницу формы
2. Заполнить `Name`
3. Заполнить `Password`
4. Выбрать `Milk` и `Coffee`
5. Выбрать `Yellow`
6. Выбрать значение в `Do you like automation?`
7. Заполнить `Email` в формате `name@example.com`
8. Сформировать `Message` как количество инструментов из списка `Automation tools` и инструмент с самым длинным названием
9. Нажать `Submit`

Ожидаемый результат:
- поле `Message` заполнено корректным значением
- появляется alert с текстом `Message received!`

### Негативный тест-кейс

Название: Отправка формы с пустым обязательным полем `Name`

Шаги:
1. Открыть страницу формы
2. Оставить поле `Name` пустым
3. Заполнить остальные поля валидными значениями
4. Нажать `Submit`

Ожидаемый результат:
- форма не отправляется
- под полем `Name` отображается ошибка `* Required`

## Структура проекта

- `.github/workflows/ci.yml` — GitHub Actions workflow для запуска тестов
- `docs/` — PDF с ТЗ и скриншот Allure-отчета
- `locators/` — локаторы страницы формы
- `models/` — модель и генерация тестовых данных через Faker
- `pages/base_page.py` — базовые действия с элементами и страницей
- `pages/form_page.py` — page object формы
- `test/conftest.py` — fixtures, запуск Chrome, Allure attachments
- `test/test_form_valid.py` — позитивный сценарий
- `test/test_form_invalid.py` — негативный сценарий
- `pytest.ini` — конфигурация pytest и логирования
- `requirements.txt` — зависимости проекта

## Подходы

- `Page Object Model` — действия и проверки инкапсулированы в `FormPage`
- `Factory-style organization` — локаторы вынесены в `FormPageLocators`, общие действия собраны в `BasePage`
- `Fluent Interface` — методы заполнения и выбора значений возвращают `self`

## Запуск тестов

Установка зависимостей:

Windows:

```powershell
pip install -r requirements.txt
```

macOS:

```bash
python3 -m pip install -r requirements.txt
```

Запуск всех тестов:

Windows:

```powershell
pytest
```

macOS:

```bash
pytest
```

Запуск отдельного теста:

Windows:

```powershell
pytest test/test_form_valid.py
pytest test/test_form_invalid.py
```

macOS:

```bash
pytest test/test_form_valid.py
pytest test/test_form_invalid.py
```

## Allure

Генерация результатов:

Windows:

```powershell
pytest --alluredir=allure-results
```

macOS:

```bash
pytest --alluredir=allure-results
```

Открытие отчета:

Windows:

```powershell
allure serve allure-results
```

macOS:

```bash
allure serve allure-results
```

Скриншот отчета добавлен в проект:

[`docs/screenshots/Allure_Screenshots.jpg`](docs/screenshots/Allure_Screenshots.jpg)

## CI

В проекте настроен GitHub Actions workflow для автоматического запуска тестов при `push` и `pull_request` в `main`.

Workflow:

[`ci.yml`](.github/workflows/ci.yml)
