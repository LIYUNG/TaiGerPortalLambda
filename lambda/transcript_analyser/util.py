import json
import pandas as pd
from CourseSuggestionAlgorithms import *
from db import get_programs_analysis_collection
from bson import ObjectId  # Import ObjectId from pymongo or bson
import datetime

import gc
import sys
import os
import io

KEY_WORDS = 0
ANTI_KEY_WORDS = 1
DIFFERENTIATE_KEY_WORDS = 2
CATEGORY_NAME = 3

# naming convention


def isfloat(value):
    try:
        if value is None:
            return False
        float(value)
        return True
    except ValueError:
        return False


def ProgramCategoryInit(program_categories):
    df_PROG_SPEC_CATES = []
    df_PROG_SPEC_CATES_COURSES_SUGGESTION = []
    for idx, cat in enumerate(program_categories):
        PROG_SPEC_CAT = {cat['program_category']: [],
                         'credits': [], 'grades': [], 'requiredECTS': cat['requiredECTS'], 'maxScore': []}
        PROG_SPEC_CATES_COURSES_SUGGESTION = {cat['program_category']: [],
                                              }
        df_PROG_SPEC_CATES.append(pd.DataFrame(data=PROG_SPEC_CAT))
        df_PROG_SPEC_CATES_COURSES_SUGGESTION.append(
            pd.DataFrame(data=PROG_SPEC_CATES_COURSES_SUGGESTION))
    return df_PROG_SPEC_CATES, df_PROG_SPEC_CATES_COURSES_SUGGESTION


def CheckTemplateFormat(df_transcript, analysis_lang):
    if analysis_lang == 'zh':
        if 'course_chinese' not in df_transcript.columns or 'credits' not in df_transcript.columns or 'grades' not in df_transcript.columns:
            print("Error: Please check the student's transcript input.")
            print(
                " There must be course_chinese, credits and grades in student's course excel file.")
            sys.exit(1)
    elif analysis_lang == 'en':
        if 'course_english' not in df_transcript.columns or 'credits' not in df_transcript.columns or 'grades' not in df_transcript.columns:
            print("Error: Please check the student's transcript input.")
            print(
                " There must be course_english, credits and grades in student's course excel file.")
            sys.exit(1)


def CheckDBFormat(df_database):
    if 'all_course_chinese' not in df_database.columns:
        print("Error: Please check the database mongodb course format.")
        sys.exit(1)


def isOutputEnglish(df_transcript):

    if ~df_transcript['course_english'].isnull().any():
        # output English version
        print("Output English Version")
        return True

    # print(df_transcript['course_chinese'].isnull().any())
    if ~df_transcript['course_chinese'].isnull().any():
        print("Output Chinese Version")
        return False  # output CHinese version

    print("course_english course_chinese credits 和 grades not match. Please make sure you fill the template correctly")
    sys.exit(1)


def DataPreparation(df_database, df_transcript):
    df_database['all_course_chinese'] = df_database['all_course_chinese'].fillna(
        '-')
    if 'all_course_english' in df_database.columns:
        df_database['all_course_english'] = df_database['all_course_english'].str.lower()
    # unify course naming convention
    if 'course_chinese' in df_transcript.columns:
        df_transcript = Naming_Convention_ZH(df_transcript)
    if 'course_english' in df_transcript.columns:
        df_transcript = Naming_Convention_EN(df_transcript)

    df_transcript = Credits_Preprocessing(df_transcript)
    df_transcript = Grades_Preprocessing(df_transcript)

    df_transcript['credits'] = df_transcript['credits'].astype(
        float, errors='ignore')
    df_transcript['grades'] = df_transcript['grades'].astype(
        float, errors='ignore')
    print("Prepared data successfully.")
    return df_database, df_transcript


def Credits_Preprocessing(df_course):
    # modify data in the same
    df_course['credits'] = df_course['credits'].fillna(0)
    return df_course


def Grades_Preprocessing(df_course):
    # modify data in the same
    df_course['grades'] = df_course['grades'].fillna('-')
    return df_course


def Naming_Convention_ZH(df_course):
    # modify data in the same, lowercase even for Chinese name!
    df_course['course_chinese'] = df_course['course_chinese'].fillna(
        '-').str.lower()

    # Create a mapping for replacements
    replacements = {
        '+': '＋',
        '1': '一',
        '2': '二',
        '3': '三',
        '(': '',
        '（': '',
        ')': '',
        '）': '',
        ' ': ''
    }

    # Apply replacements using a single loop
    for old, new in replacements.items():
        df_course['course_chinese'] = df_course['course_chinese'].str.replace(
            old, new, regex=False)

    return df_course


