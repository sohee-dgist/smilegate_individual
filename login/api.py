import jwt
import datetime
import my_settings

class myapis:
    class tokens:
        def make_token(userid):
            min_10 = datetime.timedelta(minutes=10)
            now = datetime.datetime.now()
            token = jwt.encode({"user_id": userid, "expired_date": datetime.datetime.strftime(now+min_10,"%Y/%m/%d %H:%M:%S")}, my_settings.SECRET_KEY_1, algorithm="HS256")
            return token
        def make_refresh_token(userid):
            min_10 = datetime.timedelta(minutes=10)
            day_1 = datetime.timedelta(days=1)
            now = datetime.datetime.now()
            token = jwt.encode({"user_id": userid, "expired_date": datetime.datetime.strftime(now + day_1, "%Y/%m/%d %H:%M:%S")}, my_settings.SECRET_KEY_2, algorithm="HS256")
            return token
        def check_token(token):
            decoded = jwt.decode(token, my_settings.SECRET_KEY_1, algorithms="HS256")
            userid = decoded['user_id']
            expired_date = decoded['expired_date']
            now = datetime.datetime.now()
            expired_date = datetime.datetime.strptime(expired_date,"%Y/%m/%d %H:%M:%S")
            if now < expired_date:
                return True, userid
            else:
                return False, userid
        def check_refresh_token(token):
            decoded = jwt.decode(token, my_settings.SECRET_KEY_2, algorithms="HS256")
            userid = decoded['user_id']
            expired_date = decoded['expired_date']
            now = datetime.datetime.now()
            expired_date = datetime.datetime.strptime(expired_date,"%Y/%m/%d %H:%M:%S")
            if now < expired_date:
                return True, userid
            else:
                return False, userid