from rest_framework import serializers
from .models import Category, League, PlayerDetails,  AchievementDetails


class TypeOfSportsSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        
class LeagueSerializers(serializers.ModelSerializer):
    class Meta:
        model = League
        fields = "__all__"
        
class PlyearDetailsSerializers(serializers.ModelSerializer):
    class Meta:
        model = PlayerDetails
        fields = "__all__"

class AchievementDetailsSerializers(serializers.ModelSerializer):
    class Meta:
        model = AchievementDetails
        fields = "__all__"