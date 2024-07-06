import math
import random
from django.conf import settings
from django.db import connection
from django.http import JsonResponse
from django.shortcuts import redirect, render
from guest.models import *
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from guest.serializers import *
from django.core.serializers import serialize
from datetime import datetime , timedelta
from django.core.mail import send_mail


# Create your views here.
@csrf_exempt
def students(request,id=0):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        contact = request.POST.get('contact')
        district = request.POST.get('district')
        state = request.POST.get('state')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        course = request.POST.get('course')
        subject = request.POST.get('subject')
        
        username =request.POST.get('username')
        password = request.POST.get('password')
        dates = date.today()
        
        loginlist = login()
        loginlist.username = username
        loginlist.password = password
        loginlist.role = "STUDENT"
        loginlist.status = "NON-ACTIVE"
        loginlist.save()
        
        last_inserted_id = loginlist.loginid
        
        studentslist = Students()
        studentslist.student_firstname = firstname
        studentslist.student_lastname = lastname
        studentslist.email = email
        studentslist.contactno = contact
        studentslist.district = district  
        studentslist.dob = dob
        studentslist.state = state
        studentslist.address = address
        studentslist.pincode = pincode
        studentslist.course = course
        studentslist.subject = subject
        studentslist.loginid = last_inserted_id
        studentslist.date = dates
        datenow = datetime.now().date()
        timenow = datetime.now().time()
        studentslist.login_date = datenow
        studentslist.login_time = timenow
        studentslist.fees_status = "NOT PAID"
        studentslist.save()
        studentid = studentslist.studentid
        
        
        return JsonResponse({"success":True,"studentid":studentid})
    
    elif request.method == "GET":
        sql_query = "SELECT * FROM guest_students s INNER JOIN guest_login l ON s.loginid = l.loginid INNER JOIN guest_districts d ON s.district = d.districtid INNER JOIN guest_states g ON s.state = g.stateid INNER JOIN guest_courses c ON s.course = c.courseid INNER JOIN guest_subjects u ON s.subject = u.subjectid"
        result = login.objects.raw(sql_query)
        
        data = [
            {
                'status':data.status,
                'username':data.username,
                'student_firstname':data.student_firstname,
                'student_lastname':data.student_lastname,
                'loginid':data.loginid,
                'email':data.email,
                'contactno':data.contactno,
                'district':data.districtname,
                'state':data.statename,
                'address':data.address,
                'pincode':data.pincode,
                'studentid':data.studentid,
                'subject':data.subjectname,
                'date':data.date,
                'course':data.coursename,
                'dob':data.dob
            }   
            for data in result
        ]
        
        return JsonResponse(data,safe=False)
    
    elif request.method == "DELETE":
        studentslist = Students.objects.get(studentid = id)
        studentslist.delete()
        return JsonResponse({"success":True})
        


