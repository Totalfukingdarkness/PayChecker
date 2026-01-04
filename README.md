# PayChecker
Данный скрипт позволяет просмотреть актуальную статистику по средней заработной плате, среди разработчиков 8 самых популярных языков программирования.

## Как установить
Python 3.10+ должен быть уже установлен.

Затем используйте `pip` для установки зависимостей:
```
pip install -r requirements.txt
```
Для разработки использовалась Python 3.10.

## Переменные окружения
Требуется создать файл `.env` и прописать переменные окружения:
- SJ_SECRET_KEY=your_superjob_secret_key
- SJ_ACCESS_TOKEN=your_superjob_access_token

Способ их получения [здесь](https://api.superjob.ru/#gettin).

## Скрипты и их запуск
Для запуска, введите в консоль:
```
python main.py
```
Программа обрабатывает заработные платы вакансий в г.Москва по языкам программирования:
- Python 
- Javascript
- 1C
- ruby
- C
- C#
- C++
- PHP

Пример вывода:

<img width="999" height="650" alt="image" src="https://github.com/user-attachments/assets/b60a6f13-c801-4b51-85fb-e078616bc4fc" />
