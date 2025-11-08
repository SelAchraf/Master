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
struct Node* chercher(struct Node* racine, int valeur);
struct Node* inserer(struct Node* noeud, int valeur);
struct Node* modifier(struct Node* racine, int ancienneValeur, int nouvelleValeur);  // **racine
int estABR(struct Node* racine);
struct Node* trouverMax(struct Node* racine);
struct Node* supprimerNoeud(struct Node* racine, int valeur);
void parcoursInfixe(struct Node* racine);
/* ================================================= */

// Fonction pour créer un nouveau noeud
struct Node* creerNoeud(int valeur) {
    struct Node* nouveauNoeud = (struct Node*)malloc(sizeof(struct Node));
    nouveauNoeud->data = valeur;
    nouveauNoeud->gauche = NULL;
    nouveauNoeud->droit = NULL;
    return nouveauNoeud;
}

// Fonction pour chercher un noeud avec une valeur donnée
struct Node* chercher(struct Node* racine, int valeur) {
    if (racine == NULL || racine->data == valeur) {
        return racine;
    }
    if (valeur > racine->data) {
        return chercher(racine->droit, valeur);
    }
    return chercher(racine->gauche, valeur);
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

// Fonction pour modifier la valeur d'un noeud si possible
struct Node* modifier(struct Node* racine, int ancienneValeur, int nouvelleValeur) {
    struct Node* noeud = chercher(racine, ancienneValeur);
    if (noeud != NULL) {
        noeud->data = nouvelleValeur;
        if (estABR(racine) == 0) {
            supprimerNoeud(racine, ancienneValeur);
            inserer(racine, nouvelleValeur);
        }
    }
}

// Fonction pour tester si l'arbre est un ABR
int estABR(struct Node* racine) {
    if (racine == NULL) {
        return 1;
    }

    if (racine->gauche != NULL && racine->gauche->data > racine->data) {
        return 0;
    }
    if (racine->droit != NULL && racine->droit->data < racine->data) {
        return 0;
    }

    return estABR(racine->gauche) && estABR(racine->droit);
}

// Fonction pour trouver le noeud avec la valeur maximale
struct Node* trouverMax(struct Node* racine) {
    struct Node* courant = racine;
    
    // On va le plus à droite possible
    while (courant != NULL && courant->droit != NULL) {
        courant = courant->droit;
    }
    return courant;
}

// Fonction pour trouver le noeud avec la valeur minimum
struct Node* trouverMin(struct Node* racine) {
    struct Node* courant = racine;
    
    // On va le plus à gauche possible
    while (courant != NULL && courant->gauche != NULL) {
        courant = courant->gauche;
    }
    return courant;
}

// Fonction pour supprimer un noeud avec une valeur donnée.
struct Node* supprimerNoeud(struct Node* racine, int valeur) {
    // 1. Cas de base : Arbre vide
    if (racine == NULL) {
        return NULL;
    }

    // 2. Recherche du noeud à supprimer
    if (valeur < racine->data) {
        racine->gauche = supprimerNoeud(racine->gauche, valeur);
    } else if (valeur > racine->data) {
        racine->droit = supprimerNoeud(racine->droit, valeur);
    } 
    
    // 3. On a trouvé le noeud à supprimer
    else {
        
        // --- CAS 1 : Le noeud est une feuille (0 fils) ---
        if (racine->gauche == NULL && racine->droit == NULL) {
            printf("Suppression (Cas 1 - Feuille): %d\n", racine->data);
            free(racine);
            return NULL;
        }
        
        // --- CAS 2 : Le noeud a un seul fils ---
        // A seulement un fils droit
        else if (racine->gauche == NULL) {
            struct Node* temp = racine->droit;
            free(racine);
            return temp;
        }
        // A seulement un fils gauche
        else if (racine->droit == NULL) {
            struct Node* temp = racine->gauche;
            free(racine);
            return temp;
        }

        // --- CAS 3 : Le noeud a deux fils ---        
        struct Node* temp = trouverMax(racine->gauche);
        racine->data = temp->data;
        racine->gauche = supprimerNoeud(racine->gauche, temp->data);
    }
    
