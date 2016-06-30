from django.contrib import admin
from libapp.models import Book, Dvd, LibUser, Libitem,Suggestion,UserProfile
import datetime
# Register your models here.

def renew(modeladmin,request,queryset):
    for item in queryset:
        if item.checked_out == True:
            item.duedate = datetime.date.today() + datetime.timedelta(21)
            item.save()

class BookInline(admin.StackedInline):
    model = Book  # This shows all fields of Book.
    fields = [('title', 'author'), 'duedate']   #  Customizes to show only certain fields
    extra = 0

class DvdInline(admin.TabularInline):
    model = Dvd
    fields = [('checked_out','duedate', 'duration','itemtype','maker', 'num_chkout', 'pubyr', 'rating', 'title', 'user')]
    extra = 0

class LibUserAdmin(admin.ModelAdmin):
    # fields = [('username'), ('first_name', 'last_name')]
    inlines = [BookInline,DvdInline]



class BookAdmin(admin.ModelAdmin):
    fields = [('title', 'author', 'pubyr'), ('checked_out', 'itemtype', 'user', 'duedate'),'category']
    list_display = ('title', 'borrower','overdue')
    list_filter = ('category',)
    search_fields = ('title',)
    def borrower(self, obj=None):
        if obj.checked_out == True:
            return obj.user     #Returns the user who has borrowed this book
        else:
            return ''
    actions = [renew]
class DvdAdmin(admin.ModelAdmin):
    fields = [('title','maker','pubyr'),('checked_out','itemtype','user','duedate'),('rating')]
    list_display = ('title','borrower','rating')

    def borrower(self,obj=None):
        if obj.checked_out == True:
            return obj.user
        else:
            return ''
    actions = [renew]


admin.site.register(Book,BookAdmin)
admin.site.register(Dvd,DvdAdmin)
admin.site.register(LibUser,LibUserAdmin)
admin.site.register(Suggestion)
admin.site.register(UserProfile)
