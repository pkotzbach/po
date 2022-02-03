from main.classes.Hospitation import Hospitation


def checkHospitation(hosp: Hospitation):
    isWzhz = False
    for comTeacher in hosp.commission:
        if comTeacher == hosp.teacher:
            return {"code": 1, "data": "Nauczyciel hospitowany nie moze byc w komisji"}
        if comTeacher.wzhz == True:
            isWzhz = True

    if isWzhz == False:
        return {
            "code": 1,
            "data": "Komisja musi zawierac czlonka WZHZ",
        }

    if len(set(hosp.commission)) != len(hosp.commission):
        return {
            "code": 1,
            "data": "W komisji jest co najmniej dwoch tych samych nauczycieli",
        }

    if hosp.teacher == None or hosp.schedule == None or hosp.commission == None:
        return {
            "code": 1,
            "data": "Wszystkie pola musza byc uzupelnione",
        }

    if len(hosp.commission) < 2:
        return {
            "code": 1,
            "data": "W komisji musi byc co najmniej dwoch nauczycieli",
        }

    if hosp.clas not in hosp.teacher.classes:
        return {
            "code": 1,
            "data": "Nauczyciel nie uczy tego przedmiotu",
        }

    return {"code": 0, "data": ""}
