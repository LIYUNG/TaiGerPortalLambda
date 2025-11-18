import os
import boto3
from botocore.exceptions import ClientError
from pymongo import MongoClient
from bson import ObjectId

# Global variables to store the MongoDB client and database connection
secret_name = os.environ.get("MONGODB_URI_SECRET_NAME")
region_name = os.environ.get("REGION")

# Create a Secrets Manager client
session = boto3.session.Session()
client = session.client(
    service_name='secretsmanager',
    region_name=region_name
)
try:
    get_secret_value_response = client.get_secret_value(
        SecretId=secret_name
    )
except ClientError as e:
    # For a list of exceptions thrown, see
    # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    raise e

secret = get_secret_value_response['SecretString']
MONGODB_URI = secret
MONGODB_NAME = os.environ.get("MONGODB_NAME")
mongo_uri = MONGODB_URI
db_name = MONGODB_NAME
mongo_client = mongo_client = MongoClient(
    mongo_uri, readPreference='primary', readConcernLevel='majority')
try:
    mongo_client.admin.command('ping')
    print("Successfully connected to MongoDB!")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    raise e
db = mongo_client[db_name]


def get_requirements_collection(requirement_ids_list=None):
    # Use the database connection to perform operations
    collection = db['programrequirements']

    # Convert string IDs to ObjectId, skipping invalid ones
    if requirement_ids_list:
        try:
            requirement_ids_list = [ObjectId(id)
                                    for id in requirement_ids_list]
            print('requirement_ids_list: ', requirement_ids_list)
        except Exception as e:
            print(f"Error converting requirement_ids_list to ObjectId: {e}")
            requirement_ids_list = []

    # Aggregation pipeline to fetch documents and "populate" the programId field
    pipeline = [
        {
            '$match': {
                '_id': {'$in': [ObjectId(id) for id in requirement_ids_list]}
            }
        },
        {
            '$lookup': {
                'from': 'programs',             # Collection to join with
                'localField': 'programId',
                'foreignField': '_id',          # Field in 'programs' to match with
                'as': 'programId'               # Output array field name for joined data
            }
        },
        {
            '$addFields': {
                'programId': {
                    '$map': {
                        'input': '$programId',
                        'as': 'program',
                        'in': {
                            '_id': '$$program._id',
                            'school': '$$program.school',
                            'program_name': '$$program.program_name',
                            'degree': '$$program.degree'
                        }
                    }
                }
            }
        }
    ]

    # Fetch documents based on the query
    documents = list(collection.aggregate(pipeline))

    return documents


def get_all_courses_db_collection():
    # Use the database connection to perform operations
    collection = db['allcourses']

    query = {}

    # Fetch documents based on the query
    documents = list(collection.find(query))

    return documents


def get_keywords_collection():
    # Use the database connection to perform operations
    collection = db['keywordsets']

    # Example: Fetch all documents from the collection
    documents = list(collection.find({}).sort("categoryName", 1))
    print('keyword collection: ', documents)
    # Preprocess data to convert to desired structure
    processed_data = {
        item['_id']: {
            'categoryName': item['categoryName'],
            'keywords': item['keywords'],
            'antiKeywords': item['antiKeywords']
        }
        for item in documents
    }

    return processed_data


def get_programs_analysis_collection(requirement_ids_arr):

    # Example: Fetch all documents from the collection
    documents = get_requirements_collection(requirement_ids_arr)
    print('requiremnts: ', documents)
    return documents


def generate_classification(lang, subjects, processed_data):
    """Helper function to dynamically generate classification dict for 'zh' and 'en'."""
    return {
        subject_name: [
            processed_data[category]['keywords'][lang],
            processed_data[category]['antiKeywords'][lang],
            extras
        ]
        for subject_name, (category, extras) in subjects.items()
    }


def convert_courses(course_dict, lang):
    result = {}

    # Loop through each course in the dictionary
    for course_name, course_details in course_dict.items():
        # Extract the relevant details
        categoryName = course_details.get('categoryName', '')
        keywords = course_details.get('keywords', {}).get(lang, [])
        anti_keywords = course_details.get('antiKeywords', {}).get(lang, [])

        # Add the additional ['一', '二'] list
        additional_list = ['一', '二']

        # Store the course data in the desired format
        result[course_name] = [keywords, anti_keywords,
                               additional_list, categoryName]

    return result
