from django.urls import path
from . import views

"""
### Experiences (TODOS)
api/v1/experiences/
- [ ] POST /experiences
- [ ] GET PUT DELETE /experiences/1
- [ ] GET /experiences/1/perks
- [ ] GET POST /experiences/perks
- [ ] GET PUT DELETE /experiences/perks/1
- [ ] GET POST /experiences/1/bookings
- [ ] GET PUT DELETE /experiences/1/bookings/2

"""
urlpatterns = [
    path("", views.Experiences.as_view()),
    path("<int:pk>", views.ExperienceDetail.as_view()),
    path("<int:pk>/perks", views.PerksOfExperience.as_view()),
    path("perks/", views.Perks.as_view()),
    path("perks/<int:pk>", views.PerkDetail.as_view()),
    path("<int:pk>/bookings", views.BookingsOfExperience.as_view()),
    # path("<int:pk>/bookings/<int:book_pk>", views.BookingOfExperience.as_view()),
]
