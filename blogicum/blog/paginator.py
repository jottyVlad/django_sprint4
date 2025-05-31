from django.core.paginator import Paginator


def paginate(post_list, request, per_page=10):
    post_list = post_list.order_by('-pub_date')
    paginator = Paginator(post_list, per_page)
    page_number = request.GET.get("page")
    return paginator.get_page(page_number)
