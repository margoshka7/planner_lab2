from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from datetime import datetime, timedelta

# Данные для планингов (из словарей/списков)
PLANNERS_DATA = [
    {
        'id': 1,
        'title': 'Лунный планинг',
        'description': 'Планинг с фазами луны',
        'price': 950,
        'theme': 'lunar',
        'image': 'moon_planner.jpg'
    },
    {
        'id': 2, 
        'title': 'Минималистичный планинг',
        'description': 'Простой и элегантный дизайн',
        'price': 750,
        'theme': 'minimal',
        'image': 'minimal_planner.jpg'
    },
    {
        'id': 3,
        'title': 'Цветочный планинг',
        'description': 'С цветочными орнаментами',
        'price': 850,
        'theme': 'floral',
        'image': 'floral_planner.jpg'
    }
]

THEMES = {
    'light': 'Светлая тема',
    'dark': 'Темная тема', 
    'lunar': 'Лунная тема',
    'floral': 'Цветочная тема'
}

LANGUAGES = {
    'ru': 'Русский',
    'en': 'English'
}

def home(request):
    # Получаем настройки из cookies
    theme = request.COOKIES.get('theme', 'light')
    language = request.COOKIES.get('language', 'ru')
    last_visited = request.COOKIES.get('last_visited', 'Не посещали')
    
    # Сохраняем текущее посещение
    response = render(request, 'home.html', {
        'planners': PLANNERS_DATA,
        'current_theme': theme,
        'current_language': language,
        'last_visited': last_visited,
        'themes': THEMES,
        'languages': LANGUAGES,
    })
    
    # Сохраняем время посещения
    response.set_cookie('last_visited', datetime.now().strftime('%d.%m.%Y %H:%M'), 
                       max_age=30*24*60*60)  # 30 дней
    
    return response

def save_settings(request):
    if request.method == 'POST':
        theme = request.POST.get('theme', 'light')
        language = request.POST.get('language', 'ru')
        
        response = redirect('home')
        response.set_cookie('theme', theme, max_age=365*24*60*60)  # 1 год
        response.set_cookie('language', language, max_age=365*24*60*60)
        
        return response
    
    return redirect('home')

def planner_detail(request, planner_id):
    # Находим планинг по ID
    planner = next((p for p in PLANNERS_DATA if p['id'] == planner_id), None)
    
    if not planner:
        return redirect('home')
    
    # Получаем историю просмотров
    viewed_history = request.COOKIES.get('viewed_history', '[]')
    viewed_history = json.loads(viewed_history)
    
    # Добавляем текущий планинг в историю
    if planner_id not in viewed_history:
        viewed_history.append(planner_id)
        if len(viewed_history) > 5:  # Храним только 5 последних
            viewed_history.pop(0)
    
    response = render(request, 'planner_detail.html', {
        'planner': planner,
        'current_theme': request.COOKIES.get('theme', 'light')
    })
    
    # Сохраняем историю в cookies
    response.set_cookie('viewed_history', json.dumps(viewed_history), 
                       max_age=30*24*60*60)
    
    return response
