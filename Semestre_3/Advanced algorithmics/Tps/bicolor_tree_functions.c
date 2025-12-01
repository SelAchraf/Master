#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum { ROUGE, NOIR } Couleur;

struct Node {
    int data;
    Couleur couleur;
    struct Node* gauche;
    struct Node* droit;
    struct Node* parent;
};

int compterNoeuds(struct Node* racine);

// Fonction pour créer un nouveau noeud (toujours ROUGE à l'insertion)
struct Node* creerNoeud(int valeur) {
    struct Node* nouveauNoeud = (struct Node*)malloc(sizeof(struct Node));
    nouveauNoeud->data = valeur;
    nouveauNoeud->couleur = ROUGE;
    nouveauNoeud->gauche = NULL;
    nouveauNoeud->droit = NULL;
    nouveauNoeud->parent = NULL;
    return nouveauNoeud;
}

void rotationGauche(struct Node** racine, struct Node* x) {
    struct Node* y = x->droit;
    
    x->droit = y->gauche;
    if (y->gauche != NULL) {
        y->gauche->parent = x;
    }
    
    y->parent = x->parent;
    
    if (x->parent == NULL) {
        *racine = y;
    } else if (x == x->parent->gauche) {
        x->parent->gauche = y;
    } else {
        x->parent->droit = y;
    }
    
    y->gauche = x;
    x->parent = y;
}

void rotationDroite(struct Node** racine, struct Node* x) {
    struct Node* y = x->gauche;
    
    x->gauche = y->droit;
    if (y->droit != NULL) {
        y->droit->parent = x;
    }
    
    y->parent = x->parent;
    
    if (x->parent == NULL) {
        *racine = y;
    } else if (x == x->parent->droit) {
        x->parent->droit = y;
    } else {
        x->parent->gauche = y;
    }
    
    y->droit = x;
    x->parent = y;
}

// Correction après insertion
void corrigerInsertion(struct Node** racine, struct Node* nouveau) {
    struct Node* parent = NULL;
    struct Node* grandParent = NULL;
    
    while ((nouveau != *racine) && (nouveau->couleur != NOIR) && (nouveau->parent->couleur == ROUGE)) {
        parent = nouveau->parent;
        grandParent = nouveau->parent->parent;
        
        // Cas A: Le parent est le fils gauche du grand-parent
        if (parent == grandParent->gauche) {
            struct Node* oncle = grandParent->droit;
            
            // Cas 1: L'oncle est aussi ROUGE - Recoloration
            if (oncle != NULL && oncle->couleur == ROUGE) {
                grandParent->couleur = ROUGE;
                parent->couleur = NOIR;
                oncle->couleur = NOIR;
                nouveau = grandParent;
            } else {
                // Cas 2: nouveau est le fils droit - Rotation gauche
                if (nouveau == parent->droit) {
                    rotationGauche(racine, parent);
                    nouveau = parent;
                    parent = nouveau->parent;
                }
                
                // Cas 3: nouveau est le fils gauche - Rotation droite
                rotationDroite(racine, grandParent);
                Couleur temp = parent->couleur;
                parent->couleur = grandParent->couleur;
                grandParent->couleur = temp;
                nouveau = parent;
            }
        }
        // Cas B: Le parent est le fils droit du grand-parent
        else {
            struct Node* oncle = grandParent->gauche;
            
            // Cas 1: L'oncle est aussi ROUGE - Recoloration
            if (oncle != NULL && oncle->couleur == ROUGE) {
                grandParent->couleur = ROUGE;
                parent->couleur = NOIR;
                oncle->couleur = NOIR;
                nouveau = grandParent;
            } else {
                // Cas 2: nouveau est le fils gauche - Rotation droite
                if (nouveau == parent->gauche) {
                    rotationDroite(racine, parent);
                    nouveau = parent;
                    parent = nouveau->parent;
                }
                
                // Cas 3: nouveau est le fils droit - Rotation gauche
                rotationGauche(racine, grandParent);
                Couleur temp = parent->couleur;
                parent->couleur = grandParent->couleur;
                grandParent->couleur = temp;
                nouveau = parent;
            }
        }
    }
    
    (*racine)->couleur = NOIR;  // La racine doit toujours être NOIRE
}

