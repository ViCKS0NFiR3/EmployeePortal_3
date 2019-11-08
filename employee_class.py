from flask_sqlalchemy import SQLAlchemy
from model import db,Employees

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
        

# TO DO ADD TIME IN / TIME OUT WITH RESTDAY VALIDATION