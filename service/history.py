# from datetime import datetime, timedelta


# def get_calories_per_day_pipeline(days: int):
#     start_date = (datetime.today() - timedelta(days=days))
#     end_date = datetime.today()
#     bucket_boundaries = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d')
#                          for i in range(days + 1)]
#     print(bucket_boundaries)
#     date_range_filter = {
#         '$match': {
#             'date': {
#                 '$gte': start_date.strftime('%Y-%m-%d'),
#                 '$lte': end_date.strftime('%Y-%m-%d')
#             },
#         }
#     }
#     print(date_range_filter)
#     total_calories_each_day = {
#         '$bucket': {
#             'groupBy': '$date',
#             'boundaries': bucket_boundaries,
#             'default': 'Other',
#             'output': {
#                 'date': {
#                     '$max': '$date'
#                 },
#                 'total_calories': {
#                     '$sum': '$calories'
#                 }
#             }
#         }
#     }
#     print(total_calories_each_day)
#     return [date_range_filter, total_calories_each_day]


# def get_calories_burnt_till_now_pipeline(email: str, start_date: str):
#     end_date = datetime.today().strftime('%Y-%m-%d')
#     return [{
#         '$match': {
#             'date': {
#                 '$gte': start_date,
#                 '$lte': end_date
#             },
#             'email': email
#         }
#     }, {
#         '$group': {
#             '_id': 'sum of calories',
#             'SUM': {
#                 '$sum': '$calories'
#             }
#         }
#     }]


