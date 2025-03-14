import sys
import json
from database.general_sorter import general_sorter_function


def analyze_transcript(str_courses, student_id, student_name, factor, language, str_courses_taiger_guided, requirement_ids="[]"):
    print("--------------------------")
    print("New Transcript Analyser")
    print("Python version:")
    print(sys.version)
    print("--------------------------")

    # print course:
    course = json.loads(str_courses)
    course_arr = json.loads(course)
    courses_taiger_guided = json.loads(str_courses_taiger_guided)
    courses_taiger_guided_arr = json.loads(courses_taiger_guided)
    requirement_ids_arr = json.loads(requirement_ids)
    course_arr = course_arr + courses_taiger_guided_arr
    print("requirement_ids_arr", requirement_ids_arr)

    result = general_sorter_function(
        course_arr, student_id, student_name, factor, language, requirement_ids_arr)

    return result
