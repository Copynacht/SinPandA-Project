from django.urls import path
from .views import timetable, assignment, announce, getTimetable, getAssignment, getAnnounce

urlpatterns = [
    path('timetable', timetable, name='timetable'),
    path('assignment', assignment, name='assignment'),
    path('announce', announce, name='announce'),
    path('timetableupdate', getTimetable, name='timetableupdate'),
    path('announceupdate', getAnnounce, name='announceupdate'),
    path('assignmentupdate', getAssignment, name='assignmentupdate'),
]
