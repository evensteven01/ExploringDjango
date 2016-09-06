from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse


def index(request):	
    #return HttpResponse('Hello, World! This is steve BEA!. Youre at index')
    questionList = Question.objects.order_by('-pub_date')[:5]
    #responseContent = ', '.join([q.question_text for q in questionList])
    #return HttpResponse(responseContent)
    template = loader.get_template('polls/index.html')
    context = {
        'questionList': questionList,
    }
    #return HttpResponse(template.render(context,request))
    #Shortcut
    return render(request, 'polls/index.html',context)

def detail(request, question_id):
    print('Getting question: ' + str(question_id))
    #return HttpResponse("You're looking at question %s" % question_id)
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist bea")
    context = {'question': question}
    return render(request, 'polls/detail.html',context)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    #return HttpResponse("You're voting on question %s." % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selectedChoice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        context = { 'question': question, 'error_message': 'You didnt select a choice', }
        return render(request, 'polls/detail.html', context)
    else:
        selectedChoice.votes += 1
        selectedChoice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

