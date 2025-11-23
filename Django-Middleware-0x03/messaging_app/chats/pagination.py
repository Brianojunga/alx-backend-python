from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MessagePagination(PageNumberPagination):
    page_size = 20                  # 20 messages per page
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        """
        Override to ensure the response contains 'count' from page.paginator.count,
        which the test is looking for.
        """
        return Response({
            "count": self.page.paginator.count,  # <- explicit 'count'
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data
        })