    return racine;
}

// Fonction pour trouver le successeur d'une valeur dans une ABR.
struct Node* trouverSuccesseur(struct Node* racine, int valeur)
{
    if (racine == NULL)
        return NULL;

    if (racine->data == valeur)
    {
        if (racine->droit != NULL)
            return trouverMin(racine->droit);
        else
            return NULL;
    }

    if (valeur < racine->data)
    {
        struct Node* SuccGauche = trouverSuccesseur(racine->gauche, valeur);
        if (SuccGauche != NULL)
            return SuccGauche;
        else
            return racine;
    }

    return trouverSuccesseur(racine->droit, valeur);
}

// Fonction pour afficher l'arbre (parcours infixe : Gauche-Racine-Droit)
void parcoursInfixe(struct Node* racine) {
    if (racine != NULL) {
        parcoursInfixe(racine->gauche);
        printf("%d ", racine->data);
        parcoursInfixe(racine->droit);
    }
}

// --- Fonction Principale avec Menu ---
int main() {
    struct Node *root = NULL;
    int choix, val, val2;
    char continuer;

    do
    {
        printf("\n====== MENU - Arbre Binaire de Recherche (ABR) ======\n");
        printf("1. Inserer des valeurs\n");
        printf("2. Afficher arbre (graphique)\n");
        printf("3. Rechercher une valeur\n");
        printf("4. Modifier une valeur\n");
        printf("5. Trouver successeur\n");
        printf("6. Trouver minimum et maximum\n");
        printf("7. Supprimer un noeud\n");
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
            while (1)
            {
                if (scanf("%d", &val) != 1) {
                    printf("Entree invalide.\n");
                    while (getchar() != '\n');
                    break;
                }
                
                if (val == -1)
                    break;
                root = inserer(root, val);
            }
            break;

        case 2:
            parcoursInfixe(root);
            break;

        case 3:
            printf("Entrer valeur a rechercher: ");
            if (scanf("%d", &val) != 1) {
                printf("Entree invalide.\n");
                while (getchar() != '\n');
                break;
            }
            struct Node* res = chercher(root, val);
            printf(res ? "Valeur trouvee.\n" : "Non trouvee.\n");
            break;

        case 4:
            printf("Entrer ancienne valeur a modifier: ");
            if (scanf("%d", &val) != 1) {
                printf("Entree invalide.\n");
                while (getchar() != '\n');
                break;
            }
            printf("Entrer nouvelle valeur: ");
            if (scanf("%d", &val2) != 1) {
                printf("Entree invalide.\n");
                while (getchar() != '\n');
                break;
            }
            modifier(root, val, val2);
            break;

        case 5:
            printf("Entrer la valeur dont on cherche le successeur: ");
            if (scanf("%d", &val) != 1) {
                printf("Entree invalide.\n");
                while (getchar() != '\n');
                break;
            }
            {
                struct Node *s = trouverSuccesseur(root, val);
                if (s)
                    printf("Successeur de %d est %d\n", val, s->data);
                else
                    printf("Pas de successeur pour %d (ou noeud non trouve).\n", val);
            }
            break;

        case 6:
        {
            struct Node *minNode = trouverMin(root);
            struct Node *maxNode = trouverMax(root);
            if (minNode && maxNode)
                printf("Min = %d, Max = %d\n", minNode->data, maxNode->data);
            else
                printf("Arbre vide.\n");
            break;
        }

        case 7:
            printf("Entrer valeur a supprimer: ");
            if (scanf("%d", &val) != 1) {
                printf("Entree invalide.\n");
                while (getchar() != '\n');
                break;
            }
            root = supprimerNoeud(root, val);
            printf("Suppression terminee.\n");
            break;

        case 8:
            printf("Fin du programme.\n");
            break;

        default:
            printf("Choix invalide.\n");
        }

        if (choix != 9)
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