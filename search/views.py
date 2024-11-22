# from rest_framework.views import APIView
# from rest_framework.response import Response
# from schools.models import School
# from schools.serializers import SchoolSerializer
# from django.db.models import Q


# class SchoolSearchAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         location = request.query_params.get("location")
#         city = request.query_params.get("city")
#         county = request.query_params.get("county")
#         name = request.query_params.get("name")
#         rating = request.query_params.get("rating")
#         facility = request.query_params.getlist("facility")
#         school_status = request.query_params.get("school_status")
#         school_type = request.query_params.get("school_type")
#         boarding_status = request.query_params.get("boarding_status")

#         query = Q()
#         if location:
#             query &= Q(location__icontains=location)
#         if name:
#             query &= Q(name__icontains=name)
#         if city:
#             query &= Q(city__icontains=city)
#         if county:
#             query &= Q(county__icontains=county)
#         if rating:
#             query &= Q(reviews__rating=rating)
#         if facility:
#             for f in facility:
#                 query |= Q(facility__icontains=f)
#         if school_status:
#             query &= Q(school_status=school_status)
#         if school_type:
#             query &= Q(school_type=school_type)
#         if boarding_status:
#             query &= Q(boarding_status=boarding_status)

#         queryset = School.objects.filter(query).distinct()
#         serializer = SchoolSerializer(queryset, many=True)
#         return Response(serializer.data)


# school_search_view = SchoolSearchAPIView.as_view()
