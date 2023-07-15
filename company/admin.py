from django.contrib import admin

from company import models

# Register your models here.

admin.site.register(models.Company)
admin.site.register(models.ShortList)

admin.site.register(models.Test_generation)
admin.site.register(models.Question)
admin.site.register(models.Choice)
admin.site.register(models.UserAnswer)
admin.site.register(models.category)
admin.site.register(models.test_score)
admin.site.register(models.test_shortlist)
admin.site.register(models.final_shortlist)