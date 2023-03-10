from django.core.exceptions import FieldError
from django.db.models import Avg
from rest_framework import generics,pagination
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import Clinic, ClinicReview
from authentication.serializers import ClinicProfileSerializer, ReviewSerializer, ClinicProfileSimpleSerializer
from footerlabels.models import Footerlabels, MedicalUnityTypes, AcademicDegree, Speciality, MedicalSkills, \
    ClinicSpecialities, MedicalFacilities, Newsletter
from footerlabels.serializers import FooterlabelsSerializer, MedicalUnityTypesSerializer, AcademicDegreeSerializer, \
    SpecialitySerializer, MedicalSkillsSerializer, ClinicSpecialitiesSerializer, MedicalFacilitiesSerializer


class FooterLabelList(APIView):
    """
    List all footer labels, or create a new footer label.
    """
    def get(self, request):
        snippets = Footerlabels.objects.all()
        serializer = FooterlabelsSerializer(snippets, many=True)
        return Response(serializer.data)


class MedicalUnityTypesList(APIView):
    """
    List all Medical Unity Types labels, or create a new footer label.
    """
    def get(self, request):
        medical_unity_types = MedicalUnityTypes.objects.all()
        serializer = MedicalUnityTypesSerializer(medical_unity_types, many=True)
        return Response(serializer.data, status=200)


class AcademicDegreeList(APIView):
    """
    List all Academic Degree labels, or create a new footer label.
    """
    def get(self, request):
        academic_degree = AcademicDegree.objects.all()
        serializer = AcademicDegreeSerializer(academic_degree, many=True)
        return Response(serializer.data, status=200)


class SpecialityList(APIView):
    """
    List all Academic Degree labels, or create a new footer label.
    """
    def get(self, request):
        speciality = Speciality.objects.all()
        serializer = SpecialitySerializer(speciality, many=True)
        return Response(serializer.data, status=200)


class MedicalSkillsList(APIView):
    """
    List all Academic Degree labels, or create a new footer label.
    """
    def get(self, request):
        medical_skills = MedicalSkills.objects.all()
        serializer = MedicalSkillsSerializer(medical_skills, many=True)
        return Response(serializer.data, status=200)


class ClinicSpecialitiesList(APIView):
    """
    List all Academic Degree labels, or create a new footer label.
    """
    def get(self, request):
        clinic_specialities = ClinicSpecialities.objects.all()
        serializer = ClinicSpecialitiesSerializer(clinic_specialities, many=True)
        return Response(serializer.data, status=200)


class MedicalFacilitiesList(APIView):
    """
    List all Academic Degree labels, or create a new footer label.
    """
    def get(self, request):
        medical_facilities = MedicalFacilities.objects.all()
        serializer = MedicalFacilitiesSerializer(medical_facilities, many=True)
        return Response(serializer.data, status=200)


class NewsletterView(APIView):
    """
    List all Academic Degree labels, or create a new footer label.
    """
    def post(self, request):

        email = request.data.get('email', '')
        name = request.data.get('name', '')
        try:
            Newsletter.objects.create(email=email, name=name)
        except FieldError:
            return Response({"error": "Something went wrong"})
        return Response({"success": "Success"}, status=200)


class ClinicPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class ClinicList(generics.ListAPIView):
    serializer_class = ClinicProfileSerializer
    queryset = Clinic.objects.filter(user__is_visible=True)
    pagination_class = ClinicPagination

    def get_queryset(self):
        queryset = self.queryset

        # Filtering by clinic name
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(clinic_name__icontains=name)

        # Filtering by clinic town
        town = self.request.query_params.get('town', [])
        if town:
            town = town.split("|")
            queryset = queryset.filter(clinic_town__icontains=town)

        # Filtering by clinic specialities
        specialities = self.request.query_params.get('clinic_specialities', [])
        if specialities:
            specialities = specialities.split("|")
            queryset = queryset.filter(clinic_specialities__id__in=specialities)

        # Filtering by unity facilities
        facilities = self.request.query_params.get('unity_facilities', [])
        if facilities:
            facilities = facilities.split("|")
            queryset = queryset.filter(unity_facilities__id__in=facilities)

        return queryset


class TopClinicsAPIView(APIView):
    def get(self, request, format=None):
        # TODO: Get only the visible ones - clinics
        # Get the first 4 clinics ordered by their rating
        clinics = Clinic.objects.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')[:4]

        # Serialize the clinics data
        serializer = ClinicProfileSimpleSerializer(clinics, many=True)

        # Get the first 4 reviews for each clinic and add them to the serialized clinic data
        for i, clinic in enumerate(clinics):
            # TODO: Get only the visible ones - reviews
            reviews = ClinicReview.objects.filter(clinic=clinic)[:4]
            reviews_serializer = ReviewSerializer(reviews, many=True)
            serializer.data[i]['recent_reviews'] = reviews_serializer.data

        return Response(serializer.data)


class ClinicDetailAPIView(RetrieveAPIView):
    queryset = Clinic.objects.all()
    serializer_class = ClinicProfileSerializer
    lookup_field = 'id'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        # TODO: Get only the visible ones - reviews
        context['reviews'] = ClinicReview.objects.filter(clinic=self.kwargs['id'])
        return context


class ReviewCreate(APIView):
    def post(self, request):
        clinic_id = request.query_params.get('clinic_id', None)
        # Get the clinic instance
        try:
            clinic = Clinic.objects.get(id=clinic_id)
        except Clinic.DoesNotExist:
            return Response({'error': 'Clinic not found.'}, status=404)

        copy = request.data
        copy["clinic"] = clinic.id
        # Create a new Review object
        serializer = ReviewSerializer(data=copy)

        if serializer.is_valid():
            serializer.save(clinic=clinic)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
