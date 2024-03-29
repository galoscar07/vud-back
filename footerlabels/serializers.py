from rest_framework import serializers

from authentication.models import CollaboratorDoctor
from footerlabels.models import Footerlabels, MedicalUnityTypes, AcademicDegree, Speciality, MedicalSkills, \
    ClinicSpecialities, MedicalFacilities, BannerCards, AddSense, Tag, BlogPost


class FooterlabelsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Footerlabels
        fields = ['id', 'label', 'link']


class MedicalUnityTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalUnityTypes
        fields = ['id', 'label']


class AcademicDegreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicDegree
        fields = ['id', 'label']


class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        fields = ['id', 'label']


class MedicalSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalSkills
        fields = ['id', 'label']


class ClinicSpecialitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicSpecialities
        fields = ['id', 'label']


class MedicalFacilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalFacilities
        fields = '__all__'


class BannerCardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerCards
        fields = '__all__'


class AddsCardsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddSense
        fields = '__all__'


class CollaboratorDoctorSerializer(serializers.ModelSerializer):
    academic_degree = AcademicDegreeSerializer(many=True, read_only=True)
    medical_skill = MedicalSkillsSerializer(many=True, read_only=True)
    speciality = SpecialitySerializer(many=True, read_only=True)

    class Meta:
        model = CollaboratorDoctor
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class BlogPostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = '__all__'
