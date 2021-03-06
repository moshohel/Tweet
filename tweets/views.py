import random
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url
from django.conf import settings

from .forms import TweetForm
from .models import Tweet
# Create your views here.

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request, *args, **kwargs):
    # return HttpResponse("<h1> Django </h1>")
    return render(request, "pages/home.html", context={}, status=200)


def tweet_create_view(request, *args, **kwargs):
    print("ajax", request.is_ajax())
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    # print("next_url", next_url)
    if form.is_valid():
        obj = form.save(commit=False)
        # other form related logic
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)

        form = TweetForm()
    return render(request, "components/form.html", context={"form": form})


def tweet_list_view(request, *args, **kwargs):
    """
    REST API VIEW
    return json data
    """
    qs = Tweet.objects.all()
    # tweet_list = [{"id": x.id, "content": x.content,
    #                "likes": random.randint(0, 234)} for x in qs]
    tweet_list = [x.serialize() for x in qs]
    data = {
        "isUser": False,
        "response": tweet_list
    }
    return JsonResponse(data)


def tweet_detail_view(request, tweet_id, *args, **kwargs):
    """
    REST API VIEW
    return json data
    """
    data = {
        "id": tweet_id,
        # "content": obj.content,
        # "image_path": obj.image.url
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = "Not found"
        status = 404
        #raise Http404

    # return HttpResponse(f"<h1> Django tweet {tweet_id} - {obj.content}</h1>")
    # json.dumps content_type ='application/json'
    return JsonResponse(data, status=status)