def Naming_Convention_EN(df_course):
    # Fill NaN values and convert to lowercase
    df_course['course_english'] = df_course['course_english'].fillna(
        '-').str.lower()

    # Create a mapping for replacements
    replacements = {
        '+': '＋',
        '(': '',
        '（': '',
        ')': '',
        '）': ''
    }

    # Apply replacements using a single loop
    for old, new in replacements.items():
        df_course['course_english'] = df_course['course_english'].str.replace(
            old, new, regex=False)

    return df_course


# mapping courses to target programs category
def CoursesToProgramCategoryMapping(df_PROG_SPEC_CATES, program_category_map, transcript_sorted_group_list, df_transcript_array_temp, isSuggestionCourse):
    for idx, trans_cat in enumerate(df_transcript_array_temp):
        # append sorted courses to program's category
        categ = program_category_map[idx]['program_category']
        trans_cat.rename(
            columns={transcript_sorted_group_list[idx]: categ}, inplace=True)
        # find the idx corresponding to program's category
        idx_temp = -1
        for idx2, cat in enumerate(df_PROG_SPEC_CATES):
            if categ == cat.columns[0]:
                idx_temp = idx2
                break
        # remove the redundant suggestion courses mapping to "Others" because those categories in Others are not advanced courses.
        if isSuggestionCourse:
            if idx != len(df_transcript_array_temp) - 1 and idx_temp == len(df_PROG_SPEC_CATES) - 1:
                continue
        df_PROG_SPEC_CATES[idx_temp] = pd.concat(
            [df_PROG_SPEC_CATES[idx_temp], trans_cat])
    return df_PROG_SPEC_CATES


# mapping courses to target programs category
def CoursesToProgramCategoryMappingNew(df_PROG_SPEC_CATES, program_category, baseCategoryToProgramMapping, transcript_sorted_group_list, df_transcript_array_temp, isSuggestionCourse):

    # ['GENERAL_PHYSICS', 'EE_ADVANCED_PHYSICS',...]
    # print(transcript_sorted_group_list)
    # [{'program_category': 'Mathematics', 'requiredECTS': 28, 'keywordSets': ['CALCULUS', 'ME_MATH']}, {...}]
    # print(program_category)
    # df array, Columns: [MECHANIK, credits, grades] Index: [], Empty DataFrame,  || Columns: [建議修課] Index: [], Empty DataFrame
    # print(df_transcript_array_temp)

    for idx, trans_cat in enumerate(df_transcript_array_temp):
        # append sorted courses to program's category
        # print(transcript_sorted_group_list[idx])
        # Use .get() to avoid KeyError and provide a default value if the key is not found
        categ = baseCategoryToProgramMapping.get(
            transcript_sorted_group_list[idx], None)

        if categ is not None:
            # Continue with your logic if the category is found
            # (append courses, etc.)
            trans_cat.rename(
                columns={'courses': categ['program_category']}, inplace=True)

            # remove column of ObjectId
            if transcript_sorted_group_list[idx] in trans_cat.columns:
                trans_cat.drop(
                    columns=[transcript_sorted_group_list[idx]], inplace=True)
            # find the idx corresponding to program's category
            idx_temp = -1
            for idx2, cat in enumerate(df_PROG_SPEC_CATES):
                if categ['program_category'] == cat.columns[0]:
                    idx_temp = idx2
                    break
            # remove the redundant suggestion courses mapping to "Others" because those categories in Others are not advanced courses.
            if isSuggestionCourse:
                if idx != len(df_transcript_array_temp) - 1 and idx_temp == len(df_PROG_SPEC_CATES) - 1:
                    continue
            df_PROG_SPEC_CATES[idx_temp] = pd.concat(
                [df_PROG_SPEC_CATES[idx_temp], trans_cat])
        else:
            print(
                f"Key {transcript_sorted_group_list[idx]} not found in baseCategoryToProgramMapping")

    return df_PROG_SPEC_CATES


