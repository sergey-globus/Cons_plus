# Команда 2
## Проект на тему "Защита прав потребителей в интернет-пространстве (маркетплейсы, доставка, онлайн-курсы)"

main — стабильная версия проекта (релизы).

develop — основная ветка для интеграции новых функций и исправлений.

feature/имя_фичи — отдельные ветки для разработки задач.

Работа с веткой develop:
- создание новой ветки:
  
  git checkout develop
  
  git checkout -b feature/имя_фичи
  
- получение изменений:
  
  git checkout develop
  
  git pull origin develop
  
  git checkout feature/имя_фичи
  
  git merge develop
  
- обновление собственной ветки:
  
  git checkout feature/имя_фичи
  
  git add .
  
  git commit -m "comment"
  
  git push origin feature/имя_фичи
  
- слияние с веткой develop:
  
  git checkout develop
  
  git merge feature/имя_фичи

  
