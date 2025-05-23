# Сравниваем вакансии программистов
Этот проект анализирует вакансии программистов в Москве, полученные с платформ HeadHunter и SuperJob. Скрипт собирает информацию о количестве найденных и обработанных вакансий, а также рассчитывает среднюю зарплату для разных языков программирования. Результаты выводятся в виде таблиц, понятных и удобных для сравнения.

Программа может быть полезна тем, кто интересуется рынком труда в IT-сфере, планирует менять язык программирования или просто хочет понять, где платят больше.

## Как установить
1. Убедитесь, что у вас установлен Python 3.10 или выше.
2. Установите зависимости:
```bash
pip install -r requirements.txt
```
3. Получите токен доступа SuperJob API:
* Зарегистрируйтесь на [superjob.ru](https://api.superjob.ru/)
* Получите `access_token` для использования API
* Переменная окружения должна быть сохранена в файле `.env` в корневой директории проекта. Создайте файл `.env` и добавьте в него следующую строку:
```text
SUPERJOB_TOKEN=ваш_ключ_для_SUPERJOB_API
```
4. Запустите скрипт:
```bash
python job_salary_stats.py
```
На экране появятся таблицы с анализом вакансий и зарплат по языкам программирования.

## Цель проекта 
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
Проект помогает освоить работу с API, обработку JSON-данных, форматирование таблиц и структуру реальных Python-программ.
