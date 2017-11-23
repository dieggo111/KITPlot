import sys,os
import sqlalchemy
import mysql.connector
try:
    from .db_map import db_probe_data, db_probe, db_info, db_alibava, db_annealing
except:
    from db_map import db_probe_data, db_probe, db_info, db_alibava, db_annealing
from sqlalchemy.orm import sessionmaker


class KITSearch(object):

    def __init__(self,cred):
        self.engine = sqlalchemy.create_engine("mysql+mysqlconnector://" +
                                          cred["user"] + ":" + cred["passwd"] +
                                          "@" + cred["host"] + ":" +
                                          "3306" + "/" + cred["database"])

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def search_in_info(self,val,para=None):
        if para == "name" or para == None:
            data = self.session.query(db_info).filter_by(name=val)
        elif para == "ID":
            data = self.session.query(db_info).filter_by(ID=val)
        return data

    def search_in_probe(self,val,para=None):
        if para == "PID" or para == None:
            data = self.session.query(db_probe).filter_by(probeid=val)
        elif para == "UID":
            data = self.session.query(db_probe).filter_by(ID=val)
        return data

    def search_in_probe_data(self,val,para=None):
        if para == "PID" or para == None:
            data = self.session.query(db_probe_data).filter_by(probeid=val)
        return data

    def search_in_alibava(self,val,para=None):
        if para == "run" or para == None:
            data = self.session.query(db_alibava).filter_by(run=val)
        elif para == "UID":
            data = self.session.query(db_alibava).filter_by(alibava_uid=val)
        return data

    def search_in_annealing(self,val,para=None):
        if para == "ID" or para == None:
            data = self.session.query(db_annealing).filter_by(ID=val)
        return data

    def search_for_PID(self,PID):
        dic = {}
        dataX = []
        dataY = []
        dataZ = []
        temp = []
        rh = []
        err = []
        time = []
        bias_cur = []

        for row in self.search_in_probe_data(PID):
            dataX.append(row.datax)
            dataY.append(row.datay)
            dataZ.append(row.dataz)
            temp.append(row.temperature)
            rh.append(row.RH)
            err.append(row.errory)
            time.append(row.time)
            bias_cur.append(row.bias_current)

        dic.update({"dataX"     : dataX,
                    "dataY"     : dataY,
                    "dataZ"     : dataZ,
                    "temp"      : temp,
                    "rh"        : rh,
                    "err"       : err,
                    "time"      : time,
                    "bias_cur"  : bias_cur})

        for column in self.search_in_probe(PID):
            dic.update({"paraX"     : column.paraX,
                        "paraY"     : column.paraY,
                        "t0"        : column.temperature,
                        "h0"        : column.RH})
            ID = column.ID

        for column in self.search_in_info(ID,para="ID"):
            dic.update({"name"      : column.name,
                        "Fp"        : column.F_p_aim_n_cm2,
                        "Fn"        : column.F_n_aim_n_cm2,
                        "project"   : column.project})
        return dic

    def search_for_run(self,nr):
        dic = {}
        for column in self.search_in_alibava(nr):
            dic.update({"voltage"       : column.voltage,
                        "e_sig"         : column.electron_sig,
                        "e_sig_err"     : column.signal_e_err,
                        "gain"          : column.gain,
                        "seed"          : column.SeedSig_MPV,
                        "seed_err"      : column.SeedSig_MPV_err})
            tempID = column.ID
            tempDate = column.date

        for column in self.search_in_annealing(tempID):
            print(column.equiv,column.date)
            print(tempDate>column.date)

        return dic

if __name__ == '__main__':

    db = {"host": "192.168.13.2",
          "port": "3306",
          "database": "sample",
          "user": "abfrage",
          "passwd": "JtjTN9M4WpQr,29t"}
    s = KITSearch(db)

    s.search_for_run(233763)

    # for row in s.search_in_probe_data(35678):
    #     print(row.datax,row.datay)
    #
    # for column in s.search_in_alibava(233561):
    #     print(column.alibava_uid,column.run,column.ID)
    #     ID = column.alibava_uid
    # for column in s.search_in_annealing(ID):
    #     print(column.alibava_uid,column.run,column.ID)
