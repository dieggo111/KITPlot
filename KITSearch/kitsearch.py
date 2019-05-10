#pylint: disable=C0103
"""KITSearch module"""
# import sys
# import os
import logging
import yaml
import sqlalchemy
from sqlalchemy.orm import sessionmaker
try:
    from db_map import db_info, db_probe, db_probe_data
    from db_map import db_alibava, db_annealing, db_irradiation
except ImportError:
    from .db_map import db_info, db_probe, db_probe_data
    from .db_map import db_alibava, db_annealing, db_irradiation

class KITSearch(object):
    """Module for searching data in ETP Measurement DB.
    Primary keys:
        - db_info : ID
        - db_probe : probeid
        - db_probe_data : probe_uid
        - db_alibava : alibava_uid
        - db_irradiation : uirrad_id
        - db_annealing : annealing_id
    """
    def __init__(self, cred=None):
        """Initializes class, loads credentials, creates engine and DB session,
        creates dict for calling table objects with name.

        Misc:
                cred = {"host"      : "...",
                        "database"  : "...",
                        "user"      : "...",
                        "passwd"    : "..."}
        """
        self.log = logging.getLogger(__class__.__name__)
        self.log.setLevel(logging.DEBUG)
        if self.log.hasHandlers() is False:
            format_string = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
            formatter = logging.Formatter(format_string)
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.log.addHandler(console_handler)

        if isinstance(cred, str):
            with open(cred, "r") as crx:
                dic = yaml.load(crx)
            cred = list(dic.values())[0]

        self.engine = sqlalchemy.create_engine("mysql+mysqlconnector://" +
                                               cred["user"] + ":" + cred["passwd"] +
                                               "@" + cred["host"] + ":" +
                                               "3306" + "/" + cred["database"])

        session = sessionmaker(bind=self.engine)
        self.session = session()

        self.db_table = {"db_info" : db_info,
                         "db_probe" : db_probe,
                         "db_probe_data" : db_probe_data,
                         "db_alibava" : db_alibava,
                         "db_annealing" : db_annealing,
                         "db_irradiation" : db_irradiation}

    def search_table(self, table, **kwargs):
        """Basic search operation: search for key-value DB table. You can add
        '%' in a kwarg for a wildcard search. One wildcard allowed at a time."""
        wildcard = {}
        # check vor wildcards in kwargs
        for key, val in kwargs.items():
            try:
                if "%" in val:
                    wildcard[key] = val.replace("%", "")
            except TypeError:
                pass
        if len(wildcard) > 1:
            self.log.warning("Only 1 wildcard per search allowed!")
            return None
        # use wildcard + rest of kwargs to filter DB data
        if wildcard != {}:
            wc_key = list(wildcard.keys())[0]
            kwargs.pop(wc_key)
            data = self.session.query(self.db_table[table]).filter(\
                    getattr(self.db_table[table], wc_key).contains(\
                    wildcard[wc_key])).filter_by(**kwargs)
            return data
        data = self.session.query(self.db_table[table]).filter_by(**kwargs)
        return data

    def probe_search(self, name, project, pid_list=None):
        """Combined search operation: searche data for specific name
        and project"""
        dic = {}
        PID = []
        ID = []
        for row in self.search_table("db_info", name=name, project=project):
            ID.append(row.ID)
        if ID == []:
            return dic
        for item in ID:
            for row in self.search_table("db_probe", ID=item):
                if pid_list is None:
                    PID.append(row.probeid)
                elif row.probeid in pid_list:
                    PID.append(row.probeid)
            for run in PID:
                sub = self.probe_search_data(run)
                pid = sub.pop("PID")
                sub["PID"] = pid
                sub["ID"] = item
                # fluence, pt = self.get_fluence(item, sub["date"])
                # sub.update({"fluence" : fluence,
                #             "particletype"  : pt})

                dic.update({pid : sub})
        return dic

    def probe_search_data(self, pid):
        """Searches measurement data of given probeid"""
        dic = {}
        dataX = []
        dataY = []
        dataZ = []
        temp = []
        rh = []
        err = []
        time = []
        bias_cur = []

        for row in self.search_table("db_probe_data", probeid=pid):
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

        for row in self.search_table("db_probe", probeid=pid):
            dic.update({"paraX"     : row.paraX,
                        "paraY"     : row.paraY,
                        "t0"        : row.temperature,
                        "h0"        : row.RH,
                        "PID"       : row.probeid,
                        "ID"        : row.ID,
                        "date"      : row.date,
                        "flag"      : row.flag})

        for row in self.search_table("db_info", ID=dic["ID"]):
            dic.update({"name"      : row.name,
                        "project"   : row.project})

        fluence, pt = self.get_fluence(dic["ID"], dic["date"])
        dic.update({"annealing"     : self.get_annealing(dic["ID"], dic["date"])})
        dic.update({"fluence"       : fluence,
                    "particletype"  : pt})
        return dic

    def ali_search_for_run(self, run):
        """Combined search operation: search for run data according to given
        run number"""
        dic = {}
        for row in self.search_table("db_alibava", run=run):
            dic.update({"voltage"       : row.voltage,
                        "e_sig"         : row.electron_sig,
                        "e_sig_err"     : row.signal_e_err,
                        "gain"          : row.gain,
                        "seed"          : row.SeedSigENC_MPV,
                        "seed_err"      : row.SeedSigENC_MPV_err,
                        "seedADC"       : row.SeedSig_MPV,
                        "seedADC_err"   : row.SeedSig_MPV_err})
            ID = row.ID
            # date = row.date
            a_id = row.annealing_id
            i_id = row.irradiation_id
            dic.update({"annealing" : self.get_annealing(a_id)})
            fluence, particle = self.get_fluence(i_id)
            dic.update({"fluence"       : fluence,
                        "particletype"  : particle})


        for row in self.search_table("db_info", ID=ID):
            dic.update({"name"      : row.name,
                        "project"   : row.project})
        return dic

    def ali_search_data(self, name, project, search_para, search_val):
        """Combined search operation: search for measurement data according to
        item name and project which satisfie certain frame conditions

        Args:
            - search_para (str): 'Voltage' or 'Annealing'
            - search_val (float): voltage or annealing value you are
                                  looking for
        """
        dic = {}
        ID = []
        for row in self.search_table("db_info", name=name, project=project):
            if row.project == project:
                ID.append(row.ID)
        for item in ID:
            for row in self.search_table("db_alibava", ID=item):
                sub = {}
                if search_para == "Voltage" and (search_val*0.99) \
                        < abs(row.voltage) < (search_val*1.01):
                    sub.update({"voltage"       : row.voltage})
                    sub.update({"date"          : row.date,
                                "e_sig"         : row.electron_sig,
                                "e_sig_err"     : row.signal_e_err,
                                "gain"          : row.gain,
                                "flag"          : row.flag,
                                # wrong entries in db
                                # "seed_e"        : row.SeedSigENC_MPV,
                                # "seed_e_err"    : row.SeedSigENC_MPV_err,
                                "seed"          : row.SeedSig_MPV,
                                "seed_err"      : row.SeedSig_MPV_err,
                                "annealing"     : self.get_annealing(row.annealing_id),
                                "name"          : name,
                                "ID"           : row.ID,
                                "project"       : project})
                    fluence, particle = self.get_fluence(row.irradiation_id)
                    sub.update({"fluence"       : fluence,
                                "particletype"  : particle})
                    dic.update({row.run : sub})
                if search_para == "Annealing":
                    tot_an = self.get_annealing(row.annealing_id)
                    if (search_val*0.9) <= abs(tot_an) <= (search_val*1.1):
                        sub.update({"voltage"       : row.voltage})
                        sub.update({"date"          : row.date,
                                    "e_sig"         : row.electron_sig,
                                    "e_sig_err"     : row.signal_e_err,
                                    "gain"          : row.gain,
                                    # wrong entries in db
                                    # "seed_e"        : row.SeedSigENC_MPV,
                                    # "seed_e_err"    : row.SeedSigENC_MPV_err,
                                    "seed"          : row.SeedSig_MPV,
                                    "seed_err"      : row.SeedSig_MPV_err,
                                    "annealing"     : self.get_annealing(row.annealing_id),
                                    "name"          : name,
                                    "ID"           : row.ID,
                                    "project"       : project})

                        fluence, particle = self.get_fluence(row.irradiation_id)
                        sub.update({"fluence"       : fluence,
                                    "particletype"  : particle})
                        dic.update({row.run : sub})
        return dic

    def get_annealing(self, eyedee, date=None):
        """Get annealing information"""
        if eyedee is None:
            return 0
        if date is None:
            for row in self.search_table("db_annealing", annealing_id=eyedee):
                if row.sum is None:
                    return 0
                return round(row.sum)
        else:
            annealing = 0
            for row in self.search_table("db_annealing", ID=eyedee):
                if date > row.date:
                    annealing += row.equiv
            return round(annealing)

    def get_fluence(self, eyedee, date=None):
        """Get information about irradiation"""
        if eyedee is None:
            return (0, "")
        elif date is None:
            for row in self.search_table("db_irradiation", uirrad_id=eyedee):
                return (row.F_sum, row.particles)
        else:
            fluence = 0
            pt = []
            for row in self.search_table("db_irradiation", ID=eyedee):
                if date.date() > row.date:
                    fluence += row.F_n_cm2
                    pt.append(row.particletype)
            return (fluence, pt)

    def getSession(self):
        """Return session object"""
        return self.session


if __name__ == '__main__':


    S = KITSearch("C:\\Users\\Marius\\KITScripts\\db.cfg")

    # for row in S.search_table("db_info", {"name":"KIT_Test_07", "project":"HPK_2S_II"}):
    # for line in S.search_table("db_info", name="%"):
    #     print(line.project)
    # for line in S.search_table("db_info", name="FBK_W%", project="CalibrationDiodes"):
        # print(line.ID, line.name)
    # for sec in S.probe_search(name="FBK_W%", project="CalibrationDiodes"):
    #     print(sec)
