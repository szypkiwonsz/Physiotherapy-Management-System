from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginate(request, data, paginate_by):
    url_parameter_page = request.GET.get('page')
    paginator = Paginator(data, paginate_by)
    try:
        users = paginator.page(url_parameter_page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return users