# course sorting
def CourseSorting(df_transcript, df_category_data, transcript_sorted_group_map, column_name_en_zh):
    df_transcript['grades'] = df_transcript['grades'].astype(
        float, errors='ignore')
    for idx, subj in enumerate(df_transcript[column_name_en_zh]):
        if subj == '-':
            continue
        for idx2, cat in enumerate(transcript_sorted_group_map):
            # Put the rest of courses to Others
            categoryName = transcript_sorted_group_map[cat][CATEGORY_NAME]
            if (idx2 == len(transcript_sorted_group_map) - 1):
                temp_string = df_transcript['grades'][idx]
                temp0 = 0
                if isfloat(temp_string):
                    temp0 = {cat: categoryName, 'courses': subj, 'credits': df_transcript['credits'][idx],
                             'grades': float(df_transcript['grades'][idx])}
                else:
                    temp0 = {cat: categoryName, 'courses': subj, 'credits': df_transcript['credits'][idx],
                             'grades': df_transcript['grades'][idx]}

                df_temp0 = pd.DataFrame(data=temp0, index=[0])
                if not df_temp0.empty:
                    df_category_data[idx2] = pd.concat(
                        [df_category_data[idx2], df_temp0])
                continue

            # filter subject by keywords. and exclude subject by anti_keywords
            if any(keywords in subj for keywords in transcript_sorted_group_map[cat][KEY_WORDS] if not any(anti_keywords in subj for anti_keywords in transcript_sorted_group_map[cat][ANTI_KEY_WORDS])):
                temp_string = df_transcript['grades'][idx]
                temp = 0
                if temp_string is None:
                    temp = {cat: categoryName, 'courses': subj, 'credits': float(df_transcript['credits'][idx]),
                            'grades': df_transcript['grades'][idx]}
                else:
                    # failed subject not count
                    if ((isfloat(temp_string) and float(temp_string) < 60 and float(temp_string) and float(temp_string) > 4.5)
                            or "Fail" in str(temp_string) or "W" in str(temp_string) or "F" in str(temp_string) or "fail" in str(temp_string) or "退選" in str(temp_string) or "withdraw" in str(temp_string)):
                        continue
                    if isfloat(temp_string):
                        temp = {cat: categoryName, 'courses': subj, 'credits': float(df_transcript['credits'][idx]),
                                'grades': float(df_transcript['grades'][idx])}
                    else:
                        temp = {cat: categoryName, 'courses': subj, 'credits': float(df_transcript['credits'][idx]),
                                'grades': df_transcript['grades'][idx]}
                df_temp = pd.DataFrame(data=temp, index=[0])
                if not df_temp.empty:
                    df_category_data[idx2] = pd.concat(
                        [df_category_data[idx2], df_temp])
                break
    return df_category_data


def DatabaseCourseSorting(df_database, df_category_courses_sugesstion_data, transcript_sorted_group_map, column_name_en_zh):
    for idx, subj in enumerate(df_database[column_name_en_zh]):
        if subj == '-':
            continue
        for idx2, cat in enumerate(transcript_sorted_group_map):
            # Put the rest of courses to Others
            if (idx2 == len(transcript_sorted_group_map) - 1):
                temp = {'建議修課': subj}
                df_temp = pd.DataFrame(data=temp, index=[0])
                df_category_courses_sugesstion_data[idx2] = pd.concat(
                    [df_category_courses_sugesstion_data[idx2], df_temp])
                continue

            # filter database by keywords. and exclude subject by anti_keywords
            if any(keywords in subj for keywords in transcript_sorted_group_map[cat][KEY_WORDS] if not any(anti_keywords in subj for anti_keywords in transcript_sorted_group_map[cat][ANTI_KEY_WORDS])):
                temp = {'建議修課': subj}
                df_temp = pd.DataFrame(data=temp, index=[0])
                df_category_courses_sugesstion_data[idx2] = pd.concat(
                    [df_category_courses_sugesstion_data[idx2], df_temp])
                break
    return df_category_courses_sugesstion_data


def AppendCreditsCount(df_PROG_SPEC_CATES, program_category, factor):
    for idx, trans_cat in enumerate(df_PROG_SPEC_CATES):
        df_PROG_SPEC_CATES[idx]['credits'] = df_PROG_SPEC_CATES[idx]['credits'].astype(
            float, errors='ignore')
        credit_sum = df_PROG_SPEC_CATES[idx]['credits'].sum()
        category_credits_sum = {
            trans_cat.columns[0]: "sum", 'credits': credit_sum}
        df_category_credits_sum = pd.DataFrame(
            data=category_credits_sum, index=[0])
        df_PROG_SPEC_CATES[idx] = pd.concat(
            [df_PROG_SPEC_CATES[idx], df_category_credits_sum])
        maxScore = program_category[idx].get('maxScore', 0)
        category_credits_sum = {trans_cat.columns[0]: "ECTS轉換", 'credits': factor *
                                credit_sum, 'requiredECTS': program_category[idx]['requiredECTS'], 'maxScore': maxScore}
        df_category_credits_sum = pd.DataFrame(
            data=category_credits_sum, index=[0])
        df_PROG_SPEC_CATES[idx] = pd.concat(
            [df_PROG_SPEC_CATES[idx], df_category_credits_sum])
    return df_PROG_SPEC_CATES

