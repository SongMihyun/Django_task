from django.urls import path
from todo import views
from todo import cb_views
app_name = 'todo'
urlpatterns = [
    #
    # path('todo/', views.todo_list, name='list'),
    # path('todo/<int:pk>/', views.todo_info, name='info'),
    # path('todo/delete/<int:pk>/', views.todo_delete, name='delete'),

    path('',cb_views.TodoListView.as_view(),name='list'),
    path('<int:pk>/',cb_views.TodoDetailView.as_view(),name='info'),
    path('<int:pk>/delete/',cb_views.TodoDeleteView.as_view(),name='delete'),
    path('<int:pk>/update/',cb_views.TodoUpdateView.as_view(),name='update'),
    path('create/',cb_views.TodoCreateView.as_view(),name='create'),

]
