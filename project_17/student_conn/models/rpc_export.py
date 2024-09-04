import xmlrpc.client

source_url = 'http://localhost:4987'
source_db = 'my_data_ct'
source_username = 'admin'
source_password = 'admin'

source_common = xmlrpc.client.ServerProxy(f'{source_url}/xmlrpc/2/common')
try:
    source_uid = source_common.authenticate(source_db, source_username, source_password, {})
    if not source_uid:
        print("Failed to authenticate.")
    else:
        print(f" <<<<<<<<UID: {source_uid}")
except Exception as e:
    print(f"Error: {e}")

target_url = 'http://localhost:8855'
target_db = 'my_data_odoo3'
target_username = 'admin'
target_password = 'admin'


source_common= xmlrpc.client.ServerProxy(f'{source_url}/xmlrpc/2/common')
source_models= xmlrpc.client.ServerProxy(f'{source_url}/xmlrpc/2/object')

target_common = xmlrpc.client.ServerProxy(f'{target_url}/xmlrpc/2/common')
target_models = xmlrpc.client.ServerProxy(f'{target_url}/xmlrpc/2/object')


source_uid = source_common.authenticate(source_db, source_username, source_password, {})
if not source_uid:
    print("<<<<<Failed")
    exit()


target_uid = target_common.authenticate(target_db, target_username, target_password, {})
if not target_uid:
    print("<<<<<<<Failed")
    exit()

print(f"<<<<<< UId: {source_uid}")



    #school data Read and createeeeeeeeeee
try:
    
    school_data = source_models.execute_kw(
        source_db, source_uid, source_password,
        'wb.school', 'search_read',
        [[['id', '!=', False]]],
        {'fields': ['name', 'School_type']}
    )

    
    new_schoolid_student = {}


    for school in school_data:
        new_school_id = target_models.execute_kw(
            target_db, target_uid, target_password,
            'wb.school', 'create',
            [school]
        )
        new_schoolid_student[school['id']] = new_school_id
        print("New ID")



    #student data read and createe

    student_data = source_models.execute_kw(
        source_db, source_uid, source_password,
        'wb.student', 'search_read',
        [[['id', '!=', False]]],
        {'fields': ['name', 'email', 'is_enrolled', 'School_type', 'roll_number', 'newfield1', 'newfield2',
                    'fatherjobtype', 'dob', 'status', 'habit', 'height', 'enroll_date', 'join_datetime', 'school_id']}
    )
    print("Fetched student data:", student_data)


    for student in student_data:
        if student['school_id']:
            new_school_id = new_schoolid_student.get(student['school_id'][0])
            if new_school_id:
                student['school_id'] = new_school_id
            else:
                print("School id not found")

       
        try:
            new_student_id = target_models.execute_kw(
                target_db, target_uid, target_password,
                'wb.student', 'create',
                [student]
            )
            print("create student with new ID:", new_student_id)
        except Exception as e:
            print(f"Error creating student<<<<: {e}")

    

#course  Data read and create

    course_data = source_models.execute_kw(
        source_db, source_uid, source_password,
        'wb.course', 'search_read',
        [[['id', '!=', False]]],
        {'fields': ['name']}
    )

    for course in course_data:
        try:
            new_course_id = target_models.execute_kw(
                target_db, target_uid, target_password,
                'wb.course', 'create',
                [course]
            )
        except Exception as w:
            print(f"Error creating course: {w}")

except Exception as e:
    print(f"Error: {e}")
