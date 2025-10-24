from django.contrib import admin
from validation.models import ValidationFlow, ValidationStep, ValidationInstance, ValidationAction


@admin.register(ValidationFlow)
class ValidationFlowAdmin(admin.ModelAdmin):
    list_display = ('document', 'enabled', 'created_at')
    list_filter = ('enabled',)
    search_fields = ('document__name',)


@admin.register(ValidationStep)
class ValidationStepAdmin(admin.ModelAdmin):
    list_display = ('flow', 'order', 'approver_user_id', 'created_at')
    list_filter = ('order',)
    search_fields = ('flow__document__name',)


@admin.register(ValidationInstance)
class ValidationInstanceAdmin(admin.ModelAdmin):
    list_display = ('flow', 'status', 'current_max_order_approved', 'updated_at')
    list_filter = ('status',)
    search_fields = ('flow__document__name',)


@admin.register(ValidationAction)
class ValidationActionAdmin(admin.ModelAdmin):
    list_display = ('instance', 'action', 'actor_user_id', 'step_order', 'created_at')
    list_filter = ('action', 'created_at')
    search_fields = ('instance__flow__document__name',)