# TODO: debug baseCategoryToProgramMapping, it keywordSets become object


def WriteToExcel(json_output, program_name, program_name_long, program_category, baseCategoryToProgramMapping, transcript_sorted_group_map, df_transcript_array_temp, df_category_courses_sugesstion_data_temp, program, factor):
    df_PROG_SPEC_CATES, df_PROG_SPEC_CATES_COURSES_SUGGESTION = ProgramCategoryInit(
        program_category)
    transcript_sorted_group_list = list(transcript_sorted_group_map)

    # Courses: mapping the students' courses to program-specific category
    df_PROG_SPEC_CATES = CoursesToProgramCategoryMappingNew(
        df_PROG_SPEC_CATES, program_category, baseCategoryToProgramMapping, transcript_sorted_group_list, df_transcript_array_temp, False)

    # Suggestion courses: mapping the sugesstion courses to program-specific category
    df_PROG_SPEC_CATES_COURSES_SUGGESTION = CoursesToProgramCategoryMappingNew(
        df_PROG_SPEC_CATES_COURSES_SUGGESTION, program_category, baseCategoryToProgramMapping, transcript_sorted_group_list, df_category_courses_sugesstion_data_temp, True)

    # append 總credits for each program category
    df_PROG_SPEC_CATES = AppendCreditsCount(
        df_PROG_SPEC_CATES, program_category, factor)

    # drop the Others, 建議修課
    for idx, trans_cat in enumerate(df_PROG_SPEC_CATES_COURSES_SUGGESTION):
        if (idx == len(df_PROG_SPEC_CATES_COURSES_SUGGESTION) - 1):
            df_PROG_SPEC_CATES_COURSES_SUGGESTION[idx].drop(
                columns=['Others', '建議修課'], inplace=True)

    # Write to Json
    json_output[program_name_long] = {
        'sorted': {}, 'suggestion': {}, 'scores': {}, 'fpso': "", 'admissionDescription': ""}

    fpso = program.get('fpso', "")
    admissionDescription = program.get('admissionDescription', "")
    gpaScoreBoundaryGPA = program.get('gpaScoreBoundaryGPA', 0)
    gpaScore = program.get('gpaScore', 0)
    gpaMinScore = program.get('gpaMinScore', 0)
    coursesScore = program.get('coursesScore', 0)
    cvScore = program.get('cvScore', 0)
    mlScore = program.get('mlScore', 0)
    rlScore = program.get('rlScore', 0)
    essayScore = program.get('essayScore', 0)
    gmatScore = program.get('gmatScore', 0)
    greScore = program.get('greScore', 0)
    workExperienceScore = program.get('workExperienceScore', 0)
    interviewScore = program.get('interviewScore', 0)
    testScore = program.get('testScore', 0)
    firstRoundConsidered = program.get('firstRoundConsidered', [])
    secondRoundConsidered = program.get('secondRoundConsidered', [])
    directRejectionScore = program.get('directRejectionScore', 0)
    directAdmissionScore = program.get('directAdmissionScore', 0)
    directRejectionSecondScore = program.get('directRejectionSecondScore', 0)
    directAdmissionSecondScore = program.get('directAdmissionSecondScore', 0)

    json_output[program_name_long]['fpso'] = fpso
    json_output[program_name_long]['admissionDescription'] = admissionDescription
    json_output[program_name_long]['scores'] = {
        'gpaScoreBoundaryGPA': gpaScoreBoundaryGPA,
        'gpaScore': gpaScore,
        'gpaMinScore': gpaMinScore,
        'coursesScore': coursesScore,
        'cvScore': cvScore,
        'mlScore': mlScore,
        'rlScore': rlScore,
        'essayScore': essayScore,
        'gmatScore': gmatScore,
        'greScore': greScore,
        'workExperienceScore': workExperienceScore,
        'interviewScore': interviewScore,
        'testScore': testScore,
        'firstRoundConsidered': firstRoundConsidered,
        'secondRoundConsidered': secondRoundConsidered,
        'directRejectionScore': directRejectionScore,
        'directAdmissionScore': directAdmissionScore,
        'directRejectionSecondScore': directRejectionSecondScore,
        'directAdmissionSecondScore': directAdmissionSecondScore,
    }

    for idx, sortedcourses in enumerate(df_PROG_SPEC_CATES):
        json_output[program_name_long]['sorted'][df_PROG_SPEC_CATES[idx].columns[0]] = json.loads(
            sortedcourses.to_json(orient='records', indent=4)
        )
        json_output[program_name_long]['suggestion'][df_PROG_SPEC_CATES[idx].columns[0]] = json.loads(
            df_PROG_SPEC_CATES_COURSES_SUGGESTION[idx].to_json(
                orient='records', indent=4)
        )

    gc.collect()  # Forced GC
    print("Save to " + program_name_long)


