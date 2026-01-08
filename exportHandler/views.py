import pandas as pd
from django.http import HttpResponse
from timetableHandler.models import SelectedClass

def export_schedule_excel(request):
    selected_items = SelectedClass.objects.select_related('class_info').all()
    
    if not selected_items.exists():
        return HttpResponse("Chưa có lớp nào được chọn để xuất file.", content_type="text/plain")

    associated_codes_in_use = set()
    for item in selected_items:
        assoc_code = item.class_info.associated_class_code
        if assoc_code and assoc_code != item.class_info.class_code:
            associated_codes_in_use.add(assoc_code)
    
    data_rows = []
    for item in selected_items:
        info = item.class_info

        if info.class_code in associated_codes_in_use:
            continue
            
        data_rows.append({
            "Tên HP": info.course_name,
            "Mã HP": info.course_code,
            "Mã lớp": info.class_code,
            "Thời gian": f"{info.start_time} - {info.end_time}",
            "Thứ": info.day,
            "Tuần": info.week_list,
            "Phòng": info.room
        })

    df = pd.read_json(pd.Series(data_rows).to_json(orient='records')) 
    df = pd.DataFrame(data_rows)

    if not df.empty:
        df = df.sort_values(by=['Thứ', 'Thời gian'])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=TKB_DuKien.xlsx'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='TKB Chính')

        worksheet = writer.sheets['TKB Chính']
        for column_cells in worksheet.columns:
            length = max(len(str(cell.value)) for cell in column_cells)
            worksheet.column_dimensions[column_cells[0].column_letter].width = length + 2

    return response