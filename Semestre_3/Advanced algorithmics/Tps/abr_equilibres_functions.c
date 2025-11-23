#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <string.h>

// Définition de la structure d'un noeud de l'ABR
struct Node {
    int data;
    struct Node* gauche;
    struct Node* droit;
};

/* ============ PROTOTYPES DES FONCTIONS ============ */
struct Node* creerNoeud(int valeur);
struct Node* inserer(struct Node* noeud, int valeur);
int hauteur(struct Node* racine);
int facteurEquilibre(struct Node* noeud);
int estEquilibre(struct Node* racine);
void afficherArbre(struct Node* racine, int espace);
struct Node* rotationGauche(struct Node* y);
struct Node* rotationDroite(struct Node* x);
struct Node* equilibrer(struct Node* racine);
int compterNoeuds(struct Node* racine);
void remplirTableau(struct Node* racine, int* tableau, int* index);
struct Node* construireABREquilibre(int* tableau, int debut, int fin);
void libererArbre(struct Node* racine);
struct Node* equilibrerParReconstruction(struct Node* racine);
/* ================================================= */

// Fonction pour créer un nouveau noeud
struct Node* creerNoeud(int valeur) {
    struct Node* nouveauNoeud = (struct Node*)malloc(sizeof(struct Node));
    nouveauNoeud->data = valeur;
    nouveauNoeud->gauche = NULL;
    nouveauNoeud->droit = NULL;
    return nouveauNoeud;
}

// Fonction pour afficher l'arbre graphiquement
void afficherArbre(struct Node* racine, int espace) {
    if (racine == NULL) {
        return;
    }
    
    // Afficher le noeud actuel avec l'indentation appropriée
    for (int i = 0; i < espace; i++) {
        printf("  ");
    }
    printf("%d\n", racine->data);
    
    // Augmenter l'espacement pour les sous-arbres
    espace += 1;
    
    // Afficher le sous-arbre gauche
    if (racine->gauche != NULL) {
        for (int i = 0; i < espace; i++) {
            printf("  ");
        }
        printf("G: ");
        afficherArbre(racine->gauche, espace + 1);
    }
    
    // Afficher le sous-arbre droit
    if (racine->droit != NULL) {
        for (int i = 0; i < espace; i++) {
            printf("  ");
        }
        printf("D: ");
        afficherArbre(racine->droit, espace + 1);
    }
}

// Fonction pour insérer un noeud
struct Node* inserer(struct Node* noeud, int valeur) {
    if (noeud == NULL) {
        return creerNoeud(valeur);
    }

    if (valeur < noeud->data) {
        noeud->gauche = inserer(noeud->gauche, valeur);
    } else if (valeur > noeud->data) {
        noeud->droit = inserer(noeud->droit, valeur);
    }

    return noeud;
}

// Fonction pour afficher l'arbre (parcours infixe : Gauche-Racine-Droit)
void parcoursInfixe(struct Node* racine) {
    if (racine != NULL) {
        parcoursInfixe(racine->gauche);
        printf("%d ", racine->data);
        parcoursInfixe(racine->droit);
    }
}

// Fonction pour calculer l'hauteur de l'arbre
int hauteur(struct Node* racine) {
    if (racine == NULL) {
        return -1; // Hauteur d'un arbre vide est -1
    } else {
        int hauteurGauche = hauteur(racine->gauche);
        int hauteurDroite = hauteur(racine->droit);
        return (hauteurGauche > hauteurDroite ? hauteurGauche : hauteurDroite) + 1;
    }
}

// Fonction pour calculer le facteur d'équilibre d'un noeud
int facteurEquilibre(struct Node* noeud) {
    if (noeud == NULL) {
        return 0;
    }
    int fe = hauteur(noeud->gauche) - hauteur(noeud->droit);

    return fe;
}

// Fonction pour tester si l'arbre est équilibré
int estEquilibre(struct Node* racine) {
    if (racine == NULL) {
        return 1;
    }
    int fe = facteurEquilibre(racine);
    if (abs(fe) > 1) {
        return 0;
    }
    return estEquilibre(racine->gauche) && estEquilibre(racine->droit);
}

// Fonction pour la rotation gauche
struct Node* rotationGauche(struct Node* x) {
    struct Node* y = x->droit;
    struct Node* T2 = y->gauche;
    y->gauche = x;
    x->droit = T2;
    return y;
}

// Fonction pour la rotation droite
struct Node* rotationDroite(struct Node* x) {
    struct Node* y = x->gauche;
    struct Node* T2 = y->droit;
    y->droit = x;
    x->gauche = T2;
    return y;
}

// Fonction pour équilibrer l'arbre
struct Node* equilibrer(struct Node* racine) {
    int fe = facteurEquilibre(racine);

    // Cas gauche-gauche (rotation droite simple)
    if (fe > 1 && facteurEquilibre(racine->gauche) >= 0) {
        return rotationDroite(racine);
    }

    // Cas droite-droite (rotation gauche simple)
    if (fe < -1 && facteurEquilibre(racine->droit) <= 0) {
        return rotationGauche(racine);
    }

    // Cas gauche-droite (rotation double GD)
    if (fe > 1 && facteurEquilibre(racine->gauche) < 0) {
        racine->gauche = rotationGauche(racine->gauche);
        return rotationDroite(racine);
    }

    // Cas droite-gauche (rotation double DG)
    if (fe < -1 && facteurEquilibre(racine->droit) > 0) {
        racine->droit = rotationDroite(racine->droit);
        return rotationGauche(racine);
    }

    return racine; // Déjà équilibré
}

