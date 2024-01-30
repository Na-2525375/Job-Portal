
from django.contrib import admin
from django.urls import path
from myProject.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',signupPage,name='signupPage'),
    path('logoutPage/',logoutPage,name='logoutPage'),
    path('signinPage/',signinPage,name='signinPage'),
    path('dashboardPage/',dashboardPage,name='dashboardPage'),
    path('viewjobPage/',viewjobPage,name='viewjobPage'),
    path('add_job_Page/',add_job_Page,name='add_job_Page'),
    path('deletePage/<str:myid>',deletePage,name='deletePage'),
    path('editPage/<str:myid>',editPage,name='editPage'),
    path('applicants_view_page/<str:myid>',applicants_view_page,name='applicants_view_page'),
    path('updatePage/',updatePage,name='updatePage'),
    path('applyPage/<str:myid>',applyPage,name='applyPage'),
    path('ProfilePage/',ProfilePage,name='ProfilePage'),
    path('EditProfilePage/',EditProfilePage,name='EditProfilePage'),
    path('changePasswordPage/',changePasswordPage,name='changePasswordPage'),
    path('createdJobByRecruiter/',createdJobByRecruiter,name='createdJobByRecruiter'),
    path('applied_job_by_jobseeker/',applied_job_by_jobseeker,name='applied_job_by_jobseeker'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
