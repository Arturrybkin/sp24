import requests
from django.shortcuts import render
from django.db.models import Avg
from .forms import JobSearchForm
from .models import Job


def generate_hh_url(data, page=0):
    base_url = "https://api.hh.ru/vacancies?clusters=true&only_with_salary=true"
    params = []

    if data.get('keywords'):
        params.append(f"text={data['keywords']}")

    if data.get('exclude_words'):
        params.append(f"excluded_text={data['exclude_words']}")

    city_codes = {
        'Москва': 1,
        'Санкт-Петербург': 2,
        'Новосибирск': 4,
        'Екатеринбург': 3,
        'Казань': 88,
        'Красноярск': 54,
        'Нижний Новгород': 66,
        'Челябинск': 104,
        'Уфа': 99,
        'Самара': 78,
        'Ростов-на-Дону': 76,
        'Краснодар': 53,
        'Омск': 68,
        'Воронеж': 26,
        'Пермь': 72,
        'Волгоград': 24
    }

    if data.get('cities'):
        for city in data['cities']:
            params.append(f"area={city_codes[city]}")

    if data.get('salary_min'):
        params.append(f"salary={data['salary_min']}&currency_code=RUR")

    education_map = {
        'no_edu': 'not_required_or_not_specified',
        'secondary_professional': 'special_secondary',
        'higher': 'higher'
    }

    if data.get('education'):
        for edu in data['education']:
            params.append(f"education={education_map[edu]}")

    experience_map = {
        'no_value': 'doesNotMatter',
        'no_experience': 'noExperience',
        '1-3': 'between1And3',
        '3-6': 'between3And6',
        '6+': 'moreThan6'
    }

    if data.get('experience'):
        params.append(f"experience={experience_map[data['experience']]}")

    period_map = {
        'all_time': 0,
        'month': 30,
        'week': 7,
        'three_days': 3,
        'day': 1
    }

    if data.get('period'):
        params.append(f"search_period={period_map[data['period']]}")

    params.append(f"page={page}")

    return f"{base_url}&{'&'.join(params)}"


def parse_salary(salary_data):
    if salary_data and salary_data.get('currency') == 'RUR':
        salary_from = salary_data.get('from')
        salary_to = salary_data.get('to')
        gross = salary_data.get('gross')

        if salary_from and salary_to:
            salary = (salary_from + salary_to) / 2
        elif salary_from:
            salary = salary_from
        elif salary_to:
            salary = salary_to
        else:
            salary = None

        if gross and salary:
            salary *= 0.87

        return salary

    return None


def fetch_jobs(hh_url):
    response = requests.get(hh_url)
    print(f"Fetching URL: {hh_url}")
    if response.status_code == 200:
        data = response.json()
        items = data.get('items', [])
        pages = data.get('pages', 0)
        print(f"Fetched {len(items)} jobs, total pages: {pages}")
        return items, pages
    else:
        print(f"Error fetching data: {response.status_code}")
    return [], 0


def save_jobs(jobs):
    for job in jobs:
        title = job.get('name')
        company_name = job.get('employer', {}).get('name')
        salary_data = job.get('salary')
        salary = parse_salary(salary_data)

        if salary is not None:
            print(f"Saving job: {title} at {company_name} with salary {salary}")
            Job.objects.create(title=title, company_name=company_name, salary=salary)
        else:
            print(f"Skipping job: {title} at {company_name} due to non-RUR currency")


def search_jobs(request):
    hh_url = ""
    if request.method == 'POST':
        form = JobSearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            initial_url = generate_hh_url(data, page=0)
            jobs, total_pages = fetch_jobs(initial_url)
            save_jobs(jobs)

            for page in range(1, total_pages):
                hh_url = generate_hh_url(data, page)
                jobs, _ = fetch_jobs(hh_url)
                save_jobs(jobs)
    else:
        form = JobSearchForm()

    return render(request, 'parser_app/search.html', {'form': form, 'hh_url': hh_url})


def job_analytics(request):
    jobs = Job.objects.all()
    total_jobs = jobs.count()
    avg_salary = jobs.aggregate(avg_salary=Avg('salary'))['avg_salary']
    min_salary_job = jobs.order_by('salary').first()
    max_salary_job = jobs.order_by('-salary').first()

    median_salary = None
    if total_jobs > 0:
        sorted_jobs = jobs.order_by('salary')
        middle_index = total_jobs // 2
        if total_jobs % 2 == 0:
            median_salary = (sorted_jobs[middle_index - 1].salary + sorted_jobs[middle_index].salary) / 2
        else:
            median_salary = sorted_jobs[middle_index].salary

    context = {
        'total_jobs': total_jobs,
        'avg_salary': avg_salary,
        'min_salary_job': min_salary_job,
        'max_salary_job': max_salary_job,
        'median_salary': median_salary,
    }

    return render(request, 'parser_app/job_analytics.html', context)
