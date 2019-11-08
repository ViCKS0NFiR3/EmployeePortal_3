from flask_sqlalchemy import SQLAlchemy
from model import Employees, work_shifts, Employee_status, Salary_type, Employee_attendance, Restday, db
from datetime import timedelta, datetime

class Employee_class():
    def editUser(self,employeeInfoDict):
        employeeEdit = Employees.query.filter_by(id=employeeInfoDict["user_id"]).first()
        message=""
        resultList = [message, employeeEdit]
        try:
            #employeeEdit = Employees.query.filter_by(id=employeeInfoDict["user_id"]).first()
            #print("EMPLOYEE: " + str(employeeEdit))
            #return redirect(url_for('editUser'))
            employeeEdit.username = employeeInfoDict["userName"]
            employeeEdit.password = employeeInfoDict["passWord"]
            employeeEdit.first_name = employeeInfoDict["firstName"]
            employeeEdit.last_name = employeeInfoDict["lastName"]   
            employeeEdit.age = employeeInfoDict["age"]
            employeeEdit.email = employeeInfoDict["email"]
            employeeEdit.contact_number = employeeInfoDict["contact_number"]	
            employeeEdit.address = employeeInfoDict["address"]
            employeeEdit.rate = employeeInfoDict["rate"]
            employeeEdit.shift_id = employeeInfoDict["shift_id"]
            employeeEdit.salary_type_id = employeeInfoDict["salary_type"]
            employeeEdit.is_admin = employeeInfoDict["is_admin"]
            db.session.commit()
            message = "User Information Updated Successfully."
            resultList = [message, employeeEdit]
        except:
            message = "Error Encountered on Updating User, please try again"
        finally:
            return resultList

    def addUser(self,employeeInfoDict):
        employeeAdd = Employees(
                                username=employeeInfoDict["userName"], 
                                password= employeeInfoDict["passWord"],
                                first_name = employeeInfoDict["firstName"],
                                last_name = employeeInfoDict["lastName"] ,
                                age = employeeInfoDict["age"],
                                email = employeeInfoDict["email"],
                                contact_number = employeeInfoDict["contact_number"],
                                address = employeeInfoDict["address"],
                                rate = employeeInfoDict["rate"],
                                shift_id = employeeInfoDict["shift_id"],
                                salary_type_id = employeeInfoDict["salary_type"],
                                is_admin = employeeInfoDict["is_admin"])
        message=""
        resultList = [message, employeeAdd]
        try:
            db.session.add(employeeAdd)
            db.session.commit()
            message = "User Information Added Successfully."
            resultList = [message, employeeAdd]
        except:
            message = "Error Encountered on Adding User, please try again"
        finally:
            return resultList

    def userTimeIn(self, emp_status, remarks,message, current_user):
        today = datetime.now()
        time_in = today.time()
        penalty = 0
        business_date = datetime.now().date()
        isTimedIn = Employee_attendance.query.with_entities(Employee_attendance.time_in).filter_by(employee_id = current_user.id, business_date = business_date).first()
        print(isTimedIn)
        if isTimedIn is None:
            work_shift_id = Employees.query.with_entities(Employees.shift_id, Employees.username).\
                            filter_by(id=current_user.id).\
                            join(work_shifts,Restday).\
                            add_columns(work_shifts.grace_period, work_shifts.time_out, Restday.day).first()
            print(work_shift_id)
            shiftId = work_shift_id[0]
            username = work_shift_id[1]
            grace_period = work_shift_id[2]
            employeeTimeOut = work_shift_id[3]
            restDay =  work_shift_id[4]
            if today.strftime('%A') != restDay:
                if shiftId == 3:
                    pass
                else:
                    if  grace_period < time_in and time_in < employeeTimeOut:
                        print(grace_period < time_in and time_in < employeeTimeOut)
                        emp_status = 1
                        gracePeriodDateTime = str(business_date) + ' ' + str(grace_period)
                        penalty = today - datetime.strptime(gracePeriodDateTime,'%Y-%m-%d %H:%M:%S')
                        penalty = format((penalty.seconds / 60),'.2f')
                        print('PENALTY: '+ str(penalty))
                        remarks = 'PRESENT'
                    elif  time_in < grace_period and time_in < employeeTimeOut:
                        emp_status = 2
                        penalty = 0
                        remarks = 'PRESENT'
                    else:
                        emp_status = 3
                        penalty = 0
                        remarks = 'ABSENT'
                    message = username + ' TIME IN: ' + time_in.strftime("%H:%M:%S")

            else:
                if shiftId == 3:
                    pass
                else:
                   if grace_period < time_in and time_in < employeeTimeOut:
                        emp_status = 1
                        gracePeriodDateTime = str(business_date) + ' ' + str(grace_period)
                        penalty = today - datetime.strptime(gracePeriodDateTime,'%Y-%m-%d %H:%M:%S')
                        penalty = format((penalty.seconds / 60),'.2f')
                        print(penalty)
                        remarks = 'RESTDAY OT'
                   elif grace_period > time_in and time_in < employeeTimeOut:
                        emp_status = 2
                        penalty = 0
                        remarks = 'RESTDAY OT'
                   else:
                        emp_status = 3
                        penalty = 0
                        remarks = 'RESTDAY'
                   message = username + ' TIME IN: ' + time_in.strftime("%H:%M:%S")
            emp_time_in = {
            "business_date" : business_date,
            "employee_id" : str(current_user.id),
            "time_in" : time_in,
            "employee_status_id" : emp_status,
            "penalty" : penalty,
            "remarks" : remarks
            }
            employeeTimeIn = Employee_attendance(business_date = emp_time_in['business_date'],\
                                                    employee_id = emp_time_in['employee_id'],\
                                                    time_in = emp_time_in['time_in'],\
                                                    employee_status_id = emp_time_in['employee_status_id'],\
                                                    penalty = emp_time_in['penalty'],\
                                                    remarks = emp_time_in['remarks']
                                                )
            db.session.add(employeeTimeIn)
            db.session.commit()
            return message
# TO DO ADD TIME IN / TIME OUT WITH RESTDAY VALIDATION