import requests
from django.core.exceptions import FieldError
from django.db.models import Avg, Q, Count
from django.http import JsonResponse
from rest_framework import generics,pagination
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import Clinic, ClinicReview, CollaboratorDoctor, DoctorReview
from authentication.serializers import ClinicProfileSerializer, ReviewSerializer, ClinicProfileSimpleSerializer, \
    DoctorComplexProfileSerializer, ReviewDoctorSerializer, ClinicProfileNamesSerializer
from authentication.utils import Util
from footerlabels.models import Footerlabels, MedicalUnityTypes, AcademicDegree, Speciality, MedicalSkills, \
    ClinicSpecialities, MedicalFacilities, Newsletter, BannerCards, AddSense, BlogPost, Tag
from footerlabels.serializers import FooterlabelsSerializer, MedicalUnityTypesSerializer, AcademicDegreeSerializer, \
    SpecialitySerializer, MedicalSkillsSerializer, ClinicSpecialitiesSerializer, MedicalFacilitiesSerializer, \
    BannerCardsSerializer, AddsCardsSerializer, BlogPostSerializer, TagSerializer
from vudback.settings import RECAPCHA_KEY


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


class BannerCardList(APIView):
    """
    List all Academic Degree labels, or create a new footer label.
    """
    def get(self, request):
        banners = BannerCards.objects.all()
        serializer = BannerCardsSerializer(banners, many=True)
        return Response(serializer.data, status=200)


class AddsCardList(APIView):
    def get(self, request):
        adds = AddSense.objects.all()
        serializer = AddsCardsSerializer(adds, many=True)
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

def replace_romanian_characters(text):
    replacements = {
        'ă': 'a', 'â': 'a', 'î': 'i', 'ș': 's', 'ş': 's', 'ț': 't', 'ţ': 't',
        'Ă': 'a', 'Â': 'a', 'Î': 'i', 'Ș': 's', 'Ş': 's', 'Ț': 't', 'Ţ': 't'
    }
    for romanian_char, replacement in replacements.items():
        text = text.replace(romanian_char, replacement)
    return text

class ClinicList(generics.ListAPIView):
    serializer_class = ClinicProfileSerializer
    queryset = Clinic.objects.annotate(
        average_rating=Avg('reviews__rating', filter=Q(reviews__is_visible=True)),
        review_count=Count('reviews', filter=Q(reviews__is_visible=True)),
    ).filter(is_visible=True)
    pagination_class = ClinicPagination

    def get_queryset(self):
        queryset = self.queryset

        # Filtering by clinic name
        name = self.request.query_params.get('name')
        if name:
            clinic_specialities = ClinicSpecialities.objects.filter(label__iexact=name)
            if clinic_specialities.exists():
                specialities_ids = clinic_specialities.values_list('id', flat=True)
                queryset = queryset.filter(clinic_specialities__id__in=specialities_ids)
            else:
                queryset = queryset.filter(clinic_name__icontains=name)

        # Filtering by town
        town = self.request.query_params.get('town')
        if town:
            town_list = replace_romanian_characters(town).split("|")
            queryset = queryset.filter(clinic_town__in=town_list)

        # Filtering by specialities
        specialities = self.request.query_params.get('clinic_specialities', None)
        if specialities:
            specialities_list = specialities.split("|")
            queryset = queryset.filter(clinic_specialities__id__in=specialities_list)

        # Filtering by unit facilities
        facilities = self.request.query_params.get('unit_facilities', None)
        if facilities:
            facilities_list = facilities.split("|")
            queryset = queryset.filter(unity_facilities__id__in=facilities_list)

        # Filtering by unit types
        unity = self.request.query_params.get('unity_types', None)
        if unity:
            unity_list = unity.split("|")
            queryset = queryset.filter(medical_unit_types__id__in=unity_list)

        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)

        name = request.query_params.get('name', None)

        clinic_specialities = ClinicSpecialities.objects.filter(label__iexact=name)
        if len(clinic_specialities) > 0:
            specialities = []
            for e in clinic_specialities:
                specialities.append(str(e.id))
            response.data['specialities'] = "|".join(specialities)

        return response


