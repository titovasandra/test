#!/bin/bash
echo "Run allure server"
docker-compose -f ${PWD}/allure/docker-compose.yml up -d allure allure-ui

echo "Prepare test container"
docker build -q -t akiselev:latest ${PWD}/tests/

echo "Run test container"
docker run --rm -v ${PWD}/allure-report:/opt/mount/allure-report --name test_run akiselev
sleep 10s
echo "Check latest report http://localhost:5050/allure-docker-service/latest-report"