def Classifier(courses_arr, courses_db, basic_classification_en, basic_classification_zh, studentId, student_name, factor, analysis_language, requirement_ids_arr=[]):
    df_transcript = pd.DataFrame.from_dict(courses_arr)
    # TODO: move the checking mechanism to util.py!
    # Verify the format of transcript_course_list input
    CheckTemplateFormat(df_transcript, analysis_language)
    print("Checked input template successfully.")

    df_database = pd.DataFrame.from_dict(courses_db)
    # # Verify the format of course db
    CheckDBFormat(df_database)
    print("Checked database successfully.")

    # Englist_Version = isOutputEnglish(df_transcript)
    # TODO: data validation

    # Data preparation
    df_database, df_transcript = DataPreparation(df_database, df_transcript)

    sorted_courses = []
    transcript_sorted_group_map = {}

    if analysis_language == 'en':
        transcript_sorted_group_map = basic_classification_en
    elif analysis_language == 'zh':  # Traditional Chinese
        transcript_sorted_group_map = basic_classification_zh
    else:
        transcript_sorted_group_map = basic_classification_zh

    category_data = []
    df_category_data = []
    category_courses_sugesstion_data = []
    df_category_courses_sugesstion_data = []
    for idx, cat in enumerate(transcript_sorted_group_map):
        categoryName = transcript_sorted_group_map[cat][CATEGORY_NAME]
        category_data = {cat: [], 'courses': [], 'credits': [], 'grades': []}
        df_category_data.append(pd.DataFrame(data=category_data))
        df_category_courses_sugesstion_data.append(
            pd.DataFrame(data=category_courses_sugesstion_data, columns=['建議修課']))

    if analysis_language in ['en', None]:
        # 基本分類課程 (與申請學程無關)
        df_category_data = CourseSorting(
            df_transcript, df_category_data, transcript_sorted_group_map, "course_english")
        # 基本分類電機課程資料庫
        df_category_courses_sugesstion_data = DatabaseCourseSorting(
            df_database, df_category_courses_sugesstion_data, transcript_sorted_group_map, "all_course_english")
    else:
        # 基本分類課程 (與申請學程無關)
        df_category_data = CourseSorting(
            df_transcript, df_category_data, transcript_sorted_group_map, "course_chinese")
        # 基本分類電機課程資料庫
        df_category_courses_sugesstion_data = DatabaseCourseSorting(
            df_database, df_category_courses_sugesstion_data, transcript_sorted_group_map, "all_course_chinese")

    for idx, cat in enumerate(df_category_data):
        df_category_courses_sugesstion_data[idx]['建議修課'] = df_category_courses_sugesstion_data[idx]['建議修課'].str.replace(
            '(', '', regex=False)
        df_category_courses_sugesstion_data[idx]['建議修課'] = df_category_courses_sugesstion_data[idx]['建議修課'].str.replace(
            ')', '', regex=False)

    # 樹狀篩選 微積分:[一,二] 同時有含 微積分、一  的，就從recommendation拿掉
    # algorithm :
    df_category_courses_sugesstion_data = SuggestionCourseAlgorithm(
        df_category_data, transcript_sorted_group_map, df_category_courses_sugesstion_data)

    sorted_courses = df_category_data

    json_output = {'General': {},
                   'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat()}

    for idx, sortedcourses in enumerate(sorted_courses):
        if sortedcourses.empty:
            # print(f"Skipping empty DataFrame at index {idx}")
            continue  # Skip to the next DataFrame if empty

        # Adjust key length if needed
        records = json.loads(sortedcourses.to_json(
            orient='records', indent=4))
        id_key = next(
            (key for key in records[0] if len(key) == 24), None)
        # Write to JSON
        json_output['General'][id_key] = json.loads(
            sortedcourses.to_json(orient='records', indent=4)
        )

    programs = get_programs_analysis_collection(
        requirement_ids_arr)
    print('programs', programs)

    # Create
    for idx, program in enumerate(programs):
        createSheet(
            transcript_sorted_group_map,
            sorted_courses,
            df_category_courses_sugesstion_data,
            json_output, program,
            factor)

    # Save JSON data
    json_output['factor'] = factor
    print('json_output: ', json_output)

    json_buffer = io.BytesIO()
    json_data = json.dumps(
        json_output, ensure_ascii=False, default=custom_json_serializer).encode('utf-8')
    json_buffer.write(json_data)
    json_buffer.seek(0)

    AWS_S3_BUCKET_NAME = os.environ.get("AWS_S3_BUCKET_NAME")
    print(AWS_S3_BUCKET_NAME)
    try:
        transcript_json_path = studentId + '/analysed_transcript_' + student_name + '.json'
        print('transcript_json_path: ', transcript_json_path)

        return json.dumps({
            'transcript_json_path': transcript_json_path, 'result': json_output})
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': e})
        }


