from resources.authorization import RegisterResource, LoginResource
from resources.insurences import (
    VehicleInsurenceResource,
    EstateInsurenceResource,
    InsurenceAcceptResource,
    InsurenceCancelResource,
    InsurenceResource,
)
from resources.payment import PaymentCardResource
from resources.search import SearchResource
from resources.stats import InsurenceStatsResource

routes = (
    (RegisterResource, "/insurence/register"),
    (LoginResource, "/insurence/login"),
    (VehicleInsurenceResource, "/insurence/vehicle"),
    (EstateInsurenceResource, "/insurence/estate"),
    (InsurenceAcceptResource, "/insurence/vehicle/<int:pk>/accept"),
    (InsurenceCancelResource, "/insurence/vehicle/<int:pk>/cancel"),
    (InsurenceResource, "/insurence/vehicle/<int:pk>"),
    (PaymentCardResource, "/insurence/payments/card"),
    (SearchResource, "/insurence/search"),
    (InsurenceStatsResource, "/insurence/stats"),
)
