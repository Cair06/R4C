from django.views.decorators.csrf import csrf_exempt
import datetime
from django.http import HttpResponse
from robots.utils import fetch_robots_created_last_week, group_robots_by_model_and_version, generate_excel_report


@csrf_exempt
def download_weekly_report(request):
    if request.method == 'GET':
        today_date = datetime.datetime.now().strftime('%Y-%m-%d')
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="weekly_report_{today_date}.xlsx"'
        recent_robots = fetch_robots_created_last_week()
        aggregated_data = group_robots_by_model_and_version(recent_robots)
        unique_models = set(row['model'] for row in aggregated_data)
        generate_excel_report(aggregated_data, unique_models, response)
        return response
    else:
        return HttpResponse("Method not allowed", status=405)