// Fonction pour insérer un noeud
struct Node* inserer(struct Node** racine, int valeur) {
    struct Node* nouveau = creerNoeud(valeur);
    
    // Cas spécial: arbre vide
    if (*racine == NULL) {
        nouveau->couleur = NOIR;  // La racine est toujours NOIRE
        *racine = nouveau;
        return nouveau;
    }
    
    // Insertion BST standard
    struct Node* courant = *racine;
    struct Node* parent = NULL;
    
    while (courant != NULL) {
        parent = courant;
        if (valeur < courant->data) {
            courant = courant->gauche;
        } else if (valeur > courant->data) {
            courant = courant->droit;
        } else {
            // Valeur déjà présente
            free(nouveau);
            printf("Valeur %d deja presente dans l'arbre.\n", valeur);
            return courant;
        }
    }
    
    // Insérer le nouveau noeud
    nouveau->parent = parent;
    if (valeur < parent->data) {
        parent->gauche = nouveau;
    } else {
        parent->droit = nouveau;
    }
    
    // Corriger les violations des propriétés Rouge-Noir
    corrigerInsertion(racine, nouveau);
    
    return nouveau;
}

// Fonction pour trouver le minimum
struct Node* minimum(struct Node* noeud) {
    while (noeud->gauche != NULL) {
        noeud = noeud->gauche;
    }
    return noeud;
}

// Fonction pour rechercher un noeud
struct Node* rechercherNoeud(struct Node* racine, int valeur) {
    while (racine != NULL && racine->data != valeur) {
        if (valeur < racine->data) {
            racine = racine->gauche;
        } else {
            racine = racine->droit;
        }
    }
    return racine;
}

// Remplacer un noeud par un autre
void remplacerNoeud(struct Node** racine, struct Node* u, struct Node* v) {
    if (u->parent == NULL) {
        *racine = v;
    } else if (u == u->parent->gauche) {
        u->parent->gauche = v;
    } else {
        u->parent->droit = v;
    }
    
    if (v != NULL) {
        v->parent = u->parent;
    }
}

// Correction après suppression
void corrigerSuppression(struct Node** racine, struct Node* x, struct Node* xParent) {
    while (x != *racine && (x == NULL || x->couleur == NOIR)) {
        if (x == xParent->gauche) {
            struct Node* frere = xParent->droit;
            
            // Cas 1: Le frère est ROUGE
            if (frere->couleur == ROUGE) {
                frere->couleur = NOIR;
                xParent->couleur = ROUGE;
                rotationGauche(racine, xParent);
                frere = xParent->droit;
            }
            
            // Cas 2: Les deux enfants du frère sont NOIRS
            if ((frere->gauche == NULL || frere->gauche->couleur == NOIR) &&
                (frere->droit == NULL || frere->droit->couleur == NOIR)) {
                frere->couleur = ROUGE;
                x = xParent;
                xParent = x->parent;
            } else {
                // Cas 3: L'enfant droit du frère est NOIR
                if (frere->droit == NULL || frere->droit->couleur == NOIR) {
                    if (frere->gauche != NULL) {
                        frere->gauche->couleur = NOIR;
                    }
                    frere->couleur = ROUGE;
                    rotationDroite(racine, frere);
                    frere = xParent->droit;
                }
                
                // Cas 4: L'enfant droit du frère est ROUGE
                frere->couleur = xParent->couleur;
                xParent->couleur = NOIR;
                if (frere->droit != NULL) {
                    frere->droit->couleur = NOIR;
                }
                rotationGauche(racine, xParent);
                x = *racine;
            }
        } else {
            struct Node* frere = xParent->gauche;
            
            // Cas 1: Le frère est ROUGE
            if (frere->couleur == ROUGE) {
                frere->couleur = NOIR;
                xParent->couleur = ROUGE;
                rotationDroite(racine, xParent);
                frere = xParent->gauche;
            }
            
            // Cas 2: Les deux enfants du frère sont NOIRS
            if ((frere->droit == NULL || frere->droit->couleur == NOIR) &&
                (frere->gauche == NULL || frere->gauche->couleur == NOIR)) {
                frere->couleur = ROUGE;
                x = xParent;
                xParent = x->parent;
            } else {
                // Cas 3: L'enfant gauche du frère est NOIR
                if (frere->gauche == NULL || frere->gauche->couleur == NOIR) {
                    if (frere->droit != NULL) {
                        frere->droit->couleur = NOIR;
                    }
                    frere->couleur = ROUGE;
                    rotationGauche(racine, frere);
                    frere = xParent->gauche;
                }
                
                // Cas 4: L'enfant gauche du frère est ROUGE
                frere->couleur = xParent->couleur;
                xParent->couleur = NOIR;
                if (frere->gauche != NULL) {
                    frere->gauche->couleur = NOIR;
                }
                rotationDroite(racine, xParent);
                x = *racine;
            }
        }
    }
    
    if (x != NULL) {
        x->couleur = NOIR;
    }
}

