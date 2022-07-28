FROM python:3.10-slim AS python
# В питон контейнере разворачиваем окружение и щапускаем тесты
WORKDIR  tests
COPY requirements.txt .
RUN pip3 install --compile -r requirements.txt && rm -rf /root/.cache
COPY src tests
RUN pytest --alluredir=/opt/mount/allure-report
# При запуске контейнера 
ENTRYPOINT ["pytest", "--alluredir=/opt/mount/allure-report"]


