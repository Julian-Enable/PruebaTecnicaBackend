from django.contrib import admin
from documents.models import Document, DocumentDownloadAudit, DocumentStateAudit


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'mime_type', 'validation_status', 'created_at')
    list_filter = ('validation_status', 'mime_type', 'bucket_provider')
    search_fields = ('name', 'company__name', 'bucket_key')
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(DocumentDownloadAudit)
class DocumentDownloadAuditAdmin(admin.ModelAdmin):
    list_display = ('document', 'actor', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('document__name', 'actor__username')


@admin.register(DocumentStateAudit)
class DocumentStateAuditAdmin(admin.ModelAdmin):
    list_display = ('document', 'action', 'actor', 'from_status', 'to_status', 'created_at')
    list_filter = ('action', 'created_at')
    search_fields = ('document__name', 'actor__username')

