# Smart Grid IA Afrique

<<Jumeau Numérique Intelligent pour la résilience énergétique et l'effacement de charge en Afrique.>>  
*Projet développé dans le cadre de la Presidential African Youth in AI and Robotics Competition 2026.*



##  Le Contexte & La Problématique
Les réseaux électriques africains subissent de plein fouet les variations climatiques (saisons sèches sévères impactant le niveau des barrages hydrauliques) et une augmentation massive de la demande urbaine. Les délestages classiques non planifiés paralysent l'économie locale et mettent en danger les infrastructures critiques comme les hôpitaux.

## La Solution : Le Jumeau Numérique Propulsé par l'IA
**Smart Grid IA Afrique** résout ce défi grâce à une approche logicielle innovante basée sur le Machine Learning :
1. **Prédiction Télémétrique (ML) :** Un algorithme d'intelligence artificielle (`RandomForestRegressor`) analyse en temps réel le niveau des réservoirs hydrauliques et l'impact thermique de la température ambiante pour prédire précisément la puissance disponible sur le réseau.
2. **Automate Virtuel Émulé (Jumeau Numérique) :** Le système pilote une réplique virtuelle en temps réel des armoires de distribution de terrain (Écran LCD, voyants de crise, basculeurs de puissance).
3. **Effacement de Charge Intelligent (*Demand Response*) :** En cas de déficit de production, l'IA isole et protège les infrastructures vitales (Hôpitaux maintenus à 100% de priorité) tout en appliquant un bridage dynamique sur les ménages et un effacement total programmé sur les industries lourdes pour empêcher l'effondrement du réseau (Blackout).

##  Fonctionnalités du Simulateur Python
- **Visualisation Temporelle :** Graphiques interactifs d'évolution de la charge estimée par l'IA sur 24 heures.
-  **Allocation Dynamique :** Table automatisée des directives prioritaires envoyées aux compteurs intelligents connectés.
-  **Dashboard Hardware Émulé :** Interface visuelle simulant en HTML/CSS l'état de l'automate électrique physique (Rétroéclairage LCD, LEDs d'alerte, vitesse de la turbine).
-  **Archivage SQL :** Base de données SQLite embarquée assurant la traçabilité des décisions prises par l'IA.

## 🛠️ Installation & Exécution Rapide
Pour exécuter ce jumeau numérique localement sur votre machine :

1. Installez les dépendances requises :
```bash
pip install -r requirements.txt
```

2. Lancez l'application Streamlit :
```bash
streamlit run main_simulator.py
```

---
**Développé avec passion pour l'avenir de l'énergie en Afrique. **
---
##  Démonstration Vidéo
[👉 Cliquez ici pour visionner la vidéo de démonstration officielle du Jumeau Numérique sur YouTube](https://youtu.be/IoKzAn28-ho)
