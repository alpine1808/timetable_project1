from django.db import models

class ClassInfo(models.Model):
    # --- Định danh lớp học ---
    class_code = models.CharField(max_length=20, verbose_name="Mã_lớp")      # Mã_lớp
    management_code = models.CharField(max_length=20, verbose_name="Mã_QL")  # Mã_QL (Mã quản lý)
    
    # --- Thông tin môn học ---
    course_code = models.CharField(max_length=20, verbose_name="Mã_HP")
    course_name = models.CharField(max_length=200, verbose_name="Tên_HP")
    school_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Trường_Viện_Khoa") # Trường_Viện_Khoa
    
    # --- Thông tin ràng buộc (Quan trọng cho thuật toán) ---
    associated_class_code = models.CharField(max_length=20, blank=True, null=True, verbose_name="Mã_lớp_kèm") # Mã_lớp_kèm
    requires_experiment = models.BooleanField(default=False, verbose_name="Cần_TN") # Cần_TN
    class_type = models.CharField(max_length=10, blank=True, null=True, verbose_name="Loại_lớp") # Loại_lớp (LT, BT)

    # --- Thông tin thời gian & địa điểm ---
    day = models.IntegerField(verbose_name="Thứ")
    start_time = models.IntegerField(verbose_name="BĐ") 
    end_time = models.IntegerField(verbose_name="KT")  
    room = models.CharField(max_length=50, blank=True, null=True, verbose_name="Phòng")
    week_list = models.CharField(max_length=100, verbose_name="Tuần")
    
    # --- Khác ---
    notes = models.TextField(blank=True, null=True, verbose_name="Ghi_chú") 

    def __str__(self):
        return f"{self.class_code} - {self.course_name} ({self.class_type})"