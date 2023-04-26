from resources.authorization import RegisterResource, LoginResource
from resources.insurences import (
    VehicleInsurenceResource,
    EstateInsurenceResource,
    InsurenceAcceptResource, InsurenceCancelResource, InsurenceDeleteResource

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
    (InsurenceDeleteResource, "/insurence/vehicle/<int:pk>/delete"),
    (PaymentCardResource, "/insurence/payments/card"),
    (SearchResource, "/insurence/search"),  # ?email=John&plate_number=Miami
    (InsurenceStatsResource, "/insurence/stats"),
)
