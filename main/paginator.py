from rest_framework.pagination import PageNumberPagination


class MainPaginator(PageNumberPagination):
    """
    Пагинатор по умолчанию
    """
    page_size = 5
    page_size_query_param = 5
    max_page_size = 5
