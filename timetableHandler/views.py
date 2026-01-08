from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from inputHandler.models import ClassInfo
from .models import SelectedClass
from .logic import check_conflict

def timetable_view(request):
    selected_objs = SelectedClass.objects.all().select_related('class_info')
    current_schedule = [s.class_info for s in selected_objs]

    search_query = request.GET.get('q', '').strip()
    search_results = []
    
    if search_query:
        raw_results = ClassInfo.objects.filter(
            Q(course_code__iexact=search_query) | 
            Q(class_code__iexact=search_query) |   
            Q(course_name__icontains=search_query)
        ).order_by('class_code')

        course_codes_in_result = raw_results.values_list('course_code', flat=True).distinct()
        
        courses_have_bt = set(ClassInfo.objects.filter(
            course_code__in=course_codes_in_result,
            class_type='BT'
        ).values_list('course_code', flat=True))

        processed_codes = set()
        
        for item in raw_results:
            if item.class_code in processed_codes: continue

            if item.class_type == 'LT' and item.course_code in courses_have_bt:
                continue

            combo = {
                'main': item,
                'sub': None,
                'conflict': False,
                'conflict_reason': ''
            }

            if item.associated_class_code and item.associated_class_code != item.class_code:
                sub_class = ClassInfo.objects.filter(class_code=item.associated_class_code).first()
                combo['sub'] = sub_class
            
            is_conflict, conflict_with = check_conflict(item, current_schedule)
            if is_conflict:
                combo['conflict'] = True
                combo['conflict_reason'] = f"Trùng với {conflict_with.course_name} ({conflict_with.class_code})"
            
            if not combo['conflict'] and combo['sub']:
                is_conflict_sub, conflict_with_sub = check_conflict(combo['sub'], current_schedule)
                if is_conflict_sub:
                    combo['conflict'] = True
                    combo['conflict_reason'] = f"Lớp đi kèm trùng với {conflict_with_sub.course_name}"

            search_results.append(combo)
            processed_codes.add(item.class_code)

    return render(request, 'timetableHandler/index.html', {
        'schedule': selected_objs,
        'results': search_results,
        'search_query': search_query
    })

def add_class(request, class_id):
    try:
        main_class = ClassInfo.objects.get(id=class_id)
        SelectedClass.objects.create(class_info=main_class)
        
        if main_class.associated_class_code and main_class.associated_class_code != main_class.class_code:
            sub_class = ClassInfo.objects.filter(class_code=main_class.associated_class_code).first()
            if sub_class:
                SelectedClass.objects.create(class_info=sub_class)
                messages.success(request, f"Đã đăng ký Combo: {main_class.course_name}")
            else:
                messages.warning(request, f"Lưu ý: Không tìm thấy lớp kèm {main_class.associated_class_code}")
        else:
            messages.success(request, f"Đã đăng ký: {main_class.course_name}")
            
    except Exception as e:
        messages.error(request, f"Lỗi: {e}")
        
    return redirect('timetable_view')

def remove_class(request, item_id):
    try:
        SelectedClass.objects.filter(id=item_id).delete()
        messages.success(request, "Đã hủy lớp.")
    except: pass
    return redirect('timetable_view')