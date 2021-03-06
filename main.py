#Importing Modules:
import psycopg2, logging
from flask import Flask, request
from flask_restful import Api
from sqlalchemy import Column, String, Integer,Date,BOOLEAN,and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

#Created Application:
app = Flask(__name__)
api = Api(app)

#Created a base class for mapping database objects:
Base  = declarative_base()

#Constructed database URL to access database:
database_url= "postgres://fiquqviuhjqkdc:3a9d1f46254ec48ef17b406fd1be83e299335be850d3a07ef944678aaa25d3f8@ec2-3-215-40-176.compute-1.amazonaws.com:5432/d4upal71s559o1"

#disable sqlalchemy pool using nullpool as by default postgress has its own pool
engine = create_engine(database_url,echo=True, poolclass=NullPool)

#Create connection object:
conn = engine.connect()

#Create SQL Alchemy model
class customerdata(Base):
    __tablename__ = 'customerdata'
    CustomerName =Column("customername",String)
    Gender =Column("gender",String)
    Age =Column("age",Integer)
    Occupation =Column("occupation",String)
    MobileNo =Column("mobileno",Integer,primary_key=True)
    Email =Column("email",String)
    VechicleModel =Column("vechiclemodel",String)
    CustomerState =Column("customerstate",String)
    CustomerDistrict =Column("customerdistrict",String)
    CustomerCity =Column("customercity",String)
    CustomerExistingVehicle =Column("customerexistingvehicle",String)
    DealerState =Column("dealerstate",String)
    DealerTown =Column("dealertown",String)
    DealerName =Column("dealername", String)
    BriefAboutEnquiry =Column("briefaboutenquiry", String)
    ExpectedDateofPurchase =Column("expecteddateofpurchase", Date)
    IntendedUsage =Column("intendedusage", String)
    Senttodealer = Column("senttodealer", BOOLEAN)
    DealerCode = Column("dealercode", String)
    Comments = Column("commentss", String)
    Startdate = Column("startdate", Date)
    Enddate = Column("enddate", Date)
    Productenquerycount = Column("productenquerycount", Integer)
    Productpurchasedcount = Column("productpurchasedcount", Integer)
    Productbuystatus = Column("productbuystatus", String)

#create session class
Session = sessionmaker(bind=engine)

#configure log-level:- available log levels are : INFO, WARNING, DEBUG, ERROR, CRITICAL.
logging.basicConfig(level="DEBUG")

# Post Method - Post the lead info
@app.route('/postleadinfo', methods=['POST'])
def home_post():
    session = Session()
    request_body = request.get_json(force=True)
    for index,item in enumerate(request_body):
        record = customerdata(CustomerName = item["customername"],
                                     Gender = item["gender"],
                                     Age = item["age"],
                                     Occupation =item["occupation"],
				                     MobileNo = item["mobileno"],
                                     Email = item["email"],
                                     VechicleModel =item["vechiclemodel"],
				                     CustomerState = item["customerstate"],
                                     CustomerDistrict = item["customerdistrict"],
                                     CustomerCity =item["customercity"],
				                     CustomerExistingVehicle = item["customerexistingvehicle"],
                                     DealerState = item["dealerstate"],
                                     DealerTown =item["dealertown"],
                                     DealerName = item["dealername"],
                                     BriefAboutEnquiry = item["briefaboutenquiry"],
                                     ExpectedDateofPurchase =item["expecteddateofpurchase"],
				                     IntendedUsage = item["intendedusage"],
                                     Senttodealer = item["senttodealer"],
                                     DealerCode =item["dealercode"],
                                     Comments = item["commentss"],
                                     Startdate = item["startdate"],
                                     Enddate = item["enddate"],
				                     Productenquerycount = item["productenquerycount"],
                                     Productpurchasedcount = item["productpurchasedcount"],
                                     Productbuystatus =item["productbuystatus"])
        session.add_all([record])
    session.commit()
    return ("data inserted in PersonalInfo table successfully")

# Get Method - Retrieves all lead info
@app.route('/allleadinfo', methods=['GET'])
def home_get():
    session = Session()     # creates a database session objects
    try:
        result = session.query(customerdata).all()
        result = [item.__dict__ for item in result]
        for item in result:
            item.pop("_sa_instance_state")
        print(result)
        logging.debug("Lead Info Is {}: ".format(result))
        return str(result)
    finally:
        session.close()

# Get Method - Retrieves single lead record
@app.route('/singleleadinfo', methods=['GET'])
def home_get1():
    session = Session()
    cust_name = request.args.get("customername")
    try:
        logging.info("Get function will return lead info based on your query")
        result = session.query(customerdata).filter(customerdata.CustomerName == cust_name).all()
        result = [item.__dict__ for item in result]
        for item in result:
            item.pop("_sa_instance_state")
            logging.debug("Your lead recored is: {}". format(result))
            return str(result)
    except Exception as err:
        logging.error("Error Occured: {}".format(err))
    finally:
        session.close()

#Put Method - Update the single field of lead
@app.route('/updateleadinfo', methods=['PUT'])
def home_put():
    session = Session()
    logging.info("This function will update single field of a lead")
    print("parameter is {}". format(request.args))
    Mobile_Number = request.args.get("mobileno")
    request_body = request.get_json(force=True)
    try:
        result = session.query(customerdata).filter(customerdata.Senttodealer == "True",
                                                           customerdata.MobileNo == Mobile_Number)\
        .update({customerdata.Comments : request_body[0]["commentss"]})

        session.commit()
        logging.info("update status: 0 - update unsuccessful, 1 - update successful")
        logging.debug("Your updated lead record status is: {}".format(result))
        logging.warning("Verify update lead status in database")
        return str(result)
    finally:
        session.close()

#Update single with PATCH method
@app.route('/updatesinglefield', methods=['PATCH'])
def home_patch():
    session = Session()
    logging.info("This function will update single field of a lead")
    print("parameter is {}". format(request.args))
    Mobile_Number = request.args.get("mobileno")
    request_body = request.get_json(force=True)
    try:
        result = session.query(customerdata).filter(customerdata.Senttodealer == "True",
                                                           customerdata.MobileNo == Mobile_Number)\
        .update({customerdata.Comments : request_body[0]["commentss"]})

        session.commit()
        logging.info("update status: 0 - update unsuccessful, 1 - update successful")
        logging.debug("Your updated lead record status is: {}".format(result))
        logging.warning("Verify update lead status in database")
        return str(result)
    finally:
        session.close()

# Delete Method - Deletes particular lead info from database
@app.route('/delsinglerecord',methods = ['DELETE'])
def home_del():
    session = Session()
    Mobile_Number = request.args.get("mobileno")
    try:
        result = session.query(customerdata).filter(customerdata.MobileNo == Mobile_Number).delete()
        session.commit()
        logging.info("update status: 0 - update unsuccessful, 1 - update successful")
        logging.debug("Deleted lead record status is: {}".format(result))
        logging.warning("Your data removed from database")
        return str(result)
    finally:
        session.close()

if __name__ == "__main__":
    app.run(debug=True)