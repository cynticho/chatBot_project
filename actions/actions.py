# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import json
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import os


def get_domaines_accessibles_par_bac(dataset, bac_type: str) -> List[str]:
    bac_type = bac_type.upper().strip()
    domaines = set()
    for filiere in dataset["filiere"]:
        if bac_type in filiere["conditionAdmission"].upper():
            domaines.update(filiere.get("domaines", []))
    return sorted(domaines)


def get_filieres_accessibles_par_bac(dataset, bacType: str):
    bacType_upper = bacType.upper()
    filieres_accessibles = []
    for filiere in dataset.get("filiere", []):
        conditions = filiere["conditionAdmission"].upper()
        if bacType_upper in conditions:
            filieres_accessibles.append(filiere)
    return filieres_accessibles


current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, '../data/formation.json')
image_path = os.path.join(current_dir, '../data/path/paths.json')
inscription_path= os.path.join(current_dir, '../data/inscription/procedure_inscription.json')
dossier_path= os.path.join(current_dir, '../data/inscription/formulaire/form.json')

# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


# chargement des datasets
with open(data_path, 'r', encoding='utf-8') as f:
    dataset = json.load(f)

with open(image_path, "r", encoding="utf-8") as f:
    data = json.load(f)

with open(inscription_path, "r", encoding="utf-8") as f:
    inscription_data = json.load(f)

with open(dossier_path, "r", encoding="utf-8") as f:
    dossier_data = json.load(f)








class ActionInscription(Action):

    def name(self) -> Text:
        return "action_inscription"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        inscription = tracker.get_slot("inscription")

        if not inscription:
            dispatcher.utter_message(response="utter_fallback")
            return []
        else:
            dispatcher.utter_message(text=f"Parfait, pour se pre-inscrire, vous devez:")
            dispatcher.utter_message(text=f"📚 Université : {inscription_data['universite']}")
            dispatcher.utter_message(text=f"🌐 Plateforme : {inscription_data['plateforme']}")
            for etape in inscription_data["processus"]:
                message = f"🟢 {etape['etape']} - {etape['titre']}/n{etape['description']}"
                dispatcher.utter_message(text=message)

            dispatcher.utter_message(text=f"📌 Remarque : {inscription_data['remarque_finale']}")
            dispatcher.utter_message(response="utter_help")
            return []











class ActionDossier(Action):

    def name(self) -> Text:
        return "action_dossier"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dossier = tracker.get_slot("dossier")
        filiere = tracker.get_slot("filiere")

        if not dossier:
            # dispatcher.utter_message(response="utter_fallback")
            return []
        else:
            match = next((item for item in dossier_data if item["filiere"].lower() == filiere.lower()), None)

            if not match:
                dispatcher.utter_message(text=f"❌ La filière '{filiere}' n'existe pas dans mes données.")
                return []

            message = f"📘 **Filière : {filiere.upper()}**/n"
            message += f"**Statut :** {match['statut'].capitalize()}/n/n"

            if match["statut"] == "accessible":
                message += "**📄 Conditions d'inscription :**/n"
                for i, cond in enumerate(match["conditions"], 1):
                    message += f"{i}. {cond}/n"
            else:
                message += f"**Conditions :** {match['conditions']}/n"
                message += f"**Motif :** {match['motif']}/n"
                message += f"**Prochaine mise à jour :** {match['prochaine_mise_a_jour_estimee']}/n"

                message += f"/n🔗 Source : {match['source']}"

                dispatcher.utter_message(text=message)


        dispatcher.utter_message(text=f"Parfait, voici la constitution du dossier")
        dispatcher.utter_message(response="utter_help")
        return []












class ActionDefaultFallback(Action):

    def name(self) -> Text:
        return "action_default_fallback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(response="utter_fallback")

        return []