@csrf_exempt
def logins(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        loginlist = login.objects.filter(username=username , password=password , role="STUDENT" , status = "ACTIVE")
        adminlist = login.objects.filter(username=username , password = password , role="ADMIN" , status = "ACTIVE")
        stafflist = login.objects.filter(username=username , password=password , role = "STAFF" , status = "ACTIVE")
        loginlist1 = login.objects.filter(username=username , password=password , role="STUDENT" , status = "NON-ACTIVE")
        
        
        
        if loginlist.exists():
            request.session['username'] = username
            list = login.objects.filter(username=username)
            data = [
                {
                    'loginid':data.loginid
                }
                for data in list
            ]
            
            
            loginid = data[0]['loginid']
            request.session['loginid'] = loginid
            
            studentfunction = Students.objects.get(loginid=loginid)
            studentfunction.student_status = "active"
            logindate = date.today()
            logintime = datetime.today()
            login_time_formatted = logintime.strftime('%H:%M')
            studentfunction.login_date = logindate
            studentfunction.login_time = login_time_formatted
            studentfunction.save()
            
            studentlist = Students.objects.filter(loginid=loginid)
            serialize = StudentSerializer(studentlist,many=True)
            studentlist = serialize.data[0]
            return JsonResponse({"success":True,"loginid":loginid})
        
        elif adminlist.exists():
            request.session['username'] = username
            
            return JsonResponse({"admin":True,"username":username})
        
        elif loginlist1.exists():
            return JsonResponse({"active":True})
        
        elif stafflist.exists():
            request.session['username'] = username
            list = login.objects.filter(username=username)
            data = [
                {
                    'loginid':data.loginid
                }
                for data in list
            ]
            
            
            loginid = data[0]['loginid']
            request.session['loginid'] = loginid
            
            sql_query = "SELECT * FROM `guest_login` l INNER JOIN `guest_staff` s ON l.loginid = s.loginid WHERE l.loginid = %s"
            result = login.objects.raw(sql_query,[loginid])
            resultdata = [
                {
                    'staffid':item.staffid
                }
                for item in result
            ]
            
            staffid = resultdata[0]['staffid']
            
            return JsonResponse({"staff":True,"loginid":loginid,"staffid":staffid})
        
        else:
            return JsonResponse({"success":False})
        
@csrf_exempt
def state(request):
    if request.method == "POST":
        name = request.POST.get('statename')
        
        statelist = states()
        
        statelist.statename = name
        statelist.save()
        
        return JsonResponse({"success":True})
    
    elif request.method == "GET":
        statelist = states.objects.all()
        serializer  = StateSerializer(statelist,many=True)
        return JsonResponse(serializer.data,safe=False)
        
    
@csrf_exempt
def district(request,id=0):
    if request.method == "POST":
        stateid = request.POST.get('stateid')
        districtname = request.POST.get('districtname') 
        
        districtlist = districts()
        districtlist.stateid = stateid
        districtlist.districtname = districtname
        districtlist.save()
        
        return JsonResponse({"success":True})
    
    elif request.method == "GET":
        districtlist = districts.objects.filter(stateid=id)
        serializers = DistrictSerializer(districtlist,many=True)
        return JsonResponse(serializers.data,safe=False)
    
@csrf_exempt                
def courses(request):
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        
        courselist = Courses()
        courselist.coursename = name
        courselist.coursedescription = description
        courselist.status = "ACTIVE"
        courselist.save()
        
        return JsonResponse({"success":True})
    
    elif request.method == "GET":
        courselist = Courses.objects.all()
        serializers = CourseSerializer(courselist,many=True)
        return JsonResponse(serializers.data,safe=False)
    
    
@csrf_exempt
def subject(request,id=0):
    if request.method == "GET":
        sql_query = "SELECT * FROM guest_subjects s INNER JOIN guest_staff t ON s.staffid = t.staffid WHERE s.courseid=%s"
        result = Courses.objects.raw(sql_query,[id])
        data = [
            {
                'coursename':data.coursename,
                'subjectname':data.subjectname,
                'fees':data.fees,
                'duration':data.duration,
                'courseid':data.courseid,
                'staff_firstname':data.staff_firstname,
                'staff_lastname':data.staff_lastname,
                'description':data.description,
                'subjectid':data.subjectid
            }
            for data in result
        ]
        return JsonResponse(data,safe=False)   
    
    elif request.method == "POST":
        name = request.POST.get('subjectname')
        courseid = request.POST.get('courseid')
        fees = request.POST.get('fees')
        duration = request.POST.get('duration')
        staffid = request.POST.get('staff')
        description = request.POST.get('description')
        subjectlist = Subjects()
        
        subjectlist.subjectname = name
        subjectlist.courseid = courseid
        subjectlist.fees = fees
        subjectlist.duration = duration
        subjectlist.staffid = staffid
        subjectlist.subject_status = "ACTIVE"
        subjectlist.description = description
        subjectlist.save()
        return JsonResponse({"success":True})

@csrf_exempt    
def staffs(request,id=0):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        contactno = request.POST.get('contactno')
        qualification = request.POST.get('qualification')
        gender = request.POST.get('gender')
        year = request.POST.get('year')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        
        loginlist = login()
        
        loginlist.username = username
        loginlist.password = password
        loginlist.role = "STAFF"
        loginlist.status = "ACTIVE"
        loginlist.save()
        
        last_inserted_id = loginlist.loginid
        
        stafflist = staff()
        
        stafflist.staff_firstname = firstname
        stafflist.staff_lastname = lastname
        stafflist.email_id = email
        stafflist.contact_no = contactno
        
        stafflist.qualification = qualification
        stafflist.gender = gender
        stafflist.experience = year
        stafflist.loginid = last_inserted_id
        stafflist.date = date.today()
        
        
        stafflist.save()
        
        return JsonResponse({"success":True})
    
    elif request.method == "GET":
        sql_query = "SELECT * FROM `guest_staff` s INNER JOIN `guest_login` l ON s.loginid = l.loginid"
        result = staff.objects.raw(sql_query)
        data = [
            {
                'firstname':data.staff_firstname,
                'lastname':data.staff_lastname,
                'email':data.email_id,
                'contactno':data.contact_no,
                
                'qualification':data.qualification,
                'gender':data.gender,
                'experience':data.experience,
                'date':data.date,
                'status':data.status,
                'loginid':data.loginid,
                'staffid':data.staffid,
                
                'staffimage':data.staffimage
            }
            for data in result
        ]
        return JsonResponse(data,safe=False)
    
    elif request.method == "DELETE":
        stafflist = staff.objects.get(staffid=id)
        stafflist.delete()
        return JsonResponse({"success":True})
        
        
def activate(request,id):
    if request.method == "GET":
        print(id)
        loginlist = login.objects.get(loginid=id)
        loginlist.status = "ACTIVE"
        loginlist.save()
        
        return JsonResponse({"success":True})

def deactivate(request,id):
    if request.method == "GET":
        print(id)
        loginlist = login.objects.get(loginid=id)
        loginlist.status = "NON-ACTIVE"
        loginlist.save()
        
        return JsonResponse({"success":True})
    
@csrf_exempt       
def staffedit(request,id=0):
    if request.method == "GET":
        sql_query = "SELECT * FROM guest_staff s INNER JOIN guest_login l ON s.loginid = l.loginid WHERE s.staffid = %s"
        result = staff.objects.raw(sql_query,[id])
        data = [
                    {
                        'staffid': row.staffid,
                        'firstname': row.staff_firstname,
                        'lastname': row.staff_lastname,
                        'email': row.email_id,
                        'contactno': row.contact_no,
                        
                        
                        'qualification': row.qualification,
                        'gender': row.gender,
                        'experience': row.experience,
                        'username': row.username,
                        'password': row.password
                    }
                    for row in result
                ]
            
                
        
        return JsonResponse(data,safe=False)      
    
    elif request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        contactno = request.POST.get('contactno')
        course = request.POST.get('course')
        qualification = request.POST.get('qualification')
        gender = request.POST.get('gender')
        year = request.POST.get('year')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        
        
        stafflist = staff.objects.get(staffid=id)
        
        stafflist.staff_firstname = firstname
        stafflist.staff_lastname = lastname
        stafflist.email_id = email
        stafflist.contact_no = contactno
        stafflist.course = course
        stafflist.qualification = qualification
        stafflist.gender = gender
        stafflist.experience = year
        stafflist.save()
        
        loginid = stafflist.loginid
        
        loginlist = login.objects.get(loginid=loginid)
        
        loginlist.username = username
        loginlist.password = password
        loginlist.save()
        
        return JsonResponse({"success":True})
          
@csrf_exempt
def getsubjectall(request):
    
    if request.method == "GET":
        sql_query = "SELECT * FROM guest_subjects s INNER JOIN guest_staff t ON s.staffid = t.staffid"
        result = Courses.objects.raw(sql_query)
        data = [
            {
                'coursename':data.coursename,
                'subjectname':data.subjectname,
                'fees':data.fees,
                'duration':data.duration,
                'courseid':data.courseid,
                'staff_firstname':data.staff_firstname,
                'staff_lastname':data.staff_lastname,
                'description':data.description,
                'subjectid':data.subjectid
            }
            for data in result
        ]
        return JsonResponse(data,safe=False)    

@csrf_exempt
def messages(request,id=0):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        messagearea = request.POST.get('message')
        
        messagelist = message() 
        
        messagelist.name = name
        messagelist.email = email
        messagelist.message = messagearea
        messagelist.staffid = 0
        messagelist.save()
        return JsonResponse({"success":True})
    
    elif request.method == "GET":
        messagelist = message.objects.filter(staffid=0)
        serialize = MessageSerializer(messagelist,many=True)
        return JsonResponse(serialize.data,safe=False)
    
    elif request.method == "DELETE":
        messagelist = message.objects.get(id=id)
        messagelist.delete()
        return JsonResponse({"success":True})
            
def logout(request):
    if request.method == "GET":
        request.session.flush()
        return JsonResponse({"success":True})   
    
def staffgetbystudent(request,id=0):
    if request.method == "GET":
       customerid = id
      
       sql_query = "SELECT * FROM guest_students s INNER JOIN guest_subjects u ON s.subject = u.subjectid INNER JOIN guest_login l ON l.loginid = s.loginid INNER JOIN guest_courses c ON c.courseid = u.courseid INNER JOIN guest_staff st ON st.staffid = u.staffid WHERE s.loginid = %s"
       result = Students.objects.raw(sql_query,[customerid])
       data = [
           {
               'student_firstname':data.student_firstname,
               'student_lastname':data.student_lastname,
               'coursename':data.coursename,
               'subjectname':data.subjectname,
               'staff_firstname':data.staff_firstname,
               'staff_lastname':data.staff_lastname,
               'duration':data.duration,
               'description':data.description
               
           }
           for data in result
       ]
       print(data)
       
       return JsonResponse(data,safe=False)
         
def getsubjectwithstaff(request,id=0):
    if request.method == "GET":
        sql_query = "SELECT * FROM `guest_subjects` s INNER JOIN `guest_staff` t ON s.staffid = t.staffid INNER JOIN `guest_courses` c ON  c.courseid = s.courseid"
        result = Subjects.objects.raw(sql_query)
        data = [
            {
                'subjectid':data.subjectid,
                'subjectname':data.subjectname,
                'coursename':data.coursename,
                'fees':data.fees,
                'duration':data.duration,
                'staff_firstname':data.staff_firstname,
                'staff_lastname':data.staff_lastname,
                'status':data.subject_status,
                'description':data.description
            }
            for data in result
        ]
        
        return JsonResponse(data,safe=False)
    
    elif request.method == "DELETE":
        subjectlist = Subjects.objects.get(subjectid = id)
        subjectlist.delete()
        return JsonResponse({"success":True})

def activatesubject(request,id=0):
    if request.method == "GET":
        subjectlist = Subjects.objects.get(subjectid = id)
        subjectlist.subject_status = "ACTIVE"
        subjectlist.save()
        return JsonResponse({"success":True})
        
def deactivatesubject(request,id=0):
    if request.method == "GET":
        subjectlist = Subjects.objects.get(subjectid = id)
        subjectlist.subject_status = "NON-ACTIVE"
        subjectlist.save()
        return JsonResponse({"success":True})
        
def getstaff(request,id=0):
    if request.method == "GET":
        sql_query = "SELECT * FROM `guest_staff` s INNER JOIN `guest_login` l ON s.loginid = l.loginid WHERE l.loginid = %s"
        loginid = id
        result = staff.objects.raw(sql_query,[loginid])
        
        data = [
            {
                'staff_firstname':data.staff_firstname,
                'staff_lastname':data.staff_lastname
            }
            for data in result
        ]
        
        return JsonResponse(data,safe=False)
    
def getstudentforstaff(request, id=0):
    if request.method == "GET":
        staffid = id 
        sql_query = "SELECT * FROM guest_students s INNER JOIN guest_subjects u ON s.subject = u.subjectid INNER JOIN guest_staff t ON t.staffid = u.staffid WHERE t.staffid = %s;"
        result = Students.objects.raw(sql_query, [staffid])
        data = [
            {
                'student_firstname': student.student_firstname,
                'student_lastname': student.student_lastname,
                'subjectname': student.subjectname,
                'contactno': student.contactno,
                'email': student.email,
                'studentid': student.studentid
            }
            for student in result
        ]

        for student_data in data:
            student_id = student_data['studentid']
            student_firstname = student_data['student_firstname']
            student_lastname = student_data['student_lastname']
            attendance_date = date.today()
            
            if not attendance.objects.filter(studentid=student_id, attendance_date=attendance_date).exists():
                attendancelist = attendance()
                attendancelist.studentid = student_id
                attendancelist.student_firstname = student_firstname
                attendancelist.student_lastname = student_lastname
                attendancelist.attendance_date = attendance_date
                attendancelist.status = "PRESENT"
                attendancelist.mark = "NOT-MARKED"
                attendancelist.save()

        return JsonResponse(data, safe=False)
                
                
            
            
                
        
        
    
def present(request,id=0):
    if request.method == "GET":
        studentid = id
        print(studentid)
        attendance_date = date.today()
        attendancelist = attendance.objects.get(studentid=studentid,attendance_date=attendance_date)
        attendancelist.status = "PRESENT"
        attendancelist.mark = "MARKED"
        
        attendancelist.save()
        
        return JsonResponse({"success":True})
    
def absent(request,id=0):
    if request.method == "GET":
        studentid = id
        attendance_date = date.today()
        print(studentid)
        attendancelist = attendance.objects.get(studentid=studentid,attendance_date=attendance_date)
        attendancelist.status = "ABSENT"
        attendancelist.mark = "MARKED"
        
        attendancelist.save()
        
        return JsonResponse({"success":True})
        
def attendancehistory(request):
    if request.method == "GET":
        dates = date.today()
        sql_query = "SELECT * FROM `guest_attendance` a INNER JOIN `guest_students` s ON a.studentid = s.studentid WHERE a.attendance_date = %s AND a.mark='NOT-MARKED'"
        result = attendance.objects.raw(sql_query,[dates])
        data = [
            {
                'status':data.status,
                'mark':data.mark,
                'student_firstname':data.student_firstname,
                'student_lastname':data.student_lastname,
                'studentid':data.studentid
            }
            for data in result
        ]
        
        return JsonResponse(data,safe=False)
    
def attendances(request,id=0):
    if request.method == "GET":
        loginid = id
        sql_query = "SELECT * FROM `guest_students` s INNER JOIN `guest_login` l ON s.loginid = l.loginid WHERE s.loginid = %s"
        result = Students.objects.raw(sql_query,[loginid])
        data = [
            {
                'studentid':data.studentid
            }
            for data in result
        ]
        
        studentid = data[0]['studentid']
        print(studentid)
        
        sql_query1 = "SELECT studentid, COUNT(*) AS total FROM guest_attendance WHERE studentid = %s AND mark='MARKED' GROUP BY studentid"
        
        with connection.cursor() as cursor:
            cursor.execute(sql_query1, [studentid])
            result1 = cursor.fetchall()  # Fetch the first row of the result
            totaldays = result1[0][1]
            print(totaldays)
            
        sql_query2 = "SELECT COUNT(*) AS present_count FROM guest_attendance WHERE status = 'present' AND mark = 'MARKED' AND studentid = %s"
        with connection.cursor() as cursor:
            cursor.execute(sql_query2, [studentid])
            result2 = cursor.fetchall()  # Fetch the first row of the result
            presentdays = result2[0][0]
            print(presentdays)
            
            formatted_percentage = (presentdays/totaldays)*100
            print(formatted_percentage)
            attendance_percentage = round(formatted_percentage, 1)
            
        return JsonResponse({"success":True,"attendance_percentage":attendance_percentage,"presentdays":presentdays,"totaldays":totaldays})
            
def attendancehistorywithid(request,id=0):
    if request.method == "GET":
        loginid = id
        sql_query = "SELECT * FROM `guest_login` l INNER JOIN `guest_students` s ON l.loginid = s.loginid WHERE l.loginid = %s"
        result = login.objects.raw(sql_query,[loginid])
        resultdata = [
                            {
                                'studentid':item.studentid
                            }
                            for item in result
                        ]
                
        studentid = resultdata[0]['studentid']
        sql_query1 = "SELECT * FROM `guest_attendance` WHERE studentid = %s AND mark = 'MARKED'"
        print (sql_query1)
        result1 = attendance.objects.raw(sql_query1,[studentid])
        data = [
            {
                'date':data.attendance_date,
                'status':data.status
            }
            for data in result1
        ]       
        

                    
        return JsonResponse(data,safe=False)

@csrf_exempt
def attendancedate(request):
    if request.method == "POST":
        fromDate = request.POST.get('fromDate')
        toDate = request.POST.get('toDate')
        loginid = request.POST.get('ID')
        id = loginid
        sql_query1 = "SELECT * FROM `guest_login` l INNER JOIN `guest_students` s ON l.loginid = s.loginid WHERE l.loginid = %s"
        result1 = login.objects.raw(sql_query1,[id])
        resultdata = [
                            {
                                'studentid':item.studentid
                            }
                            for item in result1
                        ]
                
        studentid = resultdata[0]['studentid']
        sqlquery2 = "SELECT * FROM `guest_attendance` WHERE attendance_date BETWEEN %s AND %s AND studentid = %s AND mark = 'MARKED'"
        result2 = attendance.objects.raw(sqlquery2,[fromDate,toDate,studentid])
        data = [
                            {
                                'date':data.attendance_date,
                                'status':data.status
                            }
                            for data in result2
                        ]
        
        return JsonResponse(data,safe=False)
    

def getstudent(request,id=0):
    if request.method == "GET":
        loginid = id
        print(loginid)
        sql_query1 = "SELECT * FROM `guest_login` l INNER JOIN `guest_students` s ON l.loginid = s.loginid WHERE l.loginid = %s"
        result1 = login.objects.raw(sql_query1,[loginid])
        resultdata = [
                        {
                            'studentid':item.studentid
                        }
                        for item in result1
                    ]
                    
        studentid = resultdata[0]['studentid']
        print(studentid)
        sqlquery2 = "SELECT * FROM `guest_students` s INNER JOIN guest_districts d ON s.district = d.districtid INNER JOIN guest_states l ON s.state = l.stateid INNER JOIN guest_courses c ON s.course = c.courseid INNER JOIN guest_subjects x ON s.subject = x.subjectid INNER JOIN guest_staff f ON x.staffid = f.staffid INNER JOIN guest_login log ON s.loginid = log.loginid WHERE s.studentid = %s"
        result2 = Students.objects.raw(sqlquery2,[studentid])
        data = [
                    {
                        'student_firstname':data.student_firstname,
                        'student_lastname':data.student_lastname,
                        'email':data.email,
                        'contactno':data.contactno,
                        'district':data.districtname,
                        'state':data.statename,
                        'address':data.address,
                        'pincode':data.pincode,
                        'course':data.coursename,
                        'subject':data.subjectname,
                        'dob':data.dob,
                        'date':data.date,
                        'subjectid':data.subjectid,
                        'username':data.username,
                        'password':data.password
                    }
                    for data in result2
        ]
            
        return JsonResponse(data,safe=False)
    
@csrf_exempt
def updateprofile(request,id=0):
    if request.method == "POST":
        username = request.POST.get('username')
        dob = request.POST.get('dob')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        print(email,username,mobile,dob)
        
        loginlist = login.objects.get(loginid=id)
        
        loginlist.username = username
        loginlist.save()
        
        loginid = id
        
        sql_query1 = "SELECT * FROM `guest_login` l INNER JOIN `guest_students` s ON l.loginid = s.loginid WHERE l.loginid = %s"
        result1 = login.objects.raw(sql_query1,[loginid])
        resultdata = [
                        {
                            'studentid':item.studentid
                        }
                        for item in result1
                    ]
                    
        studentid = resultdata[0]['studentid']
        print(studentid)
        
        studentlist = Students.objects.get(studentid=studentid)
        print(studentlist)
        studentlist.email = email
        studentlist.dob = dob
        studentlist.contactno = mobile
        studentlist.save()
        
        return JsonResponse({"success":True})
    
@csrf_exempt    
def changepassword(request,id=0):
    if request.method == "POST":
        loginid = id
        print(loginid)
        password = request.POST.get('currentpassword')
        newpassword = request.POST.get('newpassword')
        retypepass = request.POST.get('retypepass')
        if newpassword == retypepass:
            
            loginlist = login.objects.filter(loginid=loginid,password=password)
            if loginlist.exists():
                loginlist1 = login.objects.get(loginid=loginid,password=password)
                loginlist1.password = newpassword
                loginlist1.save()
                return JsonResponse({"success":True})
            else:
                return JsonResponse({"password":True})
        else:
            return JsonResponse({"retype":True})
        
@csrf_exempt  
def checkform(request,id=0):
    if request.method == "POST":
        loginid = id
        print(loginid)
        password = request.POST.get('currentpassword') 
        loginlist = login.objects.filter(loginid=loginid,password=password)
        if loginlist.exists(): 
            return JsonResponse({"success":True})  
        else:
            return JsonResponse({"fail":True})
        
@csrf_exempt
def sendmessage(request, id=0):
    if request.method == "POST":
        # Handle POST request
        loginid = id
        messages = request.POST.get('messages')
        
        # Fetch studentid based on loginid
        result1 = login.objects.raw("SELECT * FROM `guest_login` l INNER JOIN `guest_students` s ON l.loginid = s.loginid WHERE l.loginid = %s", [loginid])
        studentid = result1[0].studentid
        
        # Fetch staffid based on studentid
        result2 = Students.objects.raw("SELECT * FROM `guest_students` s INNER JOIN `guest_subjects` u ON s.subject = u.subjectid WHERE s.studentid = %s", [studentid])
        staffid = result2[0].staffid
        
        # Save message in chat and staffchat tables
        current_date = date.today()
        current_time = datetime.now().time().strftime("%H:%M")
        
        chat.objects.create(
            staffid=staffid,
            studentid=studentid,
            senderid=studentid,
            reciverid=staffid,
            messages=messages,
            date=current_date,
            time=current_time,
            sender="STUDENT",
            status="send"
        )
        
        staffchat.objects.create(
            staffid=staffid,
            studentid=studentid,
            senderid=studentid,
            reciverid=staffid,
            messages=messages,
            date=current_date,
            time=current_time,
            sender="STUDENT",
            status="unread"
        )
        
        return JsonResponse({"success": True})
    
    elif request.method == "GET":
        # Handle GET request
        loginid = id
        
        # Fetch studentid based on loginid
        result1 = login.objects.raw("SELECT * FROM `guest_login` l INNER JOIN `guest_students` s ON l.loginid = s.loginid WHERE l.loginid = %s", [loginid])
        studentid = result1[0].studentid
        
        # Fetch chat messages based on studentid
        result2 = chat.objects.raw("SELECT * FROM `guest_chat` c INNER JOIN `guest_staff` s ON c.staffid = s.staffid WHERE c.studentid = %s", [studentid])
        
        today_date = date.today()
        yesterday_date = today_date - timedelta(days=1)
        
        today_messages = []
        other_messages = []
        yesterday_messages = []
        
        for item in result2:
            if item.date == today_date:
                today_messages.append({
                    'staff_firstname': item.staff_firstname,
                    'staff_lastname': item.staff_lastname,
                    'date': item.date,
                    'time': item.time,
                    'messages': item.messages,
                    'senderid': item.senderid,
                    'reciverid': item.reciverid,
                    'staffid': item.staffid,
                    'studentid': item.studentid,
                    'sender': item.sender
                })
            elif item.date == yesterday_date:
                yesterday_messages.append({
                    'staff_firstname': item.staff_firstname,
                    'staff_lastname': item.staff_lastname,
                    'date': item.date,
                    'time': item.time,
                    'messages': item.messages,
                    'senderid': item.senderid,
                    'reciverid': item.reciverid,
                    'staffid': item.staffid,
                    'studentid': item.studentid,
                    'sender': item.sender
                })
            else:
                other_messages.append({
                    'staff_firstname': item.staff_firstname,
                    'staff_lastname': item.staff_lastname,
                    'date': item.date,
                    'time': item.time,
                    'messages': item.messages,
                    'senderid': item.senderid,
                    'reciverid': item.reciverid,
                    'staffid': item.staffid,
                    'studentid': item.studentid,
                    'sender': item.sender
                })
                # dates = other_messages['date']
                # print(dates)
        
        return JsonResponse({'todaymessages': today_messages, 'othermessages': other_messages,'yesterdaymessages':yesterday_messages,'yesterday_date':yesterday_date})

    elif request.method == "DELETE":
        # Handle DELETE request
        loginid = id
        
        # Fetch studentid based on loginid
        result1 = login.objects.raw("SELECT * FROM `guest_login` l INNER JOIN `guest_students` s ON l.loginid = s.loginid WHERE l.loginid = %s", [loginid])
        studentid = result1[0].studentid
        
        # Delete all chat messages for the student
        chat.objects.filter(studentid=studentid).delete()
        
        return JsonResponse({"success": True})
    
    else:
        return JsonResponse({"error": "Invalid request method"})

        
def staffmessages(request,id=0,studentid=0):
    if request.method == "GET":
        staffid = id
        sql_query2 = "SELECT * FROM `guest_staffchat` c INNER JOIN `guest_staff` s ON c.staffid = s.staffid INNER JOIN `guest_students` u ON c.studentid = u.studentid INNER JOIN guest_students st ON c.studentid = st.studentid INNER JOIN guest_courses co ON co.courseid = st.course INNER JOIN guest_subjects su ON su.subjectid = st.subject WHERE c.staffid = %s AND u.studentid = %s"
        result2 = Students.objects.raw(sql_query2,[staffid,studentid])
        
        today_date = date.today()
        yesterday_date = today_date - timedelta(days=1)
        
        today_messages = []
        other_messages = []
        yesterday_messages = [] 
        for item in result2:
            if item.date == today_date:
                today_messages.append({
                    'student_firstname': item.student_firstname,
                    'student_lastname': item.student_lastname,
                    'date': item.date,
                    'time': item.time,
                    'messages': item.messages,
                    'senderid': item.senderid,
                    'reciverid': item.reciverid,
                    'staffid': item.staffid,
                    'studentid': item.studentid,
                    'sender': item.sender
                })
            elif item.date == yesterday_date:
                yesterday_messages.append({
                    'student_firstname': item.student_firstname,
                    'student_lastname': item.student_lastname,
                    'date': item.date,
                    'time': item.time,
                    'messages': item.messages,
                    'senderid': item.senderid,
                    'reciverid': item.reciverid,
                    'staffid': item.staffid,
                    'studentid': item.studentid,
                    'sender': item.sender
                })
            else:
                other_messages.append({
                    'student_firstname': item.student_firstname,
                    'student_lastname': item.student_lastname,
                    'date': item.date,
                    'time': item.time,
                    'messages': item.messages,
                    'senderid': item.senderid,
                    'reciverid': item.reciverid,
                    'staffid': item.staffid,
                    'studentid': item.studentid,
                    'sender': item.sender
                })
        
        return JsonResponse({'todaymessages': today_messages, 'othermessages': other_messages,'yesterdaymessages':yesterday_messages,'yesterday_date':yesterday_date})
        
def getstudentsinchat(request,id=0):
    if request.method == "GET":
        staffid = id 
        sql_query = "SELECT * FROM `guest_students` s INNER JOIN guest_subjects u ON s.subject = u.subjectid INNER JOIN guest_staff t ON t.staffid = u.staffid WHERE t.staffid = %s;"   
        result = Students.objects.raw(sql_query,[staffid])

        data = [
                        {
                            'student_firstname':item.student_firstname,
                            'student_lastname':item.student_lastname,
                            'studentid':item.studentid,
                            'subjectname':item.subjectname,
                            'status':item.student_status,
                            'login_date':item.login_date,
                            'login_time':item.login_time
                            
                            
                        }
                        for item in result
                    ]
        
        countdata = []
        
        
        
        for count in data:
            studentid = count['studentid']
            with connection.cursor() as cursor:
                sql_query1 = "SELECT count(*) as TOTAL FROM guest_staffchat WHERE studentid=%s AND status='unread'"
                cursor.execute(sql_query1,[studentid])
                result = cursor.fetchone()
                print(result[0])
                
                countdata.append({"studentid":studentid,"count":result[0]})
                
        
        print(countdata)
        
        response_data = {
            
            'data':data,
            'countdata':countdata
        }
        
        return JsonResponse(response_data,safe=False)
    
@csrf_exempt
def sendstaffmessage(request,id=0,studentid=0):
    if request.method == "POST":
        staffid = id
        studentid = studentid
        print(studentid)
        messages = request.POST.get('messages')
        senderid = staffid
        reciverid = studentid
        dates = date.today()
        current_time = datetime.now().time().strftime("%H:%M")
        
        chatlist = chat()
        chatlist.staffid = staffid
        chatlist.studentid = studentid
        chatlist.senderid = senderid
        chatlist.reciverid = reciverid
        chatlist.messages = messages
        chatlist.date = dates
        chatlist.time = current_time
        chatlist.sender = "STAFF"
        chatlist.status = "unread"
        chatlist.save()
        
        staffchatlist = staffchat()
        staffchatlist.staffid = staffid
        staffchatlist.studentid = studentid
        staffchatlist.senderid = senderid
        staffchatlist.reciverid = reciverid
        staffchatlist.messages = messages
        staffchatlist.date = dates
        staffchatlist.time = current_time
        staffchatlist.sender = "STAFF"
        staffchatlist.status = "send"
        staffchatlist.save()
        
        return JsonResponse({"success":True})
    
    elif request.method == "DELETE":
        staffchatlist = staffchat.objects.filter(staffid=id,studentid=studentid)
        staffchatlist.delete()
        
        return JsonResponse({"success":True})

@csrf_exempt
def addevent(request,id=0):
    if request.method == "POST":
        subjectid = request.POST.get('subjectid')
        name = request.POST.get('name')
        date = request.POST.get('date')
        duration = request.POST.get('duration')
        price = request.POST.get('price')
        
        eventlist = events()
        
        eventlist.subjectid = subjectid
        eventlist.eventname = name
        eventlist.date = date
        eventlist.duration = duration
        eventlist.price = price
        eventlist.save()
        
        return JsonResponse({"success":True})
    
    if request.method == "GET":
        sql_query = "SELECT * FROM guest_events e INNER JOIN guest_subjects s ON e.subjectid = s.subjectid"
        result = events.objects.raw(sql_query)
        data = [
            {
                'subjectname' : item.subjectname,
                'eventname':item.eventname,
                'date':item.date,
                'duration':item.duration,
                'price':item.price,
                'id':item.id
            }
            for item in result
        ]
        
        return JsonResponse(data,safe=False)
    
    elif request.method == "DELETE":
        eventlist = events.objects.get(id=id)
        eventlist.delete()
        
        return JsonResponse({"success":True})
    
@csrf_exempt    
def geteventsbyid(request,id=0):
    if request.method == "GET":
        eventlist = events.objects.filter(id=id)
        serialize = EventsSerializer(eventlist,many=True)
        return JsonResponse(serialize.data,safe=False)
    
@csrf_exempt
def updateevent(request,id=0):
    if request.method == "POST":
        subjectid = request.POST.get('subjectid')
        name = request.POST.get('name')
        date = request.POST.get('date')
        duration = request.POST.get('duration')
        price = request.POST.get('price')
        
        eventlist = events.objects.get(id=id)
        
        eventlist.subjectid = subjectid
        eventlist.eventname = name
        eventlist.date = date
        eventlist.duration = duration
        eventlist.price = price
        eventlist.save()
        
        return JsonResponse({"success":True})
    
@csrf_exempt
def eventsubmitform(request):
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        eventname = request.POST.get('event')
        
        eventlist = eventregister()
        
        eventlist.name = name
        eventlist.phone = phone
        eventlist.email = email
        eventlist.eventname = eventname
        eventlist.save()
        
        return JsonResponse({"success":True})
        
    elif request.method == "GET":
        eventlist = eventlist.objects.all()
        serialize = EventsViewSerializer(eventlist,many=True)
        return JsonResponse(serialize.data,safe=False)
    
@csrf_exempt        
def getstudentsdetailes(request,id=0):
    
    if request.method == "GET":
        sql_query = "SELECT * FROM guest_students S INNER JOIN guest_districts d ON s.district = d.districtid INNER JOIN guest_states g ON s.state = g.stateid INNER JOIN guest_courses c ON s.course = c.courseid INNER JOIN guest_subjects u ON s.subject = u.subjectid WHERE S.studentid = %s"
        result = Students.objects.raw(sql_query,[id])
        data = [
            {
                'student_firstname':item.student_firstname,
                'student_lastname':item.student_lastname,
                'course':item.coursename,
                'subject':item.subjectname
                
            }
            for item in result
        ]
        
        
        return JsonResponse(data,safe=False)
    
@csrf_exempt   
def otpfunction(request,id=0):
    if request.method == "POST":
        email = request.POST.get('username')
        
        studentlist = Students.objects.filter(email=email)
        if studentlist.exists():
            studentlist = Students.objects.get(email=email)
            studentid = studentlist.studentid
            emailid = studentlist.email
            
            otpnumber = random.randint(100000,999999)
            print(emailid)
            print(otpnumber)
            
            otplist = otp()
            otplist.email = emailid
            otplist.otp = otpnumber
            otplist.time = datetime.now()
            otplist.save()
            
            send_mail(
            'Your OTP Code',
            f'Your OTP is {otpnumber}',
            settings.EMAIL_HOST_USER,
            [emailid],
            fail_silently=False,
            )
            
            return JsonResponse({"success":True,"studentid":studentid})
        else:
            return JsonResponse({"fail":True})

    elif request.method == "DELETE":
        studentid = id
        studentlist = Students.objects.get(studentid=id)
        emailid = studentlist.email
        
        otplist = otp.objects.filter(email=emailid)
        otplist.delete()
        
        return JsonResponse ({"success":True})

@csrf_exempt  
def otpdone(request,id=0):
    if request.method == "POST":
        otpnumber = request.POST.get('otp')
        otp_number = int(otpnumber)
        studentid = id
        studentlist = Students.objects.get(studentid=studentid)
        email = studentlist.email
        sql_query = "SELECT * FROM guest_otp WHERE email = %s ORDER BY id DESC LIMIT 1"
        result = otp.objects.raw(sql_query,[email])
        data = [
            {
                'otp':item.otp
            }
            for item in result
        ]
        
        otpindata = int(data[0]['otp'])
        print(otpindata)
        print(otp_number)
        
        return JsonResponse({"Fail":True,"otpnumber":otp_number,"otpindata":otpindata})
    
@csrf_exempt
def changepasswordbyotp(request,id=0):
    if request.method == "POST":
        newpass = request.POST.get('newpass')
        studentid = id
        studentlist = Students.objects.get(studentid=studentid)
        loginid = studentlist.loginid
        loginlist = login.objects.get(loginid=loginid)
        loginlist.password = newpass
        loginlist.save()
        
        return JsonResponse({"success":True})
    
def getcount(request,id):
    if request.method == "GET":
        with connection.cursor() as cursor:
            sql_query = "SELECT COUNT(*) AS TOTAL FROM guest_students s inner join guest_subjects b on s.subject=b.subjectid inner join guest_staff t on t.staffid = b.staffid WHERE b.staffid = %s"
            cursor.execute(sql_query,[id])
            row = cursor.fetchone()
            
            if row:
                students_count = row[0]
            else:
                students_count = 0
            
                   
            sql_query1 = "SELECT COUNT(*) AS UNREAD FROM `guest_staffchat` WHERE staffid = %s AND status='unread'"
            cursor.execute(sql_query1,[id])
            row1 = cursor.fetchone()
            if row1:
                unread_message = row1[0]
            else:
                unread_message = 0
        
        
        return JsonResponse({"success":True,"students_count":students_count,"unread_message":unread_message})
    
def status(request,id,studentid):
    if request.method == "GET":
        print("hi") 
        staffchatlist = staffchat.objects.filter(studentid=studentid,status="unread",staffid=id)
        for data in staffchatlist:
            print(data.messages)
            data.status = "read"
            data.save()
        return JsonResponse({"success":True})
    
def studentlogout(request,id):
    if request.method == "GET":
        studentfunction = Students.objects.get(loginid=id)
        studentfunction.student_status = "not-active"
        logindate = date.today()
        logintime = datetime.today()
        login_time_formatted = logintime.strftime('%H:%M')
        print(login_time_formatted)
        studentfunction.login_date = logindate
        studentfunction.login_time = login_time_formatted
        studentfunction.save()
        request.session.flush()
        return JsonResponse({"success":True})   
    
def getstudentswithactive(request):
    if request.method == "GET":
        sql_query = "SELECT * FROM guest_students s INNER JOIN guest_login l ON s.loginid = l.loginid INNER JOIN guest_districts d ON s.district = d.districtid INNER JOIN guest_states g ON s.state = g.stateid INNER JOIN guest_courses c ON s.course = c.courseid INNER JOIN guest_subjects u ON s.subject = u.subjectid"
        result = login.objects.raw(sql_query)
        
        data = [
            {
                'status':data.status,
                'username':data.username,
                'student_firstname':data.student_firstname,
                'student_lastname':data.student_lastname,
                'loginid':data.loginid,
                'email':data.email,
                'contactno':data.contactno,
                'district':data.districtname,
                'state':data.statename,
                'address':data.address,
                'pincode':data.pincode,
                'studentid':data.studentid,
                'subject':data.subjectname,
                'date':data.date,
                'course':data.coursename,
                'dob':data.dob
            }   
            for data in result
        ]
        
        return JsonResponse(data,safe=False)

def subjectwithid(request,id=0):
    if request.method == "GET":
        sql_query = "SELECT * FROM guest_subjects s INNER JOIN guest_staff t on s.staffid = t.staffid WHERE s.subjectid=%s"
        result = Subjects.objects.raw(sql_query,[id])
        data = [
            {
                
                'subjectname':data.subjectname,
                'fees':data.fees,
                'duration':data.duration,
                'courseid':data.courseid,
                'staff_firstname':data.staff_firstname,
                'staffid':data.staffid,
                'staff_lastname':data.staff_lastname,
                'description':data.description,
                'subjectid':data.subjectid
            }
            for data in result
            
        ]
        return JsonResponse(data,safe=False)
 
@csrf_exempt   
def updatesubject(request,id=0):
    if request.method == "POST":
        name = request.POST.get('subjectname')
        courseid = request.POST.get('courseid')
        fees = request.POST.get('subjectfees')
        duration = request.POST.get('subjectduration')
        staffid = request.POST.get('staff')
        description = request.POST.get('description')
        
        subjectlist = Subjects.objects.get(subjectid=id)
        subjectlist.subjectname = name
        subjectlist.courseid = courseid
        subjectlist.fees = fees
        subjectlist.duration = duration
        subjectlist.staffid = staffid
        subjectlist.subject_status = "ACTIVE"
        subjectlist.description = description
        subjectlist.save()
        
        return JsonResponse({"success":True})
    
@csrf_exempt
def getbankdetails(request):
    if request.method == "POST":
        account = request.POST.get('account')
        ifsc = request.POST.get('ifsc')
        
        banklist = Bank.objects.filter(bank_accountnumber=account,bank_ifsccode=ifsc)
        serialize = BankSerializer(banklist,many=True)
        
        return JsonResponse(serialize.data,safe=False)
    
def getsubjectwithsubjectid(request,id=0):
    if request.method == "GET":
        subjectlist = Subjects.objects.filter(subjectid=id)
        serialize = SubjectSerializer(subjectlist,many=True)
        return JsonResponse(serialize.data,safe=False)
    
@csrf_exempt
def cardsubmit(request,id=0):
    if request.method == "POST":
        username = request.POST.get('username')
        cardnumber = request.POST.get('cardnumber')
        mm = request.POST.get('mm')
        yy = request.POST.get('yy')
        cvv = request.POST.get('cvv')
        total = request.POST.get('total')
        datenow = datetime.now().date()
        
        feelist = Fees()
        feelist.student_id = id
        feelist.amount = total
        feelist.date = datenow
        feelist.payment_method = "CARD PAYMENT"
        feelist.save()
        fee_id = feelist.fees_id
        
        
        cardlist = CardPayment()
        cardlist.fees_id = fee_id
        cardlist.username = username
        cardlist.card_number = cardnumber
        cardlist.date = datenow
        cardlist.save()
        
        studentlist = Students.objects.get(studentid=id)
        studentlist.fees_status = "PAID"
        studentlist.save()
        
        
    return JsonResponse({"success":True})

@csrf_exempt
def banksubmit(request,id=0):
    if request.method == "POST":
        account = request.POST.get('account')
        ifsc = request.POST.get('ifsc')
        account_name = request.POST.get('account_name')
        account_owner = request.POST.get('account_owner')
        total = request.POST.get('total')
        datenow = datetime.now().date()
        
        feelist = Fees()
        feelist.student_id = id
        feelist.amount = total
        feelist.date = datenow
        feelist.payment_method = "BANK PAYMENT"
        feelist.save()
        fee_id = feelist.fees_id
        
        banklist = BankPayment()
        banklist.fees_id = fee_id
        banklist.account_number = account
        banklist.ifsc_code = ifsc
        banklist.save()
        
        studentlist = Students.objects.get(studentid=id)
        studentlist.fees_status = "PAID"
        studentlist.save()
        
    return JsonResponse({"success":True})
        
def feesreport(request,id=0):
    if request.method == "GET":
        sql_query = "SELECT * FROM `guest_login` l INNER JOIN guest_students s ON l.loginid = s.loginid WHERE s.loginid=%s"
        result = login.objects.raw(sql_query,[id])
        data = [
            {
                'studentid':item.studentid
            }
            for item in result
        ]
        studentid = data[0]['studentid']
        feelist = Fees.objects.filter(student_id=studentid)
        serialize = FeesSerializer(feelist,many=True)
        
        return JsonResponse(serialize.data,safe=False)
    
def getfeesbystudentid(request,id=0):
    if request.method == "GET":
        sql_query = "SELECT * FROM `guest_login` l INNER JOIN guest_students s ON l.loginid = s.loginid WHERE s.loginid=%s"
        result = login.objects.raw(sql_query,[id])
        data = [
            {
                'studentid':item.studentid
            }
            for item in result
        ]
        studentid = data[0]['studentid']
        sql_query1 = "SELECT * FROM guest_students s INNER JOIN guest_subjects u ON s.subject = u.subjectid WHERE s.studentid = %s"
        result1 = Students.objects.raw(sql_query1,[studentid])
        data = [
            {
            'fees':item.fees
            }
            for item in result1
        ]
        
        
        return JsonResponse(data,safe=False)
    
def feespaid(request,id=0):
    if request.method == "GET":
        sql_query2 = "SELECT * FROM `guest_login` l INNER JOIN guest_students s ON l.loginid = s.loginid WHERE s.loginid=%s"
        result = login.objects.raw(sql_query2,[id])
        data = [
            {
                'studentid':item.studentid
            }
            for item in result
        ]
        studentid = data[0]['studentid']
        
        with connection.cursor() as cursor:
            sql_query = "SELECT SUM(amount) AS total FROM `guest_fees` WHERE student_id = %s"
            cursor.execute(sql_query,[studentid])
            result = cursor.fetchone()
            fees_paid = result[0]
        
        sql_query1 = "SELECT * FROM guest_students s INNER JOIN guest_subjects u ON s.subject = u.subjectid WHERE s.studentid = %s"
        result = Students.objects.raw(sql_query1,[studentid])
        data = [
            {
            'fees':item.fees
            }
            for item in result
        ]
        fees_paid_perfect = int(fees_paid)
        total_fees = int(data[0]['fees'])
        paid_percentage = (fees_paid_perfect/total_fees)*100
        print(paid_percentage)
        percentage = math.floor(paid_percentage)  
        print(percentage)  
        return JsonResponse({"success":True,"fees_paid":fees_paid,"percentage":percentage})
            