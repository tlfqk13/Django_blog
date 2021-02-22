
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Post
from marketing.models import Signup
from django.db.models import Count, Q


def search(request):
    queryset = Post.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) | Q(overview__icontains=query)
        ).distinct()

    context = {
        'queryset': queryset
    }

    return render(request, 'search_results.html', context)


def get_category_count():
    queryset = Post\
        .objects\
        .values('categories__title')\
        .annotate(Count('categories__title'))

    return queryset

# categories__title : 밑줄 2개다


def index(request):
    featured = Post.objects.filter(featured=True)
    latest = Post.objects.order_by('-timestamp')[0:3]

    if request.method == "POST":
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    context = {
        'object_list': featured,  # 싹 가져와라
        'latest': latest  # 최근 3개
    }
    return render(request, 'index.html', context)


def blog(request):
    category_count = get_category_count()
    print(category_count)
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 4)  # page당 포스팅 몇 개 보여줄꺼냐
    page_requset_var = 'page'
    page = request.GET.get(page_requset_var)

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    context = {
        'queryset': paginated_queryset,
        'most_recent': most_recent,
        'page_requset_var': page_requset_var,
        'category_count': category_count,
    }
    return render(request, 'blog.html', context)


def post(request, id):
    post = get_object_or_404(Post, id=id)
    context = {
        'post': post
    }
    return render(request, 'post.html', context)
