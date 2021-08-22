from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # token['first_name'] = user.first_name
        # token['middle_name'] = user.middle_name
        # token['last_name'] = user.last_name
        # token['id'] = user.id
        # token['email'] = user.email
        # token['role'] = user.role

        return token
