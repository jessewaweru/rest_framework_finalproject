# In a new file like project/middleware.py
# import re
# import logging
# from django.db import connection


# class QueryInspectorMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         response = self.get_response(request)

#         # Log all queries involving the School table
#         queries = [
#             q["sql"]
#             for q in connection.queries
#             if re.search(r"SCHOOL", q["sql"], re.IGNORECASE)
#         ]
#         for query in queries:
#             logging.debug(f"School query: {query}")

#         return response
