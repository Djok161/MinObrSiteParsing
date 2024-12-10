# Базовый образ для сборки
FROM node:18-alpine as build

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы package.json и package-lock.json
COPY rksi/package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем исходный код приложения
COPY rksi/ .

# Сборка приложения
RUN npm run build

# Используем минимальный образ для запуска
FROM node:18-alpine

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем собранные файлы из предыдущего этапа
COPY --from=build /app/dist ./dist

# Устанавливаем HTTP-сервер для раздачи статических файлов
RUN npm install -g serve

# Экспонируем порт
EXPOSE 3000

# Запускаем приложение
CMD ["serve", "-s", "dist"]