def convertingKeywordsSetArrayToObject(program_categories):
    # Initialize an empty dictionary to store the results
    baseCategoryToProgramMapping = {}

    # Iterate over each program category
    for program in program_categories:
        category = program['program_category']
        ects = program['requiredECTS']

        # Iterate over each keyword in the keywordSets
        for keyword in program['keywordSets']:
            # Add the keyword to the dictionary with its corresponding program category and ECTS
            # print('keyword: ', keyword)
            #  TODO: check if keyword is id or ObjectId
            baseCategoryToProgramMapping[keyword] = {
                'program_category': category,
                'requiredECTS': ects
            }
    return baseCategoryToProgramMapping


def createSheet(transcript_sorted_group_map, df_transcript_array, df_category_courses_sugesstion_data, json_output, program, factor):
    # TODO: schema not matched to db.
    the_program = program['programId'][0]
    program_name = ' '.join(
        [the_program['school'], the_program['program_name'], the_program['degree']])

    program_name_long = ' '.join(
        [the_program['school'], the_program['program_name'], the_program['degree']])

    # Limit to 30 characters as limitation of sheet name
    if len(program_name) > 30:
        program_name = program_name[:27] + '...'  # Add ellipsis if truncated
    print("Create sheet for", program_name)
    df_transcript_array_temp = []
    df_category_courses_sugesstion_data_temp = []
    for idx, df in enumerate(df_transcript_array):
        df_transcript_array_temp.append(df.copy())
    for idx, df in enumerate(df_category_courses_sugesstion_data):
        df_category_courses_sugesstion_data_temp.append(df.copy())
    #####################################################################
    ############## Program Specific Parameters ##########################
    #####################################################################

    # This fixed to program course category.
    program_categories = program['program_categories']

    # all keywords that the program has
    all_keywords = [
        keyword for program in program_categories for keyword in program['keywordSets']]

    # Main array
    transcript_sorted_group_list = list(transcript_sorted_group_map)

    # Convert to set and use difference
    transcript_sorted_group_list_others = list(set(transcript_sorted_group_list) -
                                               set(all_keywords))

    program_categories.append({
        'program_category': 'Others', 'requiredECTS': 0,
        "keywordSets": transcript_sorted_group_list_others}  # 其他
    )

    # Iterate over each program category
    baseCategoryToProgramMapping = convertingKeywordsSetArrayToObject(
        program_categories)

    #####################################################################
    ####################### End #########################################
    #####################################################################

    WriteToExcel(json_output, program_name, program_name_long, program_categories, baseCategoryToProgramMapping,
                 transcript_sorted_group_map, df_transcript_array_temp, df_category_courses_sugesstion_data_temp, program, factor)


def custom_json_serializer(obj):
    if isinstance(obj, ObjectId):
        return str(obj)  # Convert ObjectId to string
    elif isinstance(obj, datetime.datetime):
        return obj.isoformat()  # Convert datetime to ISO 8601 string
    raise TypeError(f"Type {type(obj)} not serializable")
