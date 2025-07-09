# utils.py
from typing import Any, Text, Dict, List

def get_domaines_accessibles_par_bac(dataset, bac_type: str) -> List[str]:
    bac_type = bac_type.upper().strip()
    domaines = set()
    for filiere in dataset["filiere"]:
        if bac_type in filiere["conditionAdmission"].upper():
            domaines.update(filiere.get("domaines", []))
    return sorted(domaines)




def get_filieres_accessibles_par_bac(dataset, bac_type: str):
    bacType_upper = bacType.upper()
    filieres_accessibles = []
    for filiere in dataset.get("filiere", []):
        conditions = filiere["conditionAdmission"].upper()
        if bacType_upper in conditions:
            filieres_accessibles.append(filiere)
    return sorted(filieres_accessibles)