class TopClinicsAPIView(APIView):
    def get(self, request, format=None):
        # Get the first 4 clinics ordered by their rating
        clinics = Clinic.objects.annotate(
            average_rating=Avg('reviews__rating', filter=Q(reviews__is_visible=True)),
            review_count=Count('reviews', filter=Q(reviews__is_visible=True)),
        ).filter(is_visible=True).order_by('-average_rating')[:4]

        # Serialize the clinics data
        serializer = ClinicProfileSimpleSerializer(clinics, many=True)

        # Get the first 4 reviews for each clinic and add them to the serialized clinic data
        for i, clinic in enumerate(clinics):
            reviews = ClinicReview.objects.filter(is_visible=True, clinic=clinic)[:4]
            reviews_serializer = ReviewSerializer(reviews, many=True)
            serializer.data[i]['recent_reviews'] = reviews_serializer.data

        return Response(serializer.data)

class TopDoctorsAPIView(APIView):
    def get(self, request, format=None):
        # Get the first 4 clinics ordered by their rating
        doctors = CollaboratorDoctor.objects.annotate(
            average_rating=Avg('reviewsdoctors__rating', filter=Q(reviewsdoctors__is_visible=True)),
            review_count=Count('reviewsdoctors', filter=Q(reviewsdoctors__is_visible=True)),
        ).filter(is_visible=True).order_by('-average_rating')[:4]
        # doctors = CollaboratorDoctor.objects.filter(is_visible=True)

        # Serialize the clinics data
        serializer = DoctorComplexProfileSerializer(doctors, many=True)

        # Get the first 4 reviews for each clinic and add them to the serialized clinic data
        for i, clinic in enumerate(doctors):
            reviews = DoctorReview.objects.filter(is_visible=True, doctor=clinic)[:4]
            if len(reviews) > 0:
                reviews_serializer = ReviewDoctorSerializer(reviews, many=True)
                serializer.data[i]['recent_reviews'] = reviews_serializer.data
            else:
                serializer.data[i]['recent_reviews'] = []

        return Response(serializer.data)


class ClinicDetailAPIView(RetrieveAPIView):
    queryset = Clinic.objects.annotate(
            average_rating=Avg('reviews__rating', filter=Q(reviews__is_visible=True)),
            review_count=Count('reviews', filter=Q(reviews__is_visible=True)),
        ).filter(is_visible=True)
    serializer_class = ClinicProfileSerializer
    lookup_field = 'id'


class DoctorPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class DoctorList(generics.ListAPIView):
    serializer_class = DoctorComplexProfileSerializer
    queryset = CollaboratorDoctor.objects.annotate(
            average_rating=Avg('reviewsdoctors__rating', filter=Q(reviewsdoctors__is_visible=True)),
            review_count=Count('reviewsdoctors', filter=Q(reviewsdoctors__is_visible=True)),
        ).filter(is_visible=True)
    pagination_class = ClinicPagination

    def get_queryset(self):
        queryset = self.queryset

        name = self.request.query_params.get('name', None)
        if name is not None:
            doctor_spec = Speciality.objects.filter(label__iexact=name)
            if len(doctor_spec) > 0:
                specialities = []
                for e in doctor_spec:
                    specialities.append(e.id)
                queryset = queryset.filter(speciality__id__in=specialities)
                return queryset

            queryset = queryset.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))

        dc = self.request.query_params.get('doctor_specialities', [])
        if dc:
            town = dc.split("|")
            queryset = queryset.filter(speciality__id__in=town)

        medical_skill = self.request.query_params.get('doctor_competences', [])
        if medical_skill:
            ms = medical_skill.split("|")
            queryset = queryset.filter(medical_skill__id__in=ms)

        collab_clinics = self.request.query_params.get('doctor_clinics', [])
        if collab_clinics:
            cc = collab_clinics.split("|")
            queryset = queryset.filter(collaborator_clinic__id__in=cc)

        return queryset

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return response


