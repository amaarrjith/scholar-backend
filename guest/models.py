from django.db import models

# Create your models here.

class Students(models.Model):
    studentid = models.AutoField(primary_key=True)
    student_firstname = models.CharField((""), max_length=50)
    student_lastname = models.CharField((""), max_length=50)
    email = models.CharField((""), max_length=50)
    contactno = models.CharField((""), max_length=50)
    dob = models.CharField((""), max_length=50)
    state = models.CharField((""), max_length=50)
    district = models.CharField((""), max_length=50)
    address = models.TextField((""))
    pincode = models.BigIntegerField((""))
    course = models.CharField((""), max_length=50)
    subject = models.CharField((""), max_length=50)
    loginid = models.IntegerField((""))
    date = models.DateField((""), auto_now=False, auto_now_add=False)
    studentimage = models.CharField((""), max_length=50)
    student_status = models.CharField((""), max_length=50)
    login_date = models.DateField((""), auto_now=False, auto_now_add=False)
    login_time = models.TimeField((""), auto_now=False, auto_now_add=False)
    fees_status = models.CharField((""), max_length=50)

class staff(models.Model):
    staffid = models.AutoField(primary_key=True)
    staff_firstname = models.CharField((""), max_length=50)
    staff_lastname = models.CharField((""), max_length=50)
    email_id = models.CharField((""), max_length=50)
    contact_no = models.CharField((""), max_length=50)
    
    qualification = models.CharField((""), max_length=50)
    gender = models.CharField((""), max_length=50)
    experience = models.CharField((""), max_length=50)
    loginid = models.IntegerField((""))
    date = models.DateField()
    staffimage = models.CharField((""), max_length=50)
    
class login(models.Model):
    loginid = models.AutoField(primary_key=True)
    username = models.CharField((""), max_length=50)
    password = models.CharField((""), max_length=50)
    role = models.CharField((""), max_length=50)
    status = models.CharField((""), max_length=50)
    
    
    
class Courses(models.Model):
    courseid = models.AutoField(primary_key=True)
    coursename = models.CharField((""), max_length=50)
    courseimage = models.CharField((""), max_length=50)
    coursedescription = models.CharField((""), max_length=50)
    status = models.CharField((""), max_length=50)
    
class Subjects(models.Model):
    subjectid = models.AutoField(primary_key=True)
    courseid = models.IntegerField((""))
    subjectname = models.CharField((""), max_length=50)
    description = models.TextField((""))
    fees = models.CharField((""), max_length=50)
    syllabus = models.CharField((""), max_length=50)
    duration = models.CharField((""), max_length=50)
    staffid = models.CharField((""), max_length=50)
    subject_status = models.CharField((""), max_length=50)

class states(models.Model):
    stateid = models.AutoField(primary_key=True)
    statename = models.CharField(max_length=50)
    
class districts(models.Model):
    districtid = models.AutoField(primary_key=True)
    stateid = models.IntegerField()
    districtname = models.CharField(max_length=50)    

class message(models.Model):
    name = models.CharField((""), max_length=50)
    email = models.CharField((""), max_length=50)
    message = models.TextField((""))
    staffid = models.IntegerField((""))
    
class attendance(models.Model):
    studentid = models.IntegerField((""))
    student_firstname = models.CharField((""), max_length=50)
    student_lastname = models.CharField((""), max_length=50)
    attendance_date = models.DateField((""), auto_now=False, auto_now_add=False)
    status = models.CharField((""), max_length=50)
    mark = models.CharField((""), max_length=50)
    
class chat(models.Model):
    chatid = models.AutoField(primary_key=True)
    studentid = models.IntegerField((""))
    staffid = models.IntegerField((""))
    senderid = models.IntegerField((""))
    reciverid = models.IntegerField((""))    
    messages = models.TextField((""))
    date = models.DateField((""), auto_now=False, auto_now_add=False)
    time = models.TimeField((""), auto_now=False, auto_now_add=False)
    sender = models.CharField((""), max_length=50)
    status = models.CharField(max_length=50)
    
class staffchat(models.Model):
    chatid = models.AutoField(primary_key=True)
    studentid = models.IntegerField((""))
    staffid = models.IntegerField((""))
    senderid = models.IntegerField((""))
    reciverid = models.IntegerField((""))    
    messages = models.TextField((""))
    date = models.DateField((""), auto_now=False, auto_now_add=False)
    time = models.TimeField((""), auto_now=False, auto_now_add=False)
    sender = models.CharField((""), max_length=50)
    status = models.CharField(max_length=50)
    
class events(models.Model):
    subjectid = models.IntegerField()
    eventname = models.CharField((""), max_length=50)
    date = models.DateField((""), auto_now=False, auto_now_add=False)
    duration = models.CharField((""), max_length=50)
    price = models.CharField((""), max_length=50)
    eventpic = models.CharField((""), max_length=50)
    description = models.TextField((""))
    
class eventregister(models.Model):
    name = models.CharField((""), max_length=50)
    email = models.EmailField((""), max_length=254)
    phone = models.BigIntegerField((""))
    eventname = models.CharField((""), max_length=50)
    
class otp(models.Model):
    email = models.CharField(max_length=50)
    otp = models.IntegerField((""))
    time = models.TimeField((""), auto_now=False, auto_now_add=False)
    
class Bank(models.Model):
    bank_id = models.AutoField(primary_key=True)
    bank_accountnumber = models.BigIntegerField((""))
    bank_ifsccode = models.CharField((""), max_length=50)
    bank_name = models.CharField((""), max_length=50)
    bank_owner = models.CharField((""), max_length=50)
    
class Fees(models.Model):
    fees_id = models.AutoField(primary_key=True)
    student_id = models.IntegerField((""))
    date = models.DateField((""), auto_now=False, auto_now_add=False)
    amount = models.CharField((""), max_length=50)
    payment_method = models.CharField((""), max_length=50)
    
class CardPayment(models.Model):
    fees_id = models.IntegerField((""))
    username = models.CharField((""), max_length=50)
    card_number = models.BigIntegerField((""))
    date = models.DateField((""), auto_now=False, auto_now_add=False)
    
class BankPayment(models.Model):
    fees_id = models.IntegerField((""))
    account_number = models.BigIntegerField((""))
    ifsc_code = models.CharField((""), max_length=50)