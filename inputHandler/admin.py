from django.contrib import admin
from .models import ClassInfo

@admin.register(ClassInfo)
class ClassInfoAdmin(admin.ModelAdmin):
    # Hiển thị tất cả các cột
    list_display = (
        'id',                    # ID tự tăng của Django (rất quan trọng để debug)
        'class_code',            # Mã lớp
        'management_code',       # Mã QL
        'course_code',           # Mã HP
        'course_name',           # Tên HP
        'school_name',           # Trường/Viện
        'associated_class_code', # Mã kèm
        'requires_experiment',   # Cần TN
        'class_type',            # Loại lớp
        'day',                   # Thứ
        'start_time',            # Giờ BĐ (int)
        'end_time',              # Giờ KT (int)
        'room',                  # Phòng
        'week_list',             # Tuần
        'notes'                  # Ghi chú
    )
    
    # Thanh tìm kiếm: Đã thêm tìm theo Mã HP cho tiện
    search_fields = ('class_code', 'course_name', 'course_code')
    
    # Bộ lọc bên phải: Đã thêm lọc theo Loại lớp
    list_filter = ('day', 'requires_experiment', 'school_name', 'class_type')