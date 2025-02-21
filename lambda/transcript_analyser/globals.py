
# Global variable:

programs_mock = [
    {
        "program_name": "TUM_EI",
        "program_categories": [
            {
                'program_category': 'Mathematics',
                'requiredECTS': 28,
                "keywordSets": ['CALCULUS', 'ME_MATH', 'MATH_PROB', 'MATH_LINEAR_ALGEBRA', 'DIFF_EQUATION', 'MATH_DISCRETE', 'MATH_NUM_METHOD']},  # TODO: it is object
            {
                'program_category': 'Physics',
                'requiredECTS': 10,
                "keywordSets": ['GENERAL_PHYSICS', 'EE_ADVANCED_PHYSICS', 'PHYSICS_EXP']},
            {
                'program_category': 'Programming and Computer science',
                'requiredECTS': 12,
                "keywordSets": ['FUNDAMENTAL_COMPUTER_SCIENCE', 'EE_INTRO_COMPUTER_SCIENCE', 'PROGRAMMING_LANGUAGE', 'SOFTWARE_ENGINEERING']},
            {
                'program_category': 'System_Theory',
                'requiredECTS': 8,
                "keywordSets": ['CONTROL_THEORY']},
            {
                'program_category': 'Electronics and Circuits Module',
                'requiredECTS': 34,
                "keywordSets": ['FUNDAMENTAL_ELECTRICAL_ENGINEERING', 'ELECTRONICS', 'ELECTRONICS_EXPERIMENT', 'ELECTRO_CIRCUIT', 'SIGNAL_SYSTEM', 'ELECTRO_MAGNET', 'ELECTRO_CIRCUIT_DESIGN']},
            {
                'program_category': 'Theoretical_Module_EECS',
                'requiredECTS': 8,
                "keywordSets": ['EE_HF_RF_THEO_INFO']},
            {
                'program_category': 'Application_Module_EECS',
                'requiredECTS': 20,
                "keywordSets": ['POWER_ELECTRONICS', 'COMMUNICATION_ENGINEERING', 'EE_ADVANCED_ELECTRO', 'EE_APPLICATION_ORIENTED']}
        ]
    }, {
        "program_name": "RWTH_EI",
        "program_categories": [
            {
                'program_category': 'Mathematics',
                'requiredECTS': 28,
                "keywordSets": ['CALCULUS', 'ME_MATH', 'MATH_PROB', 'MATH_LINEAR_ALGEBRA', 'DIFF_EQUATION', 'MATH_DISCRETE', 'MATH_NUM_METHOD']},
            {
                'program_category': 'Physics',
                'requiredECTS': 10,
                "keywordSets": ['GENERAL_PHYSICS', 'EE_ADVANCED_PHYSICS', 'PHYSICS_EXP']},
            {
                'program_category': 'Programming and Computer science',
                'requiredECTS': 12,
                "keywordSets": ['FUNDAMENTAL_COMPUTER_SCIENCE', 'EE_INTRO_COMPUTER_SCIENCE', 'PROGRAMMING_LANGUAGE', 'SOFTWARE_ENGINEERING']},
            {
                'program_category': 'System_Theory',
                'requiredECTS': 8,
                "keywordSets": ['CONTROL_THEORY']},
            {
                'program_category': 'Electronics and Circuits Module',
                'requiredECTS': 34,
                "keywordSets": ['FUNDAMENTAL_ELECTRICAL_ENGINEERING', 'ELECTRONICS', 'ELECTRONICS_EXPERIMENT', 'ELECTRO_CIRCUIT', 'SIGNAL_SYSTEM', 'ELECTRO_MAGNET', 'ELECTRO_CIRCUIT_DESIGN']},
            {
                'program_category': 'Theoretical_Module_EECS',
                'requiredECTS': 8,
                "keywordSets": ['EE_HF_RF_THEO_INFO']},
            {
                'program_category': 'Application_Module_EECS',
                'requiredECTS': 20,
                "keywordSets": ['POWER_ELECTRONICS', 'COMMUNICATION_ENGINEERING', 'EE_ADVANCED_ELECTRO', 'EE_APPLICATION_ORIENTED']}
        ]
    }, {
        "program_name": "STUTTGART_EI",
        "program_categories": [
            {
                'program_category': 'Mathematics',
                'requiredECTS': 24,
                "keywordSets": ['CALCULUS', 'ME_MATH', 'MATH_PROB', 'MATH_LINEAR_ALGEBRA', 'DIFF_EQUATION', 'MATH_DISCRETE', 'MATH_NUM_METHOD']},
            {
                'program_category': 'Physics Experiment',
                'requiredECTS': 6,
                "keywordSets": ['GENERAL_PHYSICS', 'PHYSICS_EXP']},
            {
                'program_category': 'Microelectronics',
                'requiredECTS': 9,
                "keywordSets": ['FUNDAMENTAL_ELECTRICAL_ENGINEERING', 'ELECTRONICS']},
            {
                'program_category': 'Intro. Electrical Engineering and project',
                'requiredECTS': 9,
                "keywordSets": ['ELECTRONICS_EXPERIMENT']},
            {
                'program_category': 'Intro. Programming and project',
                'requiredECTS': 6,
                "keywordSets": ['PROGRAMMING_LANGUAGE']},
            {
                'program_category': 'Intro. Software System',
                'requiredECTS': 3,
                "keywordSets": ['SOFTWARE_ENGINEERING']},
            {
                'program_category': 'Energy Technique',
                'requiredECTS': 9,
                "keywordSets": ['POWER_ELECTRONICS']},
            {
                'program_category': 'Circuits Technology',
                'requiredECTS': 9,
                "keywordSets": ['ELECTRO_CIRCUIT', 'ELECTRO_CIRCUIT_DESIGN']},
            {
                'program_category': 'Electromagnetics',
                'requiredECTS': 9,
                "keywordSets": ['ELECTRO_MAGNET', 'EE_HF_RF_THEO_INFO']},
            {
                'program_category': 'Communication Engineering',
                'requiredECTS': 9,
                "keywordSets": ['COMMUNICATION_ENGINEERING']},
            {
                'program_category': 'Intro. Information processing',
                'requiredECTS': 6,
                "keywordSets": ['EE_INTRO_COMPUTER_SCIENCE']},
            {
                'program_category': 'Signals and Systems',
                'requiredECTS': 6,
                "keywordSets": ['SIGNAL_SYSTEM']},
            {
                'program_category': 'Advanced Modules',
                'requiredECTS': 6,
                "keywordSets": ['CONTROL_THEORY', 'SEMICONDUCTOR', 'EE_ADVANCED_ELECTRO', 'EE_APPLICATION_ORIENTED']}
        ]
    }, {
        "program_name": "TUM_MSCE",
        "program_categories": [
            {
                'program_category': 'Higher Mathematics',
                'requiredECTS': 30,
                "keywordSets": ['CALCULUS', 'ME_MATH', 'MATH_PROB', 'MATH_LINEAR_ALGEBRA', 'DIFF_EQUATION', 'MATH_DISCRETE', 'MATH_NUM_METHOD']},
            {
                'program_category': 'Fundamental Electrical Engineering',
                'requiredECTS': 66,
                "keywordSets": ['FUNDAMENTAL_ELECTRICAL_ENGINEERING', 'EE_INTRO_COMPUTER_SCIENCE', 'PROGRAMMING_LANGUAGE', 'ELECTRONICS', 'ELECTRONICS_EXPERIMENT', 'ELECTRO_CIRCUIT', 'SIGNAL_SYSTEM', 'ELECTRO_MAGNET', 'POWER_ELECTRONICS', 'SEMICONDUCTOR', 'ELECTRO_CIRCUIT_DESIGN']},
            {
                'program_category': 'Fundamental Communication',
                'requiredECTS': 30,
                "keywordSets": ['COMMUNICATION_ENGINEERING', 'EE_HF_RF_THEO_INFO', 'EE_ADVANCED_ELECTRO', 'COMPUTER_NETWORK']}
        ]
    }, {
        "program_name": "TUM_MSPE",
        "program_categories": [
            {
                'program_category': 'Higher Mathematics',
                'requiredECTS': 30,
                "keywordSets": ['CALCULUS', 'ME_MATH', 'MATH_PROB', 'MATH_LINEAR_ALGEBRA', 'DIFF_EQUATION', 'MATH_DISCRETE', 'MATH_NUM_METHOD']},
            {
                'program_category': 'Fundamental Electrical Engineering',
                'requiredECTS': 45,
                "keywordSets": ['FUNDAMENTAL_ELECTRICAL_ENGINEERING', 'EE_INTRO_COMPUTER_SCIENCE', 'PROGRAMMING_LANGUAGE', 'ELECTRONICS', 'ELECTRONICS_EXPERIMENT', 'ELECTRO_CIRCUIT', 'SIGNAL_SYSTEM', 'ELECTRO_MAGNET', 'POWER_ELECTRONICS', 'SEMICONDUCTOR', 'ELECTRO_CIRCUIT_DESIGN']},
            {
                'program_category': 'Fundamental Mechanics',
                'requiredECTS': 45,
                "keywordSets": ['EE_MACHINE']}
        ]
    }, {
        "program_name": "TUM_MSNE",
        "program_categories": [
            {
                'program_category': 'Higher Mathematics',
                'requiredECTS': 32,
                "keywordSets": ['CALCULUS', 'ME_MATH', 'MATH_PROB', 'MATH_LINEAR_ALGEBRA', 'DIFF_EQUATION', 'MATH_DISCRETE', 'MATH_NUM_METHOD']},
            {
                'program_category': 'Natural Science (Physics, Biochem., neuroscience',
                'requiredECTS': 45,
                "keywordSets": ['GENERAL_PHYSICS', 'EE_ADVANCED_PHYSICS', 'PHYSICS_EXP']},
            {
                'program_category': 'Bio and medical engineering',
                'requiredECTS': 40,
                "keywordSets": []}
        ]
    }, {
        "program_name": "TUHH_MICROELECTRONICS",
        "program_categories": [
            {
                'program_category': 'Mathematics',
                'requiredECTS': 30,
                "keywordSets": ['CALCULUS', 'ME_MATH', 'MATH_PROB', 'MATH_LINEAR_ALGEBRA', 'DIFF_EQUATION', 'MATH_DISCRETE', 'MATH_NUM_METHOD']},
            {
                'program_category': 'Computer Science',
                'requiredECTS': 18,
                "keywordSets": ['FUNDAMENTAL_COMPUTER_SCIENCE', 'EE_INTRO_COMPUTER_SCIENCE', 'PROGRAMMING_LANGUAGE', 'SOFTWARE_ENGINEERING']},
            {
                'program_category': 'Control Theory',
                'requiredECTS': 6,
                "keywordSets": ['CONTROL_THEORY']},
            {
                'program_category': 'Physics',
                'requiredECTS': 6,
                "keywordSets": ['GENERAL_PHYSICS', 'EE_ADVANCED_PHYSICS', 'PHYSICS_EXP']},
            {
                'program_category': 'Fundamental Electrical Engineering',
                'requiredECTS': 12,
                "keywordSets": ['FUNDAMENTAL_ELECTRICAL_ENGINEERING', 'EE_INTRO_COMPUTER_SCIENCE', 'PROGRAMMING_LANGUAGE', 'ELECTRONICS', 'ELECTRONICS_EXPERIMENT', 'POWER_ELECTRONICS', 'SEMICONDUCTOR']},
            {
                'program_category': 'Materials in Electrical Engineering',
                'requiredECTS': 3,
                "keywordSets": ['ELECTRICAL_MATERIALS']},
            {
                'program_category': 'Measurements: Methods and data processing',
                'requiredECTS': 3,
                "keywordSets": ['ELECTRONICS_EXPERIMENT']},
            {
                'program_category': 'Circuit theory',
                'requiredECTS': 6,
                "keywordSets": ['ELECTRO_CIRCUIT', 'ELECTRO_CIRCUIT_DESIGN']},
            {
                'program_category': 'Transmission Line',
                'requiredECTS': 6,
                "keywordSets": ['EE_ADVANCED_ELECTRO']},
            {
                'program_category': 'Signals and systems',
                'requiredECTS': 6,
                "keywordSets": ['SIGNAL_SYSTEM']},
            {
                'program_category': 'Theoretical Electrical Engineering',
                'requiredECTS': 12,
                "keywordSets": ['ELECTRO_MAGNET']},
            {
                'program_category': 'Semiconductor and electronics devices',
                'requiredECTS': 6,
                "keywordSets": ['SEMICONDUCTOR']},
        ]
    }, {
        "program_name": "FAU_INFO_COMM_TECH",
        "program_categories": [
            {
                'program_category': 'Higher Mathematics',
                'requiredECTS': 30,
                "keywordSets": ['CALCULUS', 'ME_MATH', 'MATH_PROB', 'MATH_LINEAR_ALGEBRA', 'DIFF_EQUATION', 'MATH_DISCRETE', 'MATH_NUM_METHOD']},
            {
                'program_category': 'Computer Science',
                'requiredECTS': 30,
                "keywordSets": ['FUNDAMENTAL_COMPUTER_SCIENCE', 'EE_INTRO_COMPUTER_SCIENCE', 'PROGRAMMING_LANGUAGE', 'SOFTWARE_ENGINEERING']},
            {
                'program_category': 'Communications Engineering',
                'requiredECTS': 30,
                "keywordSets": ['COMMUNICATION_ENGINEERING', 'SIGNAL_SYSTEM', 'EE_HF_RF_THEO_INFO', 'EE_ADVANCED_ELECTRO']},
            {
                'program_category': 'Electrical Engineering',
                'requiredECTS': 30,
                "keywordSets": ['FUNDAMENTAL_ELECTRICAL_ENGINEERING', 'EE_INTRO_COMPUTER_SCIENCE', 'PROGRAMMING_LANGUAGE', 'ELECTRONICS', 'ELECTRONICS_EXPERIMENT', 'ELECTRO_CIRCUIT', 'ELECTRO_MAGNET', 'POWER_ELECTRONICS', 'SEMICONDUCTOR', 'ELECTRO_CIRCUIT_DESIGN']},
        ]
    }, {
        "program_name": "TUM_ASIA_IC_DESIGN",
        "program_categories": [
            {
                'program_category': 'Higher Mathematics',
                'requiredECTS': 24,
                "keywordSets": ['CALCULUS', 'ME_MATH', 'MATH_PROB', 'MATH_LINEAR_ALGEBRA', 'DIFF_EQUATION', 'MATH_DISCRETE', 'MATH_NUM_METHOD']},
            {
                'program_category': 'Fundamental Electrical Engineering',
                'requiredECTS': 66,
                "keywordSets": ['FUNDAMENTAL_ELECTRICAL_ENGINEERING', 'EE_INTRO_COMPUTER_SCIENCE', 'PROGRAMMING_LANGUAGE', 'ELECTRONICS', 'ELECTRONICS_EXPERIMENT', 'SIGNAL_SYSTEM', 'ELECTRO_MAGNET', 'POWER_ELECTRONICS', 'SEMICONDUCTOR']},
            {
                'program_category': 'Communications Engineering',
                'requiredECTS': 30,
                "keywordSets": ['ELECTRO_CIRCUIT', 'ELECTRO_CIRCUIT_DESIGN', 'COMPUTER_NETWORK']},
        ]
    }, {
        "program_name": "KIT_EI",
        "program_categories": [
            {
                'program_category': 'Higher Mathematics',
                'requiredECTS': 42,
                "keywordSets": ['CALCULUS', 'ME_MATH', 'MATH_PROB', 'MATH_LINEAR_ALGEBRA', 'DIFF_EQUATION', 'MATH_DISCRETE', 'MATH_NUM_METHOD']},
            {
                'program_category': 'Fundamental Electrical Engineering',
                'requiredECTS': 28,
                "keywordSets": ['FUNDAMENTAL_ELECTRICAL_ENGINEERING', 'ELECTRONICS', 'ELECTRONICS_EXPERIMENT', 'ELECTRO_MAGNET', 'POWER_ELECTRONICS', 'SEMICONDUCTOR']},
            {
                'program_category': 'System Engineering',
                'requiredECTS': 14,
                "keywordSets": ['CONTROL_THEORY', 'SIGNAL_SYSTEM']},
            {
                'program_category': 'Information technology',
                'requiredECTS': 19,
                "keywordSets": ['EE_INTRO_COMPUTER_SCIENCE', 'PROGRAMMING_LANGUAGE', 'COMMUNICATION_ENGINEERING'],
                "fpso": "https://www.etit.kit.edu/rd_download/MHB/MHB_BSc23_ETIT_WS23-82-048-H-2023_v1_2023-10-20_de.pdf"},

        ]
    }]
