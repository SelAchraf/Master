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
void parcoursInfixe(struct Node* racine);
struct Node* rotationGauche(struct Node* y);
struct Node* rotationDroite(struct Node* x);
struct Node* equilibrer(struct Node* racine);
/* ================================================= */

// Fonction pour créer un nouveau noeud
struct Node* creerNoeud(int valeur) {
    struct Node* nouveauNoeud = (struct Node*)malloc(sizeof(struct Node));
    nouveauNoeud->data = valeur;
    nouveauNoeud->gauche = NULL;
    nouveauNoeud->droit = NULL;
    return nouveauNoeud;
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
    if (fe > 1) {
        return 0;
    }
    return estEquilibre(racine->gauche) && estEquilibre(racine->droit);
}

// Fonction pour la rotation gauche
struct Node* rotationGauche(struct Node* y) {
    struct Node* x = y->droit;
    struct Node* T2 = x->gauche;
    x->gauche = y;
    y->droit = T2;
    return x;
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

    // Cas gauche-gauche
    if (fe > 1 && facteurEquilibre(racine->gauche) >= 0) {
        return rotationDroite(racine);
    }

    // Cas droite-droite
    if (fe < -1 && facteurEquilibre(racine->droit) <= 0) {
        return rotationGauche(racine);
    }

    // Cas gauche-droite
    if (fe > 1 && facteurEquilibre(racine->gauche) < 0) {
        racine->gauche = rotationGauche(racine->gauche);
        return rotationDroite(racine);
    }

    // Cas droite-gauche
    if (fe < -1 && facteurEquilibre(racine->droit) > 0) {
        racine->droit = rotationDroite(racine->droit);
        return rotationGauche(racine);
    }

    return racine; // Déjà équilibré
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
        printf("3. Afficher hauteur de l'arbre\n");
        printf("4. Afficher facteur d'equilibre de la racine\n");
        printf("5. Verifier si l'arbre est equilibre\n");
        printf("6. Equilibrer l'arbre\n");
        printf("7. Quitter\n");
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
            printf("Arbre apres equilibration (parcours infixe): ");
            parcoursInfixe(root);
            break;
        case 7:
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