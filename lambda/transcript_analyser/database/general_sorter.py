from CourseSuggestionAlgorithms import *
from util import *
from db import get_keywords_collection, convert_courses, get_all_courses_db_collection


def general_sorter_function(course_arr, studentId, student_name, analysis_language, requirement_ids_arr):
    # Preprocess data to convert to desired structure
    processed_data = get_keywords_collection()

    print('processed_data: ', processed_data)
    # Generate all classification dynamically
    basic_classification_en = convert_courses(processed_data, 'en')
    basic_classification_zh = convert_courses(processed_data, 'zh')
    all_course_db = get_all_courses_db_collection()
    print('basic_classification_en: ', basic_classification_en)
    print('basic_classification_zh: ', basic_classification_zh)
    print('all_course_db: ', all_course_db)

    result = Classifier(course_arr, all_course_db,
               basic_classification_en, basic_classification_zh, studentId, student_name, analysis_language, requirement_ids_arr)
    return result