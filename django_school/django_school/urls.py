from django.urls import include, path
from django.contrib import admin
from classroom.views import classroom, students, teachers

urlpatterns = [
    path('', include('classroom.urls')),
    # path('google/connect/callback/', classroom.google_login_connect , name="google_login_connect"),
    path('google/login/callback/', classroom.google_login_request , name="google_login_request"),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', classroom.SignUpView.as_view(), name='signup'),
    path('accounts/signup/student/', students.StudentSignUpView.as_view(), name='student_signup'),
    path('accounts/signup/teacher/', teachers.TeacherSignUpView.as_view(), name='teacher_signup'),
]