class DoctorDetailAPIView(RetrieveAPIView):
    queryset = CollaboratorDoctor.objects.annotate(
            average_rating=Avg('reviewsdoctors__rating', filter=Q(reviewsdoctors__is_visible=True)),
            review_count=Count('reviewsdoctors', filter=Q(reviewsdoctors__is_visible=True)),
        ).filter(is_visible=True)
    serializer_class = DoctorComplexProfileSerializer
    lookup_field = 'id'


class ReviewDoctorCreate(APIView):
    def post(self, request):
        r = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': RECAPCHA_KEY,
                'response': request.data['g-recaptcha-response'],
                # 'remoteip': get_client_ip(self.request),  # Optional
            }
        )

        if r.json()['success']:
            doctor_id = request.query_params.get('doctor_id', None)
            # Get the clinic instance
            try:
                doctor = CollaboratorDoctor.objects.get(id=doctor_id)
            except CollaboratorDoctor.DoesNotExist:
                return Response({'error': 'Doctor not found.'}, status=404)

            copy = request.data
            copy["doctor"] = doctor.id
            # Create a new Review object
            serializer = ReviewDoctorSerializer(data=copy)

            if serializer.is_valid():
                serializer.save(doctor=doctor)
                return Response(serializer.data, status=201)
            else:
                return Response(serializer.errors, status=400)
        return Response({"error": "Captcha nu e valid."}, status=400)


class ReviewCreate(APIView):
    def post(self, request):
        r = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': RECAPCHA_KEY,
                'response': request.data['g-recaptcha-response'],
                # 'remoteip': get_client_ip(self.request),  # Optional
            }
        )

        if r.json()['success']:
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
        else:
            return Response({"error": "Capcha nu e valid."}, status=400)


class BlogPostListAPIView(generics.ListAPIView):
    serializer_class = BlogPostSerializer

    def get_queryset(self):
        queryset = BlogPost.objects.all()
        tags = self.request.query_params.getlist('tags')
        if tags:
            queryset = queryset.filter(tags__name__in=tags)
        return queryset


class BlogPostDetailAPIView(generics.RetrieveAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer


class TagListAPIView(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class SendMessageClinic(generics.GenericAPIView):
    def post(self, request):
        r = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': RECAPCHA_KEY,
                'response': request.data['g-recaptcha-response'],
                # 'remoteip': get_client_ip(self.request),  # Optional
            }
        )

        if r.json()['success']:
            # Successfuly validated
            # Handle the submission, with confidence!
            data = request.data
            email = data.get('email', '')
            name = data.get('name', '')
            message = data.get('message', '')
            checkmark_if_send_copy = data.get('checkmarkIfSendCopy', False)
            clinic_id = data.get('clinicId', None)

            try:
                clinic = Clinic.objects.filter(id=clinic_id)[0]
                if not clinic:
                    return JsonResponse({'error': 'Error: Clinic doesn\'t exists'})
            except Exception as e:
                print(e)
                return JsonResponse({'error': 'Error: Clinic doesn\'t exists'})

            try:
                data = {
                    'client_email': email,
                    'client_name': name,
                    'client_message': message,
                    'clinic_email': clinic.primary_email,
                    'clinic_name': clinic.clinic_name,
                    'send_copy_email': checkmark_if_send_copy
                }
                Util.send_email(data=data, email_type='send-clinic-email')
            except Exception as e:
                return JsonResponse({'error': 'Sending email'})
            return JsonResponse({'message': 'Success'})

        return JsonResponse({'error': 'ReCAPTCHA not verified.'})


class ClinicNamesListAPIView(generics.ListAPIView):
    queryset = Clinic.objects.filter(is_visible=True)
    serializer_class = ClinicProfileNamesSerializer
