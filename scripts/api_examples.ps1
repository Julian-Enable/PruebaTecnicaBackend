# API Usage Examples for ERP Documents

# Base URL
$BASE_URL = "http://localhost:8000"

Write-Host "=" -ForegroundColor Cyan
Write-Host "ERP Documents API - Usage Examples" -ForegroundColor Cyan
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""

# 1. Get JWT Token
Write-Host "1. Getting JWT Token..." -ForegroundColor Green
$tokenResponse = Invoke-RestMethod -Uri "$BASE_URL/api/token/" `
    -Method Post `
    -ContentType "application/json" `
    -Body '{"username":"uploader","password":"test123"}'

$TOKEN = $tokenResponse.access
Write-Host "   Token obtained: $($TOKEN.Substring(0,20))..." -ForegroundColor Gray

# 2. Get presigned PUT URL
Write-Host "`n2. Getting presigned PUT URL..." -ForegroundColor Green
$uploadRequest = @{
    bucket_key = "test/documents/soat-2025.pdf"
    mime_type = "application/pdf"
} | ConvertTo-Json

$uploadResponse = Invoke-RestMethod -Uri "$BASE_URL/api/storage/presign-put/" `
    -Method Post `
    -Headers @{Authorization="Bearer $TOKEN"} `
    -ContentType "application/json" `
    -Body $uploadRequest

Write-Host "   Upload URL: $($uploadResponse.upload_url.Substring(0,50))..." -ForegroundColor Gray

# 3. Create document (assuming file was uploaded)
Write-Host "`n3. Creating document with validation flow..." -ForegroundColor Green

# You'll need to replace these UUIDs with actual ones from seed data
$createDocRequest = @{
    company_id = "REPLACE_WITH_COMPANY_UUID"
    entity = @{
        entity_type = "vehicle"
        entity_id = "22222222-2222-2222-2222-222222222222"
    }
    document = @{
        name = "soat.pdf"
        mime_type = "application/pdf"
        size_bytes = 123456
        bucket_key = "test/documents/soat-2025.pdf"
    }
    validation_flow = @{
        enabled = $true
        steps = @(
            @{order = 1; approver_user_id = "SEBASTIAN_UUID"},
            @{order = 2; approver_user_id = "CAMILO_UUID"},
            @{order = 3; approver_user_id = "JUAN_UUID"}
        )
    }
} | ConvertTo-Json -Depth 5

Write-Host "   Request body prepared (update UUIDs in script)" -ForegroundColor Yellow

# Uncomment when you have valid UUIDs
# $docResponse = Invoke-RestMethod -Uri "$BASE_URL/api/documents/" `
#     -Method Post `
#     -Headers @{Authorization="Bearer $TOKEN"} `
#     -ContentType "application/json" `
#     -Body $createDocRequest
# 
# $DOC_ID = $docResponse.id
# Write-Host "   Document created: $DOC_ID" -ForegroundColor Gray

# 4. Approve document
Write-Host "`n4. Example: Approve document at highest order..." -ForegroundColor Green
Write-Host "   POST $BASE_URL/api/documents/{doc_id}/approve/" -ForegroundColor Gray
Write-Host '   {"actor_user_id":"JUAN_UUID","reason":"Approved"}' -ForegroundColor Gray

# 5. Download document
Write-Host "`n5. Example: Download document..." -ForegroundColor Green
Write-Host "   GET $BASE_URL/api/documents/{doc_id}/download/" -ForegroundColor Gray

# 6. View API docs
Write-Host "`n6. Access API Documentation:" -ForegroundColor Green
Write-Host "   Swagger UI: $BASE_URL/api/docs/" -ForegroundColor Cyan
Write-Host "   Admin Panel: $BASE_URL/admin/" -ForegroundColor Cyan

Write-Host "`n" + "=" * 50 -ForegroundColor Cyan
Write-Host "To run seed data and get actual UUIDs:" -ForegroundColor Yellow
Write-Host "   python manage.py shell < scripts\seed_data.py" -ForegroundColor Gray
Write-Host "=" -ForegroundColor Cyan