// Fonction pour supprimer un noeud
struct Node* supprimerNoeud(struct Node** racine, int valeur) {
    struct Node* z = rechercherNoeud(*racine, valeur);
    
    if (z == NULL) {
        printf("Valeur %d non trouvee dans l'arbre.\n", valeur);
        return NULL;
    }
    
    struct Node* y = z;
    struct Node* x;
    struct Node* xParent;
    Couleur couleurOriginale = y->couleur;
    
    if (z->gauche == NULL) {
        x = z->droit;
        xParent = z->parent;
        remplacerNoeud(racine, z, z->droit);
    } else if (z->droit == NULL) {
        x = z->gauche;
        xParent = z->parent;
        remplacerNoeud(racine, z, z->gauche);
    } else {
        y = minimum(z->droit);
        couleurOriginale = y->couleur;
        x = y->droit;
        
        if (y->parent == z) {
            xParent = y;
        } else {
            xParent = y->parent;
            remplacerNoeud(racine, y, y->droit);
            y->droit = z->droit;
            y->droit->parent = y;
        }
        
        remplacerNoeud(racine, z, y);
        y->gauche = z->gauche;
        y->gauche->parent = y;
        y->couleur = z->couleur;
    }
    
    if (couleurOriginale == NOIR) {
        corrigerSuppression(racine, x, xParent);
    }
    
    free(z);
    return *racine;
}

// Fonction auxiliaire pour obtenir la hauteur de l'arbre
int obtenirHauteur(struct Node* racine) {
    if (racine == NULL) {
        return 0;
    }
    int hauteurGauche = obtenirHauteur(racine->gauche);
    int hauteurDroite = obtenirHauteur(racine->droit);
    return (hauteurGauche > hauteurDroite ? hauteurGauche : hauteurDroite) + 1;
}

// Fonction auxiliaire pour imprimer les espaces
void imprimerEspaces(int n) {
    for (int i = 0; i < n; i++) {
        printf(" ");
    }
}
// Remplir un tableau avec les pointeurs de noeuds en parcours infixe
void remplirInfixePtr(struct Node* racine, struct Node** arr, int* idx) {
    if (racine == NULL) return;
    remplirInfixePtr(racine->gauche, arr, idx);
    arr[(*idx)++] = racine;
    remplirInfixePtr(racine->droit, arr, idx);
}

// Trouver l'indice d'un noeud dans le tableau infixe
int findIndex(struct Node** arr, int n, struct Node* target) {
    for (int i = 0; i < n; i++) {
        if (arr[i] == target) return i;
    }
    return -1;
}

