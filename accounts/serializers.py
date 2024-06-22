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
            'is_alumni', 'is_lecturer', 'isAdmin', 'is_verified','phone_number', 'bio', 'linked_in_url', 'x_in_url',
            'followers_count', 'following_count', 'created_at', 'updated_at','url'
        ]
        read_only_fields = ('created_at', 'updated_at', 'followers_count', 'following_count')
    
    def get_followers_count(self, obj):
        return obj.followers.count()

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

    def get_follower_name(self, obj):
        return f"{obj.follower.user.first_name} {obj.follower.user.last_name}"

    def get_followed_name(self, obj):
        return f"{obj.followed.user.first_name} {obj.followed.user.last_name}"
    
    def get_follower_url(self, obj):
        request = self.context.get('request')
        if obj.follower and obj.follower.pk:
            return request.build_absolute_uri(obj.follower.get_absolute_url())
        return None

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
        fields = ['id', 'url', 'user', 'profile_picture', 'is_verified']
        read_only_fields = ['profile_picture', "is_verified"]