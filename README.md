# OpenShop — RESTful API untuk submission Dicoding

Repository ini adalah implementasi minimal RESTful API untuk tugas submission pada kelas "Belajar Back-End Pemula dengan Python" (Dicoding). API menyediakan operasi CRUD untuk resource `Product` sesuai spesifikasi tugas.

Persyaratan
- Python 3.10
- Django 4.2
- djangorestframework

Environment variables
- Aplikasi membaca `SECRET_KEY` dari environment variable `DJANGO_SECRET_KEY`. Untuk development Anda dapat set sementara di PowerShell:

```powershell
$env:DJANGO_SECRET_KEY = "your-secret-key-here"
```

Endpoint utama
- POST /products/  -> membuat product (201)
- GET /products/   -> list product (response body: {"products": [...]})
- GET /products/{id}/ -> detail product (200) atau 404 dengan body {"detail": "Not found."}
- PUT /products/{id}/ -> update product (200) atau 404/400
- DELETE /products/{id}/ -> soft delete (204) — product tetap ada di DB dengan `is_delete: true`

Model & behavior penting
- Model `Product` menggunakan UUID untuk `id` dan atribut `is_delete` untuk soft-delete.
- Serializer menambahkan field terhitung `final_price` (price - discount, minimal 0).
- GET detail mengembalikan product meskipun sudah di-soft-delete. PUT/DELETE hanya bekerja pada product yang belum dihapus.
