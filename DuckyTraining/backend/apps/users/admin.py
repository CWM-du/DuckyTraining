from django.contrib import admin
from .models import ProfileUserTraining

@admin.register(ProfileUserTraining)
class ProfileUserTrainingAdmin(admin.ModelAdmin):
    list_display = ('user', 'temporal_level', 'current_streak', 'last_streak_date')
    list_filter = ('temporal_level',)
    search_fields = ('user__username',)