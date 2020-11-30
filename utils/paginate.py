from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginate(request, data, paginate_by):
    """
    Method for paginating pages in relation to database objects.
    :param request: <django.core.handlers.wsgi.WSGIRequest>
    :param data: <django.db.models.query.QuerySet>
    :param paginate_by: <int> -> the number of elements on the page on which the page is to be paginated
    :return: <django.core.paginator.Page> -> number of paginated pages
    """
    url_parameter_page = request.GET.get('page')
    paginator = Paginator(data, paginate_by)
    try:
        users = paginator.page(url_parameter_page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return users
