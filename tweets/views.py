from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from .models import Tweet

# Create your views here.


def home_view(request, *args, **kwargs):
    return HttpResponse("<h1> Django </h1>")


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