// Fonction pour compter le nombre de noeuds dans l'arbre
int compterNoeuds(struct Node* racine) {
    if (racine == NULL) {
        return 0;
    }
    return 1 + compterNoeuds(racine->gauche) + compterNoeuds(racine->droit);
}

// Fonction pour remplir un tableau avec les valeurs de l'arbre (parcours infixe)
// Le tableau sera automatiquement trié en ordre croissant
void remplirTableau(struct Node* racine, int* tableau, int* index) {
    if (racine == NULL) {
        return;
    }
    
    // Parcours infixe : gauche -> racine -> droite
    remplirTableau(racine->gauche, tableau, index);
    tableau[*index] = racine->data;
    (*index)++;
    remplirTableau(racine->droit, tableau, index);
}

// Fonction pour construire un ABR équilibré à partir d'un tableau trié
// Insertion récursive depuis le milieu
struct Node* construireABREquilibre(int* tableau, int debut, int fin) {
    if (debut > fin) {
        return NULL;
    }
    
    // Trouver l'élément du milieu
    int milieu = debut + (fin - debut) / 2;
    
    // Créer le noeud racine avec l'élément du milieu
    struct Node* noeud = creerNoeud(tableau[milieu]);
    
    // Construire récursivement les sous-arbres gauche et droit
    noeud->gauche = construireABREquilibre(tableau, debut, milieu - 1);
    noeud->droit = construireABREquilibre(tableau, milieu + 1, fin);
    
    return noeud;
}

// Fonction pour libérer la mémoire de l'arbre
void libererArbre(struct Node* racine) {
    if (racine == NULL) {
        return;
    }
    
    libererArbre(racine->gauche);
    libererArbre(racine->droit);
    free(racine);
}

// Fonction pour équilibrer l'arbre par reconstruction
// Méthode : stocker les valeurs triées dans un tableau, puis reconstruire l'arbre
struct Node* equilibrerParReconstruction(struct Node* racine) {
    if (racine == NULL) {
        return NULL;
    }
    
    // 1. Compter le nombre de noeuds
    int nbNoeuds = compterNoeuds(racine);
    
    // 2. Allouer un tableau pour stocker les valeurs
    int* tableau = (int*)malloc(nbNoeuds * sizeof(int));
    if (tableau == NULL) {
        printf("Erreur d'allocation memoire!\n");
        return racine;
    }
    
    // 3. Remplir le tableau avec les valeurs triées (parcours infixe)
    int index = 0;
    remplirTableau(racine, tableau, &index);
    
    // 4. Libérer l'ancien arbre
    libererArbre(racine);
    
    // 5. Construire un nouvel arbre équilibré depuis le tableau trié
    struct Node* nouvelleRacine = construireABREquilibre(tableau, 0, nbNoeuds - 1);
    
    // 6. Libérer le tableau
    free(tableau);
    
    return nouvelleRacine;
}

// --- Fonction Principale avec Menu ---
int main() {
    struct Node *root = NULL;
    int choix, val;
    char continuer;

    do
    {
        printf("\n====== MENU - Arbre Binaire de Recherche (ABR) ======\n");
        printf("1. Inserer des valeurs\n");
        printf("2. Afficher arbre (graphique)\n");
        printf("3. Afficher hauteur de l'arbre\n");
        printf("4. Afficher facteur d'equilibre de la racine\n");
        printf("5. Verifier si l'arbre est equilibre\n");
        printf("6. Equilibrer l'arbre (par rotations)\n");
        printf("7. Equilibrer l'arbre (par reconstruction)\n");
        printf("8. Quitter\n");
        printf("Choix: ");
        
        if (scanf("%d", &choix) != 1) {
            printf("Entree invalide. Veuillez entrer un nombre.\n");
            while (getchar() != '\n');
            choix = 0;
        }

        switch (choix)
        {
        case 1:
            printf("Entrer les valeurs (-1 pour arreter): ");
            int premierInsertion = (root == NULL) ? 1 : 0;
            while (1)
            {
                if (scanf("%d", &val) != 1) {
                    printf("Entree invalide.\n");
                    while (getchar() != '\n');
                    break;
                }
                
                if (val == -1)
                    break;
                
                if (premierInsertion && root == NULL) {
                    root = creerNoeud(val);
                    premierInsertion = 0;
                    printf("Racine fixee a: %d\n", val);
                } else {
                    inserer(root, val);
                }
            }
            break;
        case 2:
            printf("\nArbre (rotation 90° - droit=haut, gauche=bas):\n");
            afficherArbre(root, 0);
            printf("\n");
            break;
        case 3:
            printf("Hauteur de l'arbre: %d\n", hauteur(root));
            break;
        case 4:
            printf("Facteur d'equilibre de la racine: %d\n", facteurEquilibre(root));
            break;
        case 5:
            if (estEquilibre(root))
                printf("L'arbre est equilibre.\n");
            else
                printf("L'arbre n'est pas equilibre.\n");
            break;
        case 6:
            root = equilibrer(root);
            printf("Arbre apres equilibration (par rotations):\n");
            afficherArbre(root, 0);
            printf("\n");
            break;
        case 7:
            root = equilibrerParReconstruction(root);
            printf("Arbre apres equilibration (par reconstruction):\n");
            afficherArbre(root, 0);
            printf("\n");
            break;
        case 8:
            printf("Fin du programme.\n");
            break;

        default:
            printf("Choix invalide.\n");
        }

        if (choix != 8)
        {
            printf("Continuer ? (o/n): ");
            if (scanf(" %c", &continuer) != 1) {
                continuer = 'n';
                while (getchar() != '\n');
            }
        }
        else
            continuer = 'n';

    } while (continuer == 'o' || continuer == 'O');

    return 0;
}