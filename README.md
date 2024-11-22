# UE-AD-A1-REST-ELUECQUE

Projet réalisé dans le cadre de ma première année à l'IMT Atlantique en architecture distribuée

## Authors

- [@anthony-eluecque](https://www.github.com/anthony-eluecque)

## Pré-requis

- Docker
- Insomnia ou Postman ou équivalent.
- Pour un environnement locale, python >= 3.10


## Déploiment du projet

⚠️ Il est important d'ajouter des .env dans les dossiers suivants : 
Exemple de .env à ajouter pour configurer le projet
### - User 

```env
MOVIE_CLIENT = "http://movie:3200"
BOOKING_CLIENT = "http://booking:3201"
```

### - Booking 

```env
SHOWTIME_CLIENT = "http://showtime:3202"
```

Puis exécuter le script qui permet de lancer le projet

```bash
  ./start.bat
```
P.S : Tout est automatiquement configuré pour vous

## Modifications apportés supplémentaires

- Système de .env pour faciliter le déploiement dans un environnement de prod ou locale