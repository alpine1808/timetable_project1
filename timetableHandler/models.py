from django.db import models
from inputHandler.models import ClassInfo

class SelectedClass(models.Model):
    class_info = models.ForeignKey(ClassInfo, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Đã chọn: {self.class_info.class_code}"