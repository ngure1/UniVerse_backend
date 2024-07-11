from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from .models import UserProfile, MyUser, Address, Education, Follow as Follower

# customUser Serializer
class MyUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = MyUser
        fields = ['id', 'email', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    #AddressModel Serializer
class AddressSerializer(serializers.ModelSerializer):
   # url = serializers.HyperlinkedIdentityField(view_name='address-detail',lookup_field='pk')
    class Meta:
        model = Address
        fields = ('city', 'country', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user.user_profile)
        
        
# UserProfile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    user = MyUserSerializer(read_only=True)
    address=AddressSerializer(read_only=True)
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(view_name='userprofile-detail',lookup_field='pk')


    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'profile_picture', 'is_student','address',
            'is_alumni', 'is_lecturer', 'isAdmin', 'is_verified', 'is_company', 'job_role', 'course', 'organization','phone_number', 'bio', 'linked_in_url', 'x_in_url',
            'followers_count', 'following_count', 'created_at', 'updated_at','url'
        ]
        read_only_fields = ('created_at', 'updated_at', 'followers_count', 'following_count')
    
    #Define a method to retrieve the followers_count for the followers_count serializermethodfield
    def get_followers_count(self, obj):
        return obj.followers.count()

    #Define a method to retrieve the following_count for the following_count serializermethodfield
    def get_following_count(self, obj):
        return obj.following.count()



# EducationModel Serializer
class EducationSerializer(serializers.ModelSerializer):
    owner = UserProfileSerializer(read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='education-detail',lookup_field='pk')
    class Meta:
        model = Education
        fields = ('owner', 'institution_name', 'field_of_study', 'start_date', 'end_date', 'created_at', 'updated_at', 'url')
        read_only_fields = ("updated_at", "created_at")



class FollowerSerializer(serializers.ModelSerializer):
    follower_name = serializers.SerializerMethodField()
    followed_name = serializers.SerializerMethodField()
    follower_url = serializers.SerializerMethodField()
    followed_url = serializers.SerializerMethodField()
    class Meta:
        model = Follower
        fields = ['id','follower_name','followed_name','created_at','follower_url','followed_url']

    #Define a method to retrieve the follower_name for the follower_name serializermethodfield
    def get_follower_name(self, obj):
        return f"{obj.follower.user.first_name} {obj.follower.user.last_name}"

    #Define a method to retrieve the followed_name for followed_name serializermethodfield
    def get_followed_name(self, obj):
        return f"{obj.followed.user.first_name} {obj.followed.user.last_name}"
    
    #Define a method to retrieve the follower_url for the follower_url serializermethodfield
    def get_follower_url(self, obj):
        request = self.context.get('request')
        if obj.follower and obj.follower.pk:
            return request.build_absolute_uri(obj.follower.get_absolute_url())
        return None

    #Define a method to retrieve the followed_url for the followed_url serializermethodfield
    def get_followed_url(self, obj):
        request = self.context.get('request')
        if obj.followed and obj.followed.pk:
            return request.build_absolute_uri(obj.followed.get_absolute_url())
        return None
    
    
    
    # user serializer with fewer fields
class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name']

    # userprofile serializer with fewer fields
class UserProfileSimpleSerializer(serializers.ModelSerializer):
    user = UserNameSerializer(read_only=True)
    url=serializers.HyperlinkedIdentityField(view_name='userprofile-detail',lookup_field='pk')
    class Meta:
        model = UserProfile
        fields = [
            'id',
            'url',
            'user',
            'profile_picture',
            'is_verified',
            "is_student",
            "is_alumni",
            "is_lecturer",
            "is_company",
            'job_role',
            'course',
            'organization',
            ]
        read_only_fields = ['profile_picture', "is_verified"]