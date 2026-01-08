from inputHandler.models import ClassInfo
from .models import SelectedClass

def parse_week_to_set(week_str):
    if not week_str: return set()
    return set(map(int, week_str.split(',')))

def check_conflict(new_class, existing_classes):
    new_weeks = parse_week_to_set(new_class.week_list)
    
    for existing in existing_classes:
        if new_class.day != existing.day:
            continue
        if (new_class.start_time < existing.end_time) and (existing.start_time < new_class.end_time):
            exist_weeks = parse_week_to_set(existing.week_list)
            intersection = new_weeks & exist_weeks            
            if intersection:
                return True, existing 
                
    return False, None