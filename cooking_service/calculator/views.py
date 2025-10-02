from django.shortcuts import render
from django.http import HttpResponse

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
}


def home_view(request):
    """
    Главная страница со списком доступных рецептов
    """
    recipes_list = "\n".join([f"<li><a href='/{dish}/'>{dish}</a></li>" for dish in DATA.keys()])

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Кулинарный помощник</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f9f9f9;
            }}
            .container {{
                background: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }}
            h1 {{
                color: #333;
                text-align: center;
            }}
            ul {{
                list-style: none;
                padding: 0;
            }}
            li {{
                margin: 15px 0;
                padding: 10px;
                background: #f0f0f0;
                border-radius: 4px;
            }}
            a {{
                text-decoration: none;
                color: #007bff;
                font-weight: bold;
                font-size: 18px;
            }}
            a:hover {{
                color: #0056b3;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🍳 Кулинарный помощник</h1>
            <p>Выберите рецепт:</p>
            <ul>
                {recipes_list}
            </ul>
            <p><small>Используйте параметр ?servings= для указания количества порций</small></p>
        </div>
    </body>
    </html>
    """

    return HttpResponse(html_content)


def recipe_view(request, dish):
    """
    Представление для отображения рецепта блюда
    """
    recipe = DATA.get(dish)

    if not recipe:
        return HttpResponse(f"<h1>Рецепт '{dish}' не найден</h1><p><a href='/'>Вернуться на главную</a></p>",
                            status=404)

    adjusted_recipe = recipe.copy()

    servings = request.GET.get('servings')

    if servings:
        try:
            servings = int(servings)
            if servings > 0:
                for ingredient in adjusted_recipe:
                    adjusted_recipe[ingredient] *= servings
        except (ValueError, TypeError):
            pass

    context = {
        'recipe': adjusted_recipe
    }

    return render(request, 'calculator/index.html', context)