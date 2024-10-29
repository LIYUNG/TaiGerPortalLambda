import os
import boto3
from botocore.exceptions import ClientError
from pymongo import MongoClient
from bson import ObjectId

from globals import programs_mock

# Global variables to store the MongoDB client and database connection
mongo_client = None
db = None

# Initialize the Secrets Manager client
secrets_manager = boto3.client('secretsmanager')


# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/


def get_secret_aws_example():

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

    return secret


def get_database():
    global mongo_client
    global db

    if db is None:
        MONGODB_URI = get_secret_aws_example()
        MONGODB_NAME = os.environ.get("MONGODB_NAME")
        mongo_uri = MONGODB_URI
        db_name = MONGODB_NAME

        # Create a new client and connect to the server
        mongo_client = MongoClient(mongo_uri)

        # Send a ping to confirm a successful connection
        try:
            mongo_client.admin.command('ping')
            print("Successfully connected to MongoDB!")
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")
            raise e

        # Get the database
        db = mongo_client[db_name]

    return db


def get_requirements_collection(requirement_ids_list=None):
    # Get the database connection
    database = get_database()

    # Use the database connection to perform operations
    collection = database['programrequirements']

    # Convert string IDs to ObjectId, skipping invalid ones
    if requirement_ids_list:
        try:
            requirement_ids_list = [ObjectId(id)
                                    for id in requirement_ids_list]
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
                # Field in 'programrequirements' that references 'programs'
                'localField': 'programId',
                'foreignField': '_id',          # Field in 'programs' to match with
                'as': 'programId'               # Output array field name for joined data
            }
        },
        {
            '$project': {
                # Include specific fields from 'programrequirements' and 'programId'
                **{field: 1 for field in collection.find_one({}).keys()},
                'programId': {
                    '$map': {
                        'input': '$programId',
                        'as': 'program',
                        'in': {
                            '_id': '$$program._id',  # Include the program ID
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
    # Get the database connection
    database = get_database()

    # Use the database connection to perform operations
    collection = database['allcourses']

    query = {}

    # Fetch documents based on the query
    documents = list(collection.find(query))

    return documents


def get_keywords_collection():
    # Get the database connection
    database = get_database()

    # Use the database connection to perform operations
    collection = database['keywordsets']

    # Example: Fetch all documents from the collection
    documents = list(collection.find({}))
    print('keyword collection: ', documents)
    # Preprocess data to convert to desired structure
    processed_data = {
        item['_id']: {
            'keywords': item['keywords'],
            'antiKeywords': item['antiKeywords']
        }
        for item in documents
    }

    return processed_data


def get_programs_analysis_collection():
    # Get the database connection
    database = get_database()

    # Use the database connection to perform operations
    collection = database['programanalyse']

    # Example: Fetch all documents from the collection
    documents = list(collection.find({}))

    return documents


def get_programs_analysis_collection_mock(requirement_ids_arr):
    # # Get the database connection
    # database = get_database()

    # # Use the database connection to perform operations
    # collection = database['programanalyse']

    # Example: Fetch all documents from the collection
    # documents = programs_mock
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
        keywords = course_details.get('keywords', {}).get(lang, [])
        anti_keywords = course_details.get('antiKeywords', {}).get(lang, [])

        # Add the additional ['一', '二'] list
        additional_list = ['一', '二']

        # Store the course data in the desired format
        result[course_name] = [keywords, anti_keywords, additional_list]

    return result
