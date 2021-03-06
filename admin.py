from django.contrib import admin

from display.models import UserProfile, Letter, Template
# Register your models here.

class TemplateAdmin(admin.ModelAdmin):
    fields = ['name', 'subject', 'template']

class LetterAdmin(admin.ModelAdmin):
    fields = ['developer', 'game', 'written','subject', 'text1', 'text2', 'template']

class ProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'signature', 'devlist', 'ticket_count', 'last_donation', 'donation_count']
    
admin.site.register(Template, TemplateAdmin)
admin.site.register(Letter, LetterAdmin)
admin.site.register(UserProfile, ProfileAdmin)