class ActionFillForm(Action):

    def name(self) -> Text:
        return "action_fill_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        form = tracker.get_slot("form")

        if not form:
            dispatcher.utter_message(response="utter_fallback")
            return []

        dispatcher.utter_message(text="✅ Parfait, voici comment remplir le formulaire étape par étape :")

        # Base URL des images
        base_url = "file:///C:/Users/Lomofouet/Desktop/dicap-rasa/rasa/chatbot/data/inscription/formulaire/"

        # Liste des étapes
        items = dossier_data.get("form", [])

        for i, item in enumerate(items):
            title = item["name"].capitalize()
            image_name = item["image"]
            image_url = f"{base_url}{image_name}.png"

            dispatcher.utter_message(text=f"📝 Étape {i+1} : {title}")
            dispatcher.utter_message(image=image_url)

        dispatcher.utter_message(text="✅ Une fois toutes les étapes complétées, vous pouvez finaliser l'inscription.")
        dispatcher.utter_message(response="utter_help")

        return []










class ActionGivenBac(Action):
    def name(self) -> Text:
        return "action_given_bac"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        bac = tracker.get_slot("bac")
        bacType = tracker.get_slot("bacType")

        if not bac or not bacType:
            dispatcher.utter_message(response="utter_ask_bac")
            return []

        bacType_upper = bacType.upper()
        filieres_accessibles = get_filieres_accessibles_par_bac(dataset, bacType)

        if not filieres_accessibles:
            dispatcher.utter_message(text=f"❌ Aucune filière trouvée pour le bac {bacType_upper}. ❌")
            dispatcher.utter_message(response="utter_help")
            return []
        else:
            dispatcher.utter_message(text=f"🎓 Voici les filières accessibles avec le bac {bacType_upper} :")

            for filiere in filieres_accessibles:
                nom = filiere.get("nom", "Nom inconnu")
                description = filiere.get("description", "Aucune description disponible.")
                debouches = filiere.get("debouches", [])

                debouches_formattes = "/n".join([f"- ✅ {d}" for d in debouches])

                message = (
                    f"/n📘 *{nom}*/n/n"
                    f"**Description** :/n{description}/n/n"
                    f"💼 **Débouchés** :/n{debouches_formattes}"
                )

                dispatcher.utter_message(text=message)

            dispatcher.utter_message(response="utter_help")
            return []

        # if not bac:
        #     dispatcher.utter_message(response="utter_ask_bac")
        #     return []
        # else:
        #     dispatcher.utter_message(text=f"action pour le {bac} {bacType}.")
        #     dispatcher.utter_message(response="utter_help")
        #     return []

        # options = BAC_OPTIONS.get(bac.upper())
        # if options:
        #     dispatcher.utter_message(text=f"Avec un bac {bac.upper()}, vous pouvez envisager les formations suivantes :")
        #     for opt in options:
        #         dispatcher.utter_message(text=f"- {opt}")
        # else:
        #     dispatcher.utter_message(text=f"Désolé, je ne connais pas encore d’options pour le bac {bac}.")
        # return []












class ActionSchool(Action):

    def name(self) -> Text:
        return "action_school"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        school = tracker.get_slot("school")

        if not school:
            dispatcher.utter_message(response="utter_greet")
            return []
        else:
            dispatcher.utter_message(response="utter_school")
            dispatcher.utter_message(response="utter_help")
            return []











class ActionTrain(Action):

    def name(self) -> Text:
        return "action_train"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        train = tracker.get_slot("train")
        bac = tracker.get_slot("bac")
        bacType = tracker.get_slot("bacType")

        if not train:
            dispatcher.utter_message(response="utter_greet_local")
            return []
        else:
            dispatcher.utter_message(response="utter_train")
            dispatcher.utter_message(response="utter_help")
            return []














class ActionFiliere(Action):

    def name(self) -> Text:
        return "action_filiere"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        bac = tracker.get_slot("bac")
        bacType = tracker.get_slot("bacType")

        if not bac or not bacType:
            dispatcher.utter_message(response="utter_ask_bac")
            return []

        bacType_upper = bacType.upper()

        filieres_accessibles = []
        for filiere in dataset.get("filiere", []):
            conditions = filiere["conditionAdmission"].upper()
            if bacType_upper in conditions:
                filieres_accessibles.append(filiere)

        if not filieres_accessibles:
            # utter_no_filiere
            dispatcher.utter_message(text=f"❌ Désolé, Aucune filière trouvée pour le bac {bacType_upper}. ❌")
        else:
            dispatcher.utter_message(text=f"🎓 Voici les filières accessibles avec le bac {bacType_upper} :")

            for filiere in filieres_accessibles:
                nom = filiere.get("nom", "Nom inconnu")
                description = filiere.get("description", "Aucune description disponible.")
                debouches = filiere.get("debouches", [])

                debouches_formattes = "/n".join([f"- ✅ {d}" for d in debouches])

                message = (
                    f"/n📘 *{nom}*/n/n"
                    f"**Description** :/n{description}/n/n"
                    f"💼 **Débouchés** :/n{debouches_formattes}"
                )

                dispatcher.utter_message(text=message)

            dispatcher.utter_message(response="utter_help")

        return []








