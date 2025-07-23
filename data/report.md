---
marp: true
theme: default
paginate: true
---

# Exemple de diagramme Mermaid
:metal:

|Variable|Valeur|Description|
|:---|:---:|---:|
|A|1|Entier|
|B|2||

---
title: Node with text
---

---
config:
  flowchart:
    htmlLabels: false
---
```mermaid
graph LR
    A[Bords droits] -->|Lien texte| B(Bords arondis)
    B --> C{Décision}
    C -->|Un| D[Résultat un]
    C -->|Deux| E[Résultat deux]
```
---

```mermaid
flowchart LR
    id1[This is the text in the box]
```


---
```
[params]
  # Ordre du contenu du menu latéral du site (https://gohugo.io/templates/lists/#order-content)
  siteContentOrder = "weight"
  siteContentOrder = "date"
  siteContentOrder = "publishdate"
  siteContentOrder = "expirationdate"
  siteContentOrder = "lastmodifieddate"
  siteContentOrder = "length"
  siteContentOrder = "title"
  siteContentOrder = "linktitle"
```
---
```mermaid
graph LR;
    A[Bords droits] -->|Lien texte| B(Bords arondis)
    B --> C{Décision}
    C -->|Un| D[Résultat un]
    C -->|Deux| E[Résultat deux]
```
---
```mermaid
sequenceDiagram
    participant Alice
    participant Bob
    Alice->>John: Salut John, comment vas-tu?
    loop Vérification
        John->>John: Se bat contre l'hyponcodrie.
    end
    Note right of John: Les pensées rationnelles<br/>prédominent...
    John-->Alice: Super!
    John->Bob: Et toi?
    Bob-->John: Au top!
```

---

```mermaid
gantt
        dateFormat  YYYY-MM-DD
        title Ajout de la fonctionnalité de GANTT à Mermaid
        section Une section
        Tâche complétée            :done,    des1, 2014-01-06,2014-01-08
        Tâche en cours             :active,  des2, 2014-01-09, 3d
        Future tâche               :         des3, after des2, 5d
        Future tâche 2             :         des4, after des3, 5d
        section Tâches critiques
        Tâche complétée dans le chemin critique :crit, done, 2014-01-06,24h
        Implémenter le parser et jison          :crit, done, after des1, 2d
        Créer des tests pour le parser          :crit, active, 3d
        Future tâche dans le chemin critique    :crit, 5d
        Créer des tests pour le renderer        :2d
        Ajout à Mermaid                          :1d
```

---

```mermaid
---
config:
  radar:
    axisScaleFactor: 0.25
    curveTension: 0.1
  theme: base
  themeVariables:
    cScale0: "#FF0000"
    cScale1: "#00FF00"
    cScale2: "#0000FF"
    radar:
      curveOpacity: 0
---
radar-beta
  axis A, B, C, D, E
  curve c1{1,2,3,4,5}
  curve c2{5,4,3,2,1}
  curve c3{3,3,3,3,3}

```
---
```mermaid
gitGraph:
  commit
  branch newbranch
  checkout newbranch
  commit
  commit
  checkout master
  commit
  commit
  merge newbranch
```
---

```mermaid
stateDiagram-v2
  ouvert: Ouvert
  clos: Clos
  fermé: Fermé
  ouvert --> clos
  clos   --> fermé: Lock
  fermé --> clos: Unlock
  clos --> ouvert: Open
```
---

```mermaid
gitGraph
   commit id: "Initial commit, project's initialization "
   branch dicap
   branch marcelle
   branch mhd
   branch asaph
   checkout dicap
   commit id: ""
   commit id: ""
   checkout mhd
   commit id: ""
   commit id: ""
   checkout marcelle
   commit id: ""
   commit id: ""
   checkout asaph
   commit id: ""
   commit id: ""
   checkout dicap
   commit id: ""
   commit id: ""
   merge main

```