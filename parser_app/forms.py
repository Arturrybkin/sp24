from django import forms


class JobSearchForm(forms.Form):
    keywords = forms.CharField(
        label='Ключевые слова',
        max_length=3000,
        required=False,
        widget=forms.TextInput(attrs={'value': ''})
    )
    exclude_words = forms.CharField(
        label='Исключить слова',
        max_length=3000,
        required=False,
        widget=forms.TextInput(attrs={'value': ''})
    )

    CITY_CHOICES = [
        ('Москва', 'Москва'),
        ('Санкт-Петербург', 'Санкт-Петербург'),
        ('Новосибирск', 'Новосибирск'),
        ('Екатеринбург', 'Екатеринбург'),
        ('Казань', 'Казань'),
        ('Красноярск', 'Красноярск'),
        ('Нижний Новгород', 'Нижний Новгород'),
        ('Челябинск', 'Челябинск'),
        ('Уфа', 'Уфа'),
        ('Самара', 'Самара'),
        ('Ростов-на-Дону', 'Ростов-на-Дону'),
        ('Краснодар', 'Краснодар'),
        ('Омск', 'Омск'),
        ('Воронеж', 'Воронеж'),
        ('Пермь', 'Пермь'),
        ('Волгоград', 'Волгоград')
    ]

    cities = forms.MultipleChoiceField(
        label='Город',
        choices=CITY_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    salary_min = forms.IntegerField(label='Минимальная зарплата', required=False)

    EDUCATION_CHOICES = [
        ('no_edu', 'Не требуется или не указано'),
        ('secondary_professional', 'Среднее профессиональное'),
        ('higher', 'Высшее')
    ]

    education = forms.MultipleChoiceField(
        label='Образование',
        choices=EDUCATION_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    EXPERIENCE_CHOICES = [
        ('no_value', 'Не имеет значения'),
        ('no_experience', 'Нет опыта'),
        ('1-3', 'От 1 года до 3 лет'),
        ('3-6', 'От 3 до 6 лет'),
        ('6+', 'Более 6 лет')
    ]

    experience = forms.ChoiceField(
        label='Опыт работы',
        choices=EXPERIENCE_CHOICES,
        widget=forms.RadioSelect,
        required=False
    )

    PERIOD_CHOICES = [
        ('all_time', 'За всё время'),
        ('month', 'За месяц'),
        ('week', 'За неделю'),
        ('three_days', 'За последние три дня'),
        ('day', 'За сутки')
    ]

    period = forms.ChoiceField(
        label='Выводить',
        choices=PERIOD_CHOICES,
        widget=forms.RadioSelect,
        required=False
    )