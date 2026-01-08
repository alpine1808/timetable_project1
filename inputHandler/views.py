from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UploadFileForm
from .models import ClassInfo
import pandas as pd
import re

def parse_time_str(time_str):
    if not isinstance(time_str, str): return 0, 0
    times = re.findall(r'\d+', time_str)
    if len(times) >= 2: return int(times[0]), int(times[1])
    return 0, 0

def clean_excel_code(val):
    s = str(val).strip()
    if not s or s.lower() == 'nan': return ""
    if '.' in s: return s.split('.')[0]
    return s

def parse_week_string(week_str):
    if not isinstance(week_str, str) or not week_str or week_str.lower() == 'nan':
        return ""
    week_set = set()
    parts = week_str.split(',')
    for part in parts:
        part = part.strip()
        if '-' in part: 
            try:
                nums = re.findall(r'\d+', part)
                if len(nums) >= 2:
                    start, end = int(nums[0]), int(nums[1])
                    if start <= end:
                        week_set.update(range(start, end + 1))
            except: continue
        else: 
            try:
                if part.isdigit(): week_set.add(int(part))
            except: continue
            
    if not week_set: return ""
    return ",".join(map(str, sorted(list(week_set))))

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                df = pd.read_excel(request.FILES['file'], header=2)
                df.columns = df.columns.str.strip()
                ClassInfo.objects.all().delete()
                
                new_classes = []
                for index, row in df.iterrows():
                    ma_lop = clean_excel_code(row.get('Mã_lớp'))
                    if not ma_lop: continue

                    start, end = parse_time_str(str(row.get('Thời_gian', '')))
                    
                    raw_week = str(row.get('Tuần', ''))
                    clean_week = parse_week_string(raw_week)
                    ma_lop_kem = clean_excel_code(row.get('Mã_lớp_kèm'))
                    
                    item = ClassInfo(
                        class_code=ma_lop,
                        management_code=clean_excel_code(row.get('Mã_QL')),
                        course_code=str(row.get('Mã_HP', '')).strip(),
                        course_name=str(row.get('Tên_HP', '')).strip(),
                        school_name=str(row.get('Trường_Viện_Khoa', '')).strip(),
                        associated_class_code=ma_lop_kem,
                        requires_experiment=str(row.get('Cần_TN', '')).strip().lower() not in ['nan', ''],
                        class_type=str(row.get('Loại_lớp', '')).strip(),
                        notes=str(row.get('Ghi_chú', '')).strip(),
                        day=int(float(row.get('Thứ', 8))) if str(row.get('Thứ', '')).replace('.','').isdigit() else 8,
                        start_time=start,
                        end_time=end,
                        week_list=clean_week,
                        room=str(row.get('Phòng', '')).strip()
                    )
                    new_classes.append(item)
                
                ClassInfo.objects.bulk_create(new_classes)
                messages.success(request, f"Đã nhập {len(new_classes)} lớp.")
                return redirect('timetable_view')

            except Exception as e:
                print(e)
                messages.error(request, f"Lỗi: {e}")
    else:
        form = UploadFileForm()
    return render(request, 'inputHandler/upload.html', {'form': form})