// Construire un tableau niveaux[] parallèle à l'ordre infixe (niveau de chaque noeud)
void buildLevels(struct Node* racine, struct Node** infixe, int n, int* niveaux) {
    if (racine == NULL) return;
    // BFS queue
    struct Node** queue = (struct Node**)malloc(n * sizeof(struct Node*));
    int head = 0, tail = 0;
    queue[tail++] = racine;
    int level = 1;
    while (head < tail) {
        int levelCount = tail - head;
        for (int i = 0; i < levelCount; i++) {
            struct Node* node = queue[head++];
            int idx = findIndex(infixe, n, node);
            if (idx >= 0) niveaux[idx] = level;
            if (node->gauche) queue[tail++] = node->gauche;
            if (node->droit) queue[tail++] = node->droit;
        }
        level++;
    }
    free(queue);
}

// Afficher l'arbre en alignant les noeuds par ordre infixe (colonnes fixes)
void afficherArbreAvecCouleurs(struct Node* racine, int espace) {
    if (racine == NULL) {
        printf("Arbre vide.\n");
        return;
    }

    int hauteur = obtenirHauteur(racine);
    int n = compterNoeuds(racine);
    struct Node** infixe = (struct Node**)malloc(n * sizeof(struct Node*));
    int idx = 0;
    remplirInfixePtr(racine, infixe, &idx);

    int* niveaux = (int*)malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) niveaux[i] = 0;
    buildLevels(racine, infixe, n, niveaux);

    int cell = 8; // largeur fixe par colonne
    int totalWidth = n * cell;

    printf("\n");
    printf("Legende: \033[1;31m[R]=Rouge\033[0m, \033[1;90m[N]=Noir\033[0m\n");
    printf("Hauteur de l'arbre: %d\n\n", hauteur);

    for (int level = 1; level <= hauteur; level++) {
        // ligne des noeuds
        for (int i = 0; i < n; i++) {
            if (niveaux[i] == level) {
                struct Node* node = infixe[i];
                // centrer le label dans the cell
                int pad = (cell - 6) / 2; // label like " 12[R]" length ~6
                imprimerEspaces(pad);
                if (node->couleur == ROUGE) {
                    printf("\033[1;31m%3d[R]\033[0m", node->data);
                } else {
                    printf("\033[1;90m%3d[N]\033[0m", node->data);
                }
                imprimerEspaces(cell - 6 - pad);
            } else {
                imprimerEspaces(cell);
            }
        }
        printf("\n");

        // ligne des connexions
        if (level < hauteur) {
            for (int i = 0; i < n; i++) {
                if (niveaux[i] == level) {
                    struct Node* node = infixe[i];
                    // Draw connectors for children
                    int hasLeft = (node->gauche != NULL);
                    int hasRight = (node->droit != NULL);
                    
                    if (hasLeft && hasRight) {
                        imprimerEspaces((cell/2)-1);
                        printf("/");
                        imprimerEspaces(1);
                        printf("\\");
                        imprimerEspaces((cell/2)-1);
                    } else if (hasLeft) {
                        imprimerEspaces((cell/2)-1);
                        printf("/");
                        imprimerEspaces((cell/2));
                    } else if (hasRight) {
                        imprimerEspaces((cell/2));
                        printf("\\");
                        imprimerEspaces((cell/2)-1);
                    } else {
                        imprimerEspaces(cell);
                    }
                } else {
                    imprimerEspaces(cell);
                }
            }
            printf("\n");
        }
    }

    free(infixe);
    free(niveaux);
}

// Fonction pour calculer la hauteur noire
int hauteurNoire(struct Node* racine) {
    if (racine == NULL) {
        return 1;  // NULL est considéré comme noir
    }
    int hn = hauteurNoire(racine->gauche);
    if (racine->couleur == NOIR) {
        hn++;
    }
    return hn;
}

// Vérifier les hauteurs noires (propriété de l'arbre Rouge-Noir)
int verifierHauteursNoires(struct Node* racine, int* hauteurNoire) {
    if (racine == NULL) {
        *hauteurNoire = 0;
        return 1;
    }
    
    int hnGauche, hnDroite;
    
    if (!verifierHauteursNoires(racine->gauche, &hnGauche) ||
        !verifierHauteursNoires(racine->droit, &hnDroite)) {
        return 0;
    }
    
    if (hnGauche != hnDroite) {
        return 0;
    }
    
    *hauteurNoire = hnGauche + (racine->couleur == NOIR ? 1 : 0);
    return 1;
}

