from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TypeOfSportsSerializers, PlyearDetailsSerializers, LeagueSerializers, AchievementDetailsSerializers
from .models import Category, League, PlayerDetails,  AchievementDetails
from django.db import transaction
# Create your views here.
class AddAllInformationsApiView(GenericAPIView):
    def post(self, request):
        data = request.data
        
        category_type_data = data.get("type_of_sport_info",{})
        category_serializers = TypeOfSportsSerializers(data = category_type_data)
        
        if category_serializers.is_valid():
            try:
                existing_category  = Category.objects.get(title = category_type_data['title'])
                category_instance = existing_category
                category_message = "Category is already provided, add the other data under these"
            except Category.DoesNotExist:
                category_serializers.is_valid(raise_exception = True)
                category_instance = category_serializers.save()
                category_message = "new category added"
            
            league_data = data.get("league_data_info",{})
            league_data['related_sport'] = category_instance.id 
            league_data_serializer = LeagueSerializers(data = league_data)
            if league_data_serializer.is_valid():
                try:
                    existing_league_data_info = League.objects.get(title = league_data['title'])  
                    league_instance = existing_league_data_info
                    league_message = "this league is already registered"
                except League.DoesNotExist:
                    league_data_serializer.is_valid(raise_exception = True)
                    league_instance = league_data_serializer.save()
                    league_message = "New league added"
                    
                try:
                    with transaction.atomic():
                        player_data = data.get("player_info", {})
                        
                        ## checking that the player is exsited or not ##
                        existing_player_info = PlayerDetails.objects.filter(name = player_data['name']).first()
                        if existing_player_info:
                            return Response({"message" : "The player's detail is already existed"}, status = status.HTTP_400_BAD_REQUEST)
                        player_data['league'] = league_instance.id
                        player_data_serializer = PlyearDetailsSerializers(data = player_data)
                        if player_data_serializer.is_valid():
                            player_data_instance = player_data_serializer.save()
                            
                            achievement_data = data.get("achievement_info", {})
                            achievement_data['player'] = player_data_instance.id 
                            achievement_data_serializer = AchievementDetailsSerializers(data = achievement_data)
                            if achievement_data_serializer.is_valid():
                                achievement_data_serializer.save()
                                response_data = {
                                        "type_of_sport_info" : TypeOfSportsSerializers(category_instance).data if category_instance else {},
                                        "league_data_info" : league_data_serializer.data,
                                        "player_info" : player_data_serializer.data,
                                        "achievement_info" : achievement_data_serializer.data
                                    }
                                return Response({
                                    "msg" : league_message,
                                    "data" : response_data
                                }, status = status.HTTP_201_CREATED)
                            else:
                                return Response({"msg" : achievement_data_serializer.errors}, status= 400)
                        else:
                            return Response({"msg" : player_data_serializer.errors}, status= 400)
                except:
                    return Response({"message" : "some thing is wrong"})
            else:
                return Response({"msg" : league_data_serializer.errors})
        else:
            return Response({"msg" : category_serializers.errors}, status = 400)
                        