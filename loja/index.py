from django.shortcuts import render

def index(request):
    print('blog')
    return render(
        request,
        'blog/index.html',
    )