// Helper function to check Red-Black properties recursively
int verifierProprietesRN(struct Node* noeud) {
    if (noeud == NULL) {
        return 1;
    }
    
    // Vérifier qu'il n'y a pas deux noeuds ROUGES consécutifs
    if (noeud->couleur == ROUGE) {
        if ((noeud->gauche != NULL && noeud->gauche->couleur == ROUGE) ||
            (noeud->droit != NULL && noeud->droit->couleur == ROUGE)) {
            printf("Violation: Deux noeuds ROUGES consecutifs.\n");
            return 0;
        }
    }
    
    // Vérifier récursivement
    return verifierProprietesRN(noeud->gauche) && verifierProprietesRN(noeud->droit);
}

// Fonction pour vérifier si l'arbre est un arbre Rouge-Noir valide
int estBicolore(struct Node* racine) {
    // Propriété 1: La racine doit être NOIRE
    if (racine != NULL && racine->couleur != NOIR) {
        printf("Violation: La racine n'est pas NOIRE.\n");
        return 0;
    }
    
    // Vérifier les propriétés récursivement
    int hn;
    if (!verifierHauteursNoires(racine, &hn)) {
        printf("Violation: Les hauteurs noires ne sont pas uniformes.\n");
        return 0;
    }
    
    // Vérifier qu'il n'y a pas deux noeuds ROUGES consécutifs
    if (!verifierProprietesRN(racine)) {
        return 0;
    }
    
    return 1;
}

// Compter le nombre de noeuds
int compterNoeuds(struct Node* racine) {
    if (racine == NULL) {
        return 0;
    }
    return 1 + compterNoeuds(racine->gauche) + compterNoeuds(racine->droit);
}

// Libérer la mémoire de l'arbre
void libererArbre(struct Node* racine) {
    if (racine == NULL) {
        return;
    }
    
    libererArbre(racine->gauche);
    libererArbre(racine->droit);
    free(racine);
}

// --- Fonction Principale avec Menu ---
int main() {
    struct Node *root = NULL;
    int choix, val;
    char continuer;

    do {
        printf("\n====== MENU - Arbre Rouge-Noir (Bicolore) ======\n");
        printf("1. Inserer une valeur\n");
        printf("2. Supprimer une valeur\n");
        printf("3. Afficher arbre graphique (avec couleurs ANSI)\n");
        printf("4. Verifier si l'arbre est bicolore valide\n");
        printf("5. Quitter\n");
        printf("Choix: ");
        
        if (scanf("%d", &choix) != 1) {
            printf("Entree invalide. Veuillez entrer un nombre.\n");
            while (getchar() != '\n');
            choix = 0;
        }

        switch (choix) {
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
                
                inserer(&root, val);
                printf("Valeur %d inseree.\n", val);
            }
            break;
            
        case 2:
            printf("Entrer la valeur a supprimer: ");
            if (scanf("%d", &val) == 1) {
                supprimerNoeud(&root, val);
                printf("Valeur %d supprimee (si presente).\n", val);
            } else {
                printf("Entree invalide.\n");
                while (getchar() != '\n');
            }
            break;
            
        case 3:
            printf("\nArbre avec couleurs (Format graphique):\n");
            afficherArbreAvecCouleurs(root, 0);
            break;
            
        case 4:
            if (estBicolore(root)) {
                printf("L'arbre respecte les proprietes d'un arbre Rouge-Noir.\n");
            } else {
                printf("L'arbre ne respecte PAS les proprietes d'un arbre Rouge-Noir.\n");
            }
            break;
            
        case 5:
            printf("Fin du programme.\n");
            libererArbre(root);
            break;

        default:
            printf("Choix invalide.\n");
        }

        if (choix != 5) {
            printf("\nContinuer ? (o/n): ");
            if (scanf(" %c", &continuer) != 1) {
                continuer = 'n';
                while (getchar() != '\n');
            }
        } else {
            continuer = 'n';
        }

    } while (continuer == 'o' || continuer == 'O');

    return 0;
}