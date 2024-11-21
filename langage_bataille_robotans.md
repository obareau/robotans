# Langage de Bataille Robotans

## Description

Ce projet propose une collection de programmes interactifs pour la conversion et le cryptage de textes en différents langages fictifs inspirés de l'univers Robotans. Il inclut des transformations simples, des cryptages renforcés, et des méthodes avancées de codage.

### Fonctionnalités principales

1. **Langage de Bataille Robotans V1** :
   - Applique un décalage de César de 3 sur les lettres.
   - Regroupe les lettres en blocs de 5.
   - Exemple :
     - **Entrée** : `Les Robotans préparent la bataille.`
     - **Sortie** : `OHV URER WDQV SUH SDUH QWOD EDWW DILO H`

2. **Langage de Bataille Robotans V2 (Cryptage renforcé)** :
   - Applique un décalage de César de 3.
   - Inverse le texte pour un brouillage supplémentaire.
   - Regroupe les lettres en blocs de 5.
   - Exemple :
     - **Entrée** : `Les Robotans préparent la bataille.`
     - **Sortie** : `H LIO D WTDE LQWD ERA DS ERU HVH`

3. **Langage de Bataille Robotans V3 (Cryptage musical avec octaves)** :
   - Convertit chaque lettre en une note musicale avec une octave.
   - Regroupe les mots par blocs de 4 avec une majuscule au début.
   - Exemple :
     - **Entrée** : `Les Robotans préparent la bataille.`
     - **Sortie** : `G2 F2 A2 / C2 F3 C2 / D3 G3 C2 / G3 D3 A4`

4. **Ordre Flash** :
   - Supprime les espaces.
   - Factorise les lettres consécutives (par ex., `hello` devient `he2lo`).
   - Encadre le message avec `!`.
   - Exemple :
     - **Entrée** : `hello world`
     - **Sortie** : `!he2lo2world!`

---