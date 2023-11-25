from datetime import datetime, timedelta


def get_calories_per_day_pipeline(days: int):
    start_date = (datetime.today() - timedelta(days=days))
    end_date = datetime.today()
    bucket_boundaries = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d')
                         for i in range(days + 1)]
    date_range_filter = {
        '$match': {
            'date': {
                '$gte': start_date.strftime('%Y-%m-%d'),
                '$lte': end_date.strftime('%Y-%m-%d')
            },
        }
    }
    print(date_range_filter)
    total_calories_each_day = {
        '$bucket': {
            'groupBy': '$date',
            'boundaries': bucket_boundaries,
            'default': 'Other',
            'output': {
                'date': {
                    '$max': '$date'
                },
                'total_calories': {
                    '$sum': '$calories'
                }
            }
        }
    }
    print(total_calories_each_day)
    return [date_range_filter, total_calories_each_day]


def get_calories_burnt_till_now_pipeline(email: str, start_date: str):
    end_date = datetime.today().strftime('%Y-%m-%d')
    return [{
        '$match': {
            'date': {
                '$gte': start_date,
                '$lte': end_date
            },
            'email': email
        }
    }, {
        '$group': {
            '_id': 'sum of calories',
            'SUM': {
                '$sum': '$calories'
            }
        }
    }]


def total_calories_to_burn(target_weight: int, current_weight: int):
    return int((target_weight - current_weight) * 7700)


def calories_to_burn(target_calories: int, current_calories: int,
                     target_date: datetime, start_date: datetime):
    actual_current_calories = current_calories - (
        (datetime.today() - start_date).days * 2000)

    new_target = target_calories - actual_current_calories

    days_remaining = (target_date - datetime.today()).days
    return int(new_target / days_remaining)
