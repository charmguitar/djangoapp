from django.urls import path

from . import views

#.../polls/以降のurlを定義
#name="xxx"を付加しておけば、そのurlをハードコーディングを解消できる。href="/polls/{{ question.id }}/"を、href="{% url 'detail' question.id %}"
app_name = 'polls' #名前空間を指定した場合は、上記のコードを'detail'から'polls:detail'と変更する。
urlpatterns = [
    path('', views.index, name='name'), #polls/viewsのhello関数を実行
    path('<question_id>/', views.detail, name='detail'), #question_idはview.detail関数を呼び出す時の引数として渡される.
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
