import os
import time
import boto3
import json
import requests
from datetime import datetime, timedelta, date

SLACK_WEBHOOK_URL = os.environ['SLACK_WEBHOOK_URL']


def lambda_handler(event, context) -> None:
    client = boto3.client('ce')

    total_billing = with_retry(lambda: get_total_billing(client), name="total_billing")
    if not total_billing:
        return

    service_billings = with_retry(lambda: get_service_billings(client), name="service_billings")
    if not service_billings:
        return

    if not total_billing or not service_billings:
        print(json.dumps({
            "level": "error",
            "function": "lambda_handler",
            "message": "Failed to retrieve billing data."
        }))
        return

    (title, detail) = get_message(total_billing, service_billings)
    post_slack(title, detail)

def with_retry(fn, retries=5, interval=2, name=""):
    for i in range(retries):
        if i > 0:
            time.sleep(interval)
        result = fn()
        if result:
            return result
        print(json.dumps({
            "level": "warning",
            "function": name,
            "retry": i + 1,
            "message": "Retry failed"
        }))
        # retries 回リトライしても失敗したらログ出力し、例外を投げる
    error_message = f"Failed to retrieve data after {retries} attempts"
    # retries回リトライしてもダメだった場合ログ出力
    print(json.dumps({
        "level": "error",
        "function": name,
        "message": error_message,
    }))
    raise Exception(error_message)


def get_total_billing(client) -> dict:
    (start_date, end_date) = get_total_cost_date_range()

    try:
        response = client.get_cost_and_usage(
            TimePeriod={'Start': start_date, 'End': end_date},
            Granularity='MONTHLY',
            Metrics=['AmortizedCost']
        )

    except Exception as e:
        print(json.dumps({
            "level": "error",
            "function": "get_total_billing",
            "message": f"Unexpected error: {e}"
        }))
        return {}

    return {
        'start': response['ResultsByTime'][0]['TimePeriod']['Start'],
        'end': response['ResultsByTime'][0]['TimePeriod']['End'],
        'billing': response['ResultsByTime'][0]['Total']['AmortizedCost']['Amount'],
    }


def get_service_billings(client) -> list:
    (start_date, end_date) = get_total_cost_date_range()

    try:

        response = client.get_cost_and_usage(
            TimePeriod={'Start': start_date, 'End': end_date},
            Granularity='MONTHLY',
            Metrics=['AmortizedCost'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
        )

    except Exception as e:
        print(json.dumps({
            "level": "error",
            "function": "get_service_billings",
            "message": f"Unexpected error: {e}"
        }))
        return []

    billings = []
    for item in response['ResultsByTime'][0]['Groups']:
        service_name = item.get('Keys', [None])[0]
        billing_amount = item['Metrics']['AmortizedCost'].get('Amount', "0")

        if not service_name or not billing_amount:
            continue

        billings.append({'service_name': service_name, 'billing': billing_amount})
    return billings


def get_message(total_billing: dict, service_billings: list) -> tuple[str, str]:
    start = datetime.strptime(total_billing['start'], '%Y-%m-%d').strftime('%m/%d')
    end_today = datetime.strptime(total_billing['end'], '%Y-%m-%d')
    end_yesterday = (end_today - timedelta(days=1)).strftime('%m/%d')
    total = round(float(total_billing['billing']), 2)

    title = f'{start}～{end_yesterday}の請求額は、{total:.2f} USDです。'
    details = [
        f'　・{item["service_name"]}: {round(float(item["billing"]), 2):.2f} USD'
        for item in service_billings if float(item['billing']) > 0
    ]

    return title, '\n'.join(details)


def post_slack(title: str, detail: str) -> None:
    payload = {'attachments': [{'color': '#36a64f', 'pretext': title, 'text': detail}]}
    try:
        response = requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload))
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # 失敗時
        print(json.dumps({
            "level": "error",
            "event": "slack_post",
            "message": "Slack notification failed",
            "error": str(e)
        }))
    else:
        # 成功時
        print(json.dumps({
            "level": "info",
            "event": "slack_post",
            "status": response.status_code,
            "message": "Slack notification sent successfully."
        }))


def get_total_cost_date_range() -> tuple[str, str]:
    start_date = get_begin_of_month()
    end_date = get_today()
    if start_date == end_date:
        end_of_month = datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=-1)
        begin_of_month = end_of_month.replace(day=1)
        return begin_of_month.date().isoformat(), end_date
    return start_date, end_date


def get_begin_of_month() -> str:
    return date.today().replace(day=1).isoformat()


def get_today() -> str:
    return date.today().isoformat()
