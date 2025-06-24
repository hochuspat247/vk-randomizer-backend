# CORS Configuration for VK Randomizer Backend

## Overview

This document explains the CORS (Cross-Origin Resource Sharing) configuration for the VK Randomizer Backend API, which allows frontend applications from any domain to access the API.

## Problem Solved

The original error:
```
Access to fetch at 'https://randomizer.avenir-team.ru/api/v1/communities/cards' 
from origin 'https://user440084704-ekxc27na.tunnel.vk-apps.com' has been blocked by CORS policy
```

This occurred because the backend server wasn't configured to allow cross-origin requests.

## Configuration

### Current CORS Settings

The CORS configuration is defined in `src/core/config.py`:

```python
CORS_ORIGINS: List[str] = ["*"]  # Разрешаем доступ с любого домена
CORS_ALLOW_CREDENTIALS: bool = False  # Должно быть False при использовании "*"
CORS_ALLOW_METHODS: List[str] = ["*"]  # Все HTTP методы
CORS_ALLOW_HEADERS: List[str] = ["*"]  # Все заголовки
```

### Applied to FastAPI Applications

CORS middleware is applied to both main applications:

1. **`src/main.py`** - Full application with database
2. **`src/main_simple.py`** - Simplified application with in-memory data

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)
```

## Allowed Origins

### Open Access Configuration
- `"*"` - **Любой домен** - API доступен с любого веб-сайта

Это означает, что ваш API будет доступен с:
- VK Apps доменов
- Любых других веб-сайтов
- Локальных приложений разработки
- Мобильных приложений
- И любых других источников

## Testing CORS Configuration

Use the provided test script to verify CORS is working:

```bash
python test_cors.py
```

This script will:
1. Test preflight OPTIONS requests for various origins
2. Test actual GET requests with CORS headers
3. Display the response headers to verify configuration

## Customization

### Restricting Access (Optional)

If you want to restrict access to specific domains later, you can modify `src/core/config.py`:

```python
CORS_ORIGINS: List[str] = [
    "https://your-domain.com",
    "https://another-domain.com",
    "http://localhost:3000",
]
CORS_ALLOW_CREDENTIALS: bool = True  # Можно включить обратно
```

### Environment Variables

You can override CORS settings using environment variables:

```bash
export CORS_ORIGINS='["https://your-domain.com", "https://another-domain.com"]'
```

## Security Notes

⚠️ **Важно**: Текущая конфигурация разрешает доступ с любого домена, что удобно для разработки, но может быть небезопасно для продакшена.

### Для продакшена рекомендуется:

1. **Ограничить домены**: Указать только те домены, которые действительно нужны
2. **Использовать переменные окружения**: Не хардкодить домены в коде
3. **Мониторинг запросов**: Логировать CORS нарушения для выявления несанкционированного доступа

```python
# Пример более безопасной конфигурации
CORS_ORIGINS: List[str] = [
    "https://your-production-domain.com",
    "https://your-staging-domain.com",
]
CORS_ALLOW_CREDENTIALS: bool = True
CORS_ALLOW_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
CORS_ALLOW_HEADERS: List[str] = ["Content-Type", "Authorization"]
```

## Troubleshooting

### Common Issues

1. **Credentials with Wildcard**: Если используете `credentials: 'include'`, убедитесь что `CORS_ALLOW_CREDENTIALS: False` при `CORS_ORIGINS: ["*"]`
2. **Browser Caching**: Очистите кэш браузера после изменения CORS настроек
3. **Server Restart**: Перезапустите сервер после изменения конфигурации

### Debug Steps

1. Check browser console for CORS errors
2. Run `test_cors.py` to verify server configuration
3. Verify the server is running and accessible
4. Check that the server was restarted after configuration changes

## Example Frontend Usage

```javascript
// Fetch без credentials (рекомендуется с "*")
fetch('https://randomizer.avenir-team.ru/api/v1/communities/cards', {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
    },
    // credentials: 'include', // Не используйте с "*"
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
```

## Related Files

- `src/core/config.py` - CORS configuration
- `src/main.py` - Main FastAPI application with CORS
- `src/main_simple.py` - Simple FastAPI application with CORS
- `test_cors.py` - CORS testing script 