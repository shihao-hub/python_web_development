from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class ArticleListAnonRateThrottle(AnonRateThrottle):
    THROTTLE_RATES = {"anon": "5/min"}


class ArticleListUserRateThrottle(UserRateThrottle):
    THROTTLE_RATES = {"user": "30/min"}