class ActionDomain(Action):

    def name(self) -> Text:
        return "action_domain"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        bacType = tracker.get_slot("bacType")

        if not bacType:
            dispatcher.utter_message(response="utter_ask_bac")
            return []

        bacType_upper = bacType.strip().upper()
        domaines = set()

        for filiere in dataset["filiere"]:
            conditions = filiere["conditionAdmission"].upper()
            if bacType_upper in conditions:
                domaines.update(filiere.get("domaines", []))

        if not domaines:
            # utter_no_domain
            dispatcher.utter_message(text=f"❌ Aucun domaine trouvé pour le bac {bacType}. ❌")
            dispatcher.utter_message(response="utter_help")
            return []
        else:
            domaines_list = "/n/n".join(f"✅ {domaine}" for domaine in sorted(domaines))
            dispatcher.utter_message(text=f"📚 Voici les domaines accessibles avec le bac {bacType} :/n/n{domaines_list}")
            dispatcher.utter_message(response="utter_help")
            return []










# 🔁
def est_filiere_accessible(bac: str, terme: str) -> str:
    bac_upper = bac.upper()
    terme_lower = terme.lower()
    resultats = []

    for filiere in dataset["filiere"]:
        # Recherche dans le nom, les domaines et les débouchés
        nom_match = terme_lower in filiere["nom"].lower()
        domaine_match = any(terme_lower in domaine.lower() for domaine in filiere["domaines"])
        debouche_match = any(terme_lower in debouche.lower() for debouche in filiere["debouches"])

        if nom_match or domaine_match or debouche_match:
            conditions = filiere["conditionAdmission"].upper()
            if bac_upper in conditions:
                resultats.append(f"✅ Oui, vous pouvez bien faire *{terme}* avec un bac {bac}.")
            else:
                resultats.append(f"❌ Non, *{terme}* n'est pas accessible avec un bac {bac}. ❌")

    if resultats:
        return "/n".join(resultats)
    else:
        return f"⚠️ Oops, Aucun profil ne correspondant à **{terme}**. ⚠️"


class ActionBacFiliere(Action):

    # 🔧
    def name(self) -> Text:
        return "action_bac_filiere"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        bac = tracker.get_slot("bac")
        bacType = tracker.get_slot("bacType")
        work = tracker.get_slot("work")

        if not work:
            # utter_ask_filiere
            # dispatcher.utter_message(response="utter_ask_filiere")
            # dispatcher.utter_message(text=" ⚠️ vous parlez de quoi plus precisement ? ⚠️")
            return []

        if not bacType:
            dispatcher.utter_message(response="utter_ask_bac")
            return []

        dispatcher.utter_message(f" vous voulez savoir si le {bac} {bacType} permet d'acceder : **{work}**")
        reponse = est_filiere_accessible(bacType, work)
        dispatcher.utter_message(text=reponse)
        dispatcher.utter_message(response="utter_help")

        return []







