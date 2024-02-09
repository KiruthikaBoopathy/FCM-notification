import mysql.connector
from datetime import datetime, timedelta
from pyfcm import FCMNotification
import json

api_key = ("AAAA5_BzCJY:APA91bGw3YFRu68oLaMsf4d8HFkQ"
           "-v2oQwGtESFGngSi7jRzpOPEFLv5szePG_OKdnS1K4KlwUFjfPjP64WJ075QjuRJ4T4lo2H6oyeav"
           "-RCFPp0zPtKvdeY2dAozQKXPfG6rOTDMeQs")


def SendReminderNotification(event=None, context=None):
    db_config = {
        'host': 'crm.cb3elanm71vl.ap-south-1.rds.amazonaws.com',
        'user': 'root',
        'password': 'ZzKvQ%7O22',
        'database': 'VivyaCrm',
        'port': '3306'
    }
    connection = mysql.connector.connect(**db_config)
    with connection.cursor(dictionary=True) as cursor:
        user_query = "SELECT * FROM users ;"
        cursor.execute(user_query)
        user_rows = cursor.fetchall()
        for user_row in user_rows:
            reg_id = user_row['fcm_token']
            user_ids = user_row['user_id']
            today_date = datetime.now().date()
            notification_query = (f"SELECT * FROM activities_reminders WHERE user_id = '{user_ids}' AND DATE("
                                  f"reminder_datetime) = '{today_date}'")
            cursor.execute(notification_query)
            reminder_rows = cursor.fetchall()
            if reminder_rows:
                notifi_time = reminder_rows[0]['reminder_datetime'] - timedelta(minutes=30)
                for note in reminder_rows:
                    compare_notifi_time = notifi_time.strftime("%H:%M")
                    if datetime.now().strftime("%H:%M") == compare_notifi_time and reminder_rows[0][
                        "status_remainder"] != 1:
                        select_query = "SELECT * FROM activities_reminders WHERE activitiesreminders_id = %s"
                        cursor.execute(select_query, (reminder_rows[0]['activitiesreminders_id'],))
                        selected_row = cursor.fetchone()

                        if selected_row:
                            update_query = ("UPDATE activities_reminders SET status_remainder = 1 WHERE "
                                            "activitiesreminders_id = %s")
                            cursor.execute(update_query, (reminder_rows[0]['activitiesreminders_id'],))
                            connection.commit()
                            print("Update successful")

                        resp = FCMNotification(api_key=api_key).notify_single_device(registration_id=reg_id,
                                                                                     message_title=reminder_rows[0][
                                                                                         'reminder_notes'])
                        noti_title = reminder_rows[0]['reminder_notes']
                        noti_message = 'this is message'
                        user_id_value = user_ids
                        sql_query = ("INSERT INTO user_notification (noti_title, noti_message, user_id, noti_type) "
                                     "VALUES (%s, %s, %s, %s);")
                        values = (noti_title, noti_message, user_id_value, 'remindernotes')
                        cursor.execute(sql_query, values)
                        connection.commit()


SendReminderNotification()
