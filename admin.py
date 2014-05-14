from django.contrib import admin

from display.models import UserProfile, Letter, Template
# Register your models here.

class TemplateAdmin(admin.ModelAdmin):
    fields = ['name', 'subject', 'template']

class LetterAdmin(admin.ModelAdmin):
    fields = ['developer', 'game', 'written', 'text1', 'text2', 'template']

class ProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'signature', 'devlist']
    
admin.site.register(Template, TemplateAdmin)
admin.site.register(Letter, LetterAdmin)
admin.site.register(UserProfile, ProfileAdmin)
