from django.contrib import admin
from App.models import *

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(BasicInfo)
admin.site.register(SkillModel)
admin.site.register(IntermediateSkillModel)
admin.site.register(FieldOfStudyModel)
admin.site.register(DegreeModel)
admin.site.register(InstituteNameModel)
admin.site.register(EducationModel)
admin.site.register(JobModel)