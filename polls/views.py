from django.http import HttpResponse, HttpResponseRedirect


from .models import Question,Choice

#get_object_or_404はget_object_or_404関数用。shortcut版renderはtemplateのロードが自動
from django.shortcuts import get_object_or_404, render
#from django.utils import timezone
from django.urls import reverse

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def hello(request):
    return HttpResponse("Hello, world. You're at the polls hello.")

# %sは文字列型, %aは？（''が付く)
#q = Question(question_text="%s" %question_id,pub_date=timezone.now())
    #q.save()
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id) #Questionオブジェクト(DBにある)から条件pk=question_idで取得。取得できない場合は404エラーをはく。
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
