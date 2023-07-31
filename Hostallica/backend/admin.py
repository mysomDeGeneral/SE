from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from backend.models import Student, Hall, Room, Booking, HallManager, Message, HallImage
from .forms import StudentCreationForm, StudentChangeForm
# Register your models here.

class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number','occupants','price','floor','hall',]

class HallAdmin(admin.ModelAdmin):
    list_display = ['name','capacity']

class BookingAdmin(admin.ModelAdmin):
    list_display = ['student','room','hall','date','paid']



class StudentAdmin(BaseUserAdmin):
    add_form = StudentCreationForm
    form = StudentChangeForm
    model = Student
    list_display = ['name','username','phone','room','program','is_active']
    list_filter = ('is_active',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('name','phone','picture','program','room')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
   
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name','username','phone','picture','program','room', 'password1', 'password2'),
        }),
    )
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()


admin.site.register(Student, StudentAdmin)  
admin.site.register(Message)
admin.site.register(HallManager)
admin.site.register(HallImage)

admin.site.unregister(Group)


custom_models = [Hall, Room, Booking]
custom_models_admin = [HallAdmin, RoomAdmin, BookingAdmin]

for model, model_admin in zip(custom_models, custom_models_admin):
    admin.site.register(model, model_admin)