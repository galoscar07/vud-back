from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from footerlabels.models import Footerlabels, MedicalUnityTypes, AcademicDegree, Speciality, MedicalSkills, \
    ClinicSpecialities, MedicalFacilities
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
