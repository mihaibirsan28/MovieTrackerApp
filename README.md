# Movie Tracker App: **"Cinemate"**


# Cinemate

**"Cinemate"** va fi o aplicație web proiectată atât pentru cinefilii înrăiți, cât și pentru utilizatorii obișnuiți care doresc să se delecteze din când în când cu un film pe placul lor. Ne propunem ca aplicația să fie o platformă completă și interactivă pentru tot ceea ce ține de lumea cinematografiei. **"Cinemate"** va oferi o gamă extinsă de funcționalități precum căutare și recomandare de filme, salvare de filme în arhivă. Principalele caracteristici ale acesteia sunt:

## Caracteristici

### Sistem de Gestiune al Utilizatorilor (Înregistrare, Autentificare)

- Un utilizator va fi capabil să își creeze un cont și să se autentifice.
- După autentificare, el va putea accesa funcționalități generale ale aplicației precum căutarea de filme ori adăugarea acestora la favorite.

### Sistem de Recomandări de Filme

- Pe baza filmelor din arhiva personală, utilizatorii autentificați vor primi recomandări de noi filme cu caracteristici similare (gen, tematică, actori, an apariție).

### Sistem de Căutare de Filme

- Un utilizator autentificat va putea căuta filme pe baza caracteristicilor acestora (gen, tematică, actori, an apariție) dar și pe baza unei scurte descrieri în limbaj natural a acestuia (actori, elemente de scenariu, replici).
- Căutarea asistată de inteligența artificială este o caracteristică inedită a platformei, integrând procesarea de limbaj natural și un model de învățare automată.

### Arhivă Personală

- Aplicația permite fiecărui utilizator să salveze o listă cu filme pe care fie le-a vizionat ori dorește să le vizioneze.
- Utilizatorii vor putea să își urmărească reciproc aceste arhive, stimulând astfel implicarea socială în vizionarea filmelor.

### Sistem de Notificări

- Aplicația va notifica utilizatorii cu privire la cele mai noi filme apărute și evenimente cinematografice (festivaluri de film, proiecții în aer liber, etc.).

### Pagina unui Film

- Conține imagini de prezentare, informații cu privire la acesta (gen, tematică, an apariție, actori, descriere etc.), și platformele de streaming pe care poate fi vizionat.

### Secțiune de Clasamente (TOP-uri)

- Va conține diferite clasamente, precum TOP N filme în funcție de țară sau gen, și TOP filme premiate.


## Flowchart Diagram

![](./Diagrams/Flowchart.png)

## Database Diagram

![](./Diagrams/Db.png)

## Gantt Diagram

![](./Diagrams/gantt_chart.png)

## Use case Diagram

![](./Diagrams/use_case.png)

## Component Diagram

![](./Diagrams/cinemate_component_diagram.png)


## Class diagram
```mermaid
%%{init: {'theme':'neutral'}}%%
classDiagram
    class Movie {
        -String id
        +Enum genre
        +Int releaseYear
        +String imageUrl
        +String title
        +String[] Actors
    }
    class Review {
        -String id
        -String userId
        -String movieId
        +Int rating[1..10]
        +String reviewText
    }
  class Wishlist{
    -Int id
    -Movie movies[]
    +addMovie()
    +removeMovie()
}
class Library{
    -Int id
    -Movie movies[]
    +addMovie()
    +removeMovie()
    }
class User{
    -String id
    -String username
    -String password
    +Wishlist wishlist
    +Library library
    +login()
    +shareLibrary()
    +changePassword(newPassword)
    -sendConfirmationEmail()
    -getRecommendation()
    +addReview(movieId, rating, message)
}




Wishlist <-- Movie : contains
Library <-- Movie : contains
User *-- Wishlist : has
User *-- Library : has
Review o-- User : give
Review o-- Movie : to
```

## Diagrama de interactiune
```mermaid
sequenceDiagram
    participant Frontend
    participant Backend
    participant Database
    participant PublicAPI

    Frontend ->> Backend: Request for Movie List
    activate Backend
    Backend ->> PublicAPI: Fetch Movie List
    activate PublicAPI
    PublicAPI -->> Backend: Movie List
    deactivate PublicAPI
    Backend -->> Frontend: Movie List Response
    deactivate Backend

    activate Frontend
    Frontend -->> Backend: Add movie to wishlist
    activate Backend
    Backend ->> Database: Store Wishlist
    activate Database
    Backend ->> Database: <<add>>
    Database -->> Backend: New wishlist returned
    deactivate Database
    Backend -->> Frontend: Wishlist Response
    deactivate Backend

```

