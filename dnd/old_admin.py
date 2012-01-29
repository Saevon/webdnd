from django.contrib import admin
from library.models import *

# General
admin.site.register(Source)
admin.site.register(DieRoll)
admin.site.register(LibraryAccount)

# Rules
admin.site.register(Rule)
admin.site.register(Term)
admin.site.register(Article)
admin.site.register(Example)

#Items
class MaterialAdmin(admin.ModelAdmin):
	list_display = ('title','hardness','density')

class ItemAdmin(admin.ModelAdmin):
	list_display = ('title','formatted_price')

admin.site.register(Material, MaterialAdmin)
admin.site.register(Gem, ItemAdmin)
admin.site.register(ArtObject, ItemAdmin)
admin.site.register(MagicArtObject, ItemAdmin)
admin.site.register(PhysicalEnhancement)
admin.site.register(MagicEnhancement)
admin.site.register(Weapon, ItemAdmin)
admin.site.register(MagicWeapon, ItemAdmin)
admin.site.register(Armor, ItemAdmin)
admin.site.register(MagicArmor, ItemAdmin)
admin.site.register(Shield, ItemAdmin)
admin.site.register(MagicShield, ItemAdmin)
admin.site.register(WondrousMagicItem, ItemAdmin)
admin.site.register(Poison, ItemAdmin)
admin.site.register(Ammunition, ItemAdmin)
admin.site.register(MagicAmmunition, ItemAdmin)
admin.site.register(Vehicle, ItemAdmin)
admin.site.register(Container, ItemAdmin)
admin.site.register(AdventuringGear, ItemAdmin)
admin.site.register(Modifier)
