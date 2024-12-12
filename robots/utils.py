import datetime
import pandas as pd
from django.db.models import Count
from django.utils import timezone
from .models import Robot


def fetch_robots_created_last_week():
    last_week = timezone.now() - datetime.timedelta(days=7)
    return Robot.objects.filter(created__gte=last_week)


def group_robots_by_model_and_version(robots_queryset):
    return (robots_queryset
            .values('model', 'version')
            .annotate(count=Count('id'))
            .order_by('model', 'version'))


def generate_excel_report(aggregated_data, unique_models, response):
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        if unique_models:
            for model_name in unique_models:
                model_data = [row for row in aggregated_data if row['model'] == model_name]
                df = pd.DataFrame(model_data)
                df.rename(columns={
                    'model': 'Модель',
                    'version': 'Версия',
                    'count': 'Количество за неделю'
                }, inplace=True)
                df.to_excel(writer, sheet_name=model_name, index=False)
        else:
            df = pd.DataFrame([{'Сообщение': 'Нет данных за последнюю неделю'}])
            df.to_excel(writer, sheet_name="Нет данных", index=False)