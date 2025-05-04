from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('welcome/', views.welcome, name='welcome'),
    path('tasks/', views.task_list, name='task_list'),
    path('add-task/', views.add_task, name='add_task'),
    path('complete-task/<int:task_id>/', views.complete_task, name='complete_task'),
    path('undo/<int:task_id>/', views.undo_task, name='undo_task'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
]