class ActionAskInfo(Action):

    # 🔧 Action Rasa
    def name(self) -> Text:
        return "action_ask_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        info = tracker.get_slot("info")

        if not info:
            # utter_ask_faculty
            dispatcher.utter_message(text=" ⚠️ désolé, je n'ai pas bien saisi, pouvez vous rapeller la faculté ? ⚠️")
            return []

        url = {
            "flsh": "file:///C:/Users/Lomofouet/Desktop/dicap-rasa/rasa/chatbot/data/pdfs_training/flsh.pdf",
            "fseg": "file:///C:/Users/Lomofouet/Desktop/dicap-rasa/rasa/chatbot/data/pdfs_training/fseg.pdf",
            "fsjp": "file:///C:/Users/Lomofouet/Desktop/dicap-rasa/rasa/chatbot/data/pdfs_training/fsjp.pdf",
            "fs":   "file:///C:/Users/Lomofouet/Desktop/dicap-rasa/rasa/chatbot/data/pdfs_training/fs.pdf",
            "fasa": "file:///C:/Users/Lomofouet/Desktop/dicap-rasa/rasa/chatbot/data/pdfs_training/fasa.pdf",
            "iutfv":"file:///C:/Users/Lomofouet/Desktop/dicap-rasa/rasa/chatbot/data/pdfs_training/iutfv.pdf",
            "iba":  "file:///C:/Users/Lomofouet/Desktop/dicap-rasa/rasa/chatbot/data/pdfs_training/ibaf.pdf",
            "fmsp": "file:///C:/Users/Lomofouet/Desktop/dicap-rasa/rasa/chatbot/data/pdfs_training/fmsp.pdf",
        }

        info = info.lower()
        lien = url.get(info)

        if lien:
            dispatcher.utter_message(text=f"vous recherchez probablement des infos sur {info}")
            dispatcher.utter_message(text=f"✅ Voici les infos demandées ci dessous ✅")
            resources = {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": [
                        {
                            "title": f"📁{info}",
                            "subtitle": f"{info} description",
                            "image_url": "./logo dschang.PNG",
                            "buttons": [{
                                "title": "📁Telecharger",
                                "url": f"{lien}",
                                "type": "web_url"
                            },
                                {
                                    "title": "un autre choix",
                                    "type": "postback",
                                    "payload": "/affirm"
                                }
                            ]
                        }
                    ]
                }
            }
            dispatcher.utter_message(attachment=resources)
            dispatcher.utter_message(response="utter_help")
            return []
        else:
            # utter_no_info
            dispatcher.utter_message(text=f"❌ Désolé, je n’ai pas trouvé d'info pour {info}. ❌")
            dispatcher.utter_message(response="utter_help")
            return []








# Fonction de recherche stricte
def search_strict(term, data):
    term = term.lower().strip()
    for entity in data["myEntities"]:
        prefix = entity["name"].split(",")[0].strip().lower()
        if term == prefix:
            return entity
    return None  # Aucun résultat trouvé


class ActionPlace(Action):
    def name(self) -> str:
        return "action_place"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Récupérer la place depuis un slot ou une entité
        # place = tracker.get_slot("place")
        place = tracker.get_slot("destination")
        origine = tracker.get_slot("origine")
        work = tracker.get_slot("work")
        if not place:
            dispatcher.utter_message(text="⚠️ Désolé, Je n'ai pas compris la place que vous cherchez ⚠️")
            return []

        # Recherche de la localisation
        result = search_strict(place, data)

        if not result:
            # utter_no_place
            dispatcher.utter_message(text=f"❌ Aucune localisation pour « {place} » n'a été trouvée. ❌")
            dispatcher.utter_message(response="utter_help")
            return []

        # base_url ="file:D:/rasa/chatbot/data/path/images"
        base_url = "file:///C:/Users/Lomofouet/Desktop/dicap-rasa/rasa/chatbot/data/path/images/"
        # base_url = "file:///C:/Users/Lomofouet/Desktop/dicap-rasa/rasa/chatbot/data/path/images/"
        steps = result["steps"]

        # Créer les éléments du carousel
        elements = []
        for i, step in enumerate(steps):
            image_url = f"{base_url}{step}.jpg"
            elements.append({
                # "title": f"Étape {i + 1}",
                "title": result["name"],
                "image_url": image_url,
                "subtitle": result["description"],
                "buttons": [
                    {
                        "type": "postback",
                        "title": "Suivant"
                    }
                ]
            })
        name= result["name"]
        # Envoyer le carousel de localisation ✅
        dispatcher.utter_message(text=f"✅ parfait, vous chercher {name}")
        dispatcher.utter_message(text=f"✅ voici comment procéder ✅")
        dispatcher.utter_message(attachment={
            "type": "template",
            "payload": {
                "template_type": "generic",
                "elements": elements
            }
        })

        return []