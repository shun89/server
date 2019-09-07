from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


class AnonBurstRateThrottle(AnonRateThrottle):
    scope = 'anon-burst'


class UserBurstRateThrottle(UserRateThrottle):
    scope = 'user-burst'
