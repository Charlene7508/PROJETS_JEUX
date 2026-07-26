# MAZE - Générateur de labyrinthe à jouer

*Réimplémentation personnelle du projet "A-Maze-ing" de l'École 42 — seule, de zéro, incluant le moteur de génération de labyrinthe, un affichage terminal, et une version graphique jouable avec la MiniLibX (MLX).*

## Description

Ce projet génère un labyrinthe avec un algorithme de backtracking récursif, calcule le plus court chemin entre une entrée et une sortie via un parcours en largeur (BFS), et affiche le résultat de deux façons :

- un **mode terminal**, qui affiche le labyrinthe généré et sa solution automatiquement ;
- un **mode graphique jouable** (MLX), où l'on contrôle un personnage et navigue soi-même dans le labyrinthe, avec un indice optionnel (le plus court chemin) et un motif "C" personnel caché au centre du labyrinthe, à la place du "42" original.

Ce projet est une suite personnelle du projet officiel "A-Maze-ing" de l'École 42 (réalisé en binôme avec un camarade), redéveloppée seule ensuite pour m'approprier les algorithmes de génération et de pathfinding qui avaient été gérés par mon binôme la première fois.

## Fonctionnalités

- Génération de labyrinthe par backtracking récursif (garantit un labyrinthe parfait : exactement un chemin entre deux cellules quelconques).
- Résolution du plus court chemin par BFS (parcours en largeur).
- Motif "C" personnalisé (cellules fermées, isolées), centré dans le labyrinthe, remplaçant le motif "42" original.
- Encodage hexadécimal du labyrinthe dans un fichier de sortie texte.
- Affichage terminal : murs complets, entrée/sortie, chemin solution, 3 palettes de couleurs, menu interactif.
- Affichage graphique (MLX) : le même labyrinthe, jouable aux flèches directionnelles, avec un personnage déplaçable, détection de collision contre les murs, message de victoire, et les mêmes options interactives (régénérer, afficher/masquer l'indice, changer de couleurs, quitter).

## Instructions

### Prérequis

- Python 3.10+
- Un environnement virtuel (recommandé)

### Installation

```bash
python3 -m venv venv
source venv/bin/activate
make install
```

### Configuration

Modifier `config.txt` pour définir les paramètres du labyrinthe :

```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

### Lancer — mode terminal

```bash
make run
```

Génère un labyrinthe, l'écrit dans le fichier de sortie, et l'affiche (avec la solution) dans le terminal, avec un menu interactif :

- `1` — Régénérer un nouveau labyrinthe
- `2` — Afficher / masquer le plus court chemin
- `3` — Changer la palette de couleurs
- `4` — Quitter

### Lancer — mode graphique / jouable (MLX)

Le mode graphique MLX nécessite de compiler le module Python MiniLibX à partir des sources fournies par l'École 42 (`mlx_CLXV`), ainsi qu'un environnement d'affichage graphique (disponible par défaut sur les bureaux Linux ; sur WSL, nécessite WSLg sous Windows 11).

**Installation (une seule fois) :**

```bash
make install-mlx
```

**Lancer le jeu :**

```bash
make run-mlx
```

Contrôles :

- **Flèches directionnelles** — déplacer le personnage dans le labyrinthe
- `1` — Régénérer un nouveau labyrinthe
- `2` — Afficher / masquer le plus court chemin (indice)
- `3` — Changer la palette de couleurs
- `4` — Quitter

Atteindre la sortie pour gagner — un message apparaît, et on peut régénérer un nouveau labyrinthe depuis le menu.

### Lint

```bash
make lint          # flake8 + mypy
make lint-strict   # flake8 + mypy --strict
```

## Structure du projet

```
.
├── a_maze_ing.py           # point d'entrée (pipeline mode terminal)
├── config.txt               # configuration par défaut
├── mazegen/
│   ├── mazegen.py           # moteur de génération : create_grid, remove_wall,
│   │                        # generate_maze (backtracker), BFS, shortest_path
│   └── config_loader.py     # parsing et validation du fichier de config
├── output/
│   ├── encoder.py           # encodage hexadécimal, écriture du fichier de sortie
│   ├── display.py           # affichage terminal (murs, couleurs, chemin)
│   ├── menu.py               # menu interactif terminal
│   ├── mlx_display.py       # version graphique + jouable (MLX)
│   └── assets/               # images du joueur et de la sortie
├── tests/
│   └── fixtures.py          # labyrinthes de test fixes utilisés pendant le développement
└── Makefile
```

## Choix techniques

**Algorithme de génération — backtracking récursif (itératif, à base de pile).** Choisi car il produit toujours un labyrinthe parfait (aucune boucle, exactement un chemin entre deux cellules quelconques) — ce qui garantit aussi, gratuitement, qu'aucune zone ne peut faire plus de 2 cellules de large. Implémenté de façon itérative (avec une pile explicite) plutôt qu'en récursion réelle, pour éviter la limite de profondeur de récursion de Python sur les grands labyrinthes.

**Pathfinding — BFS (parcours en largeur).** Explore le labyrinthe niveau par niveau depuis l'entrée ; la première fois que la sortie est dépilée, le chemin trouvé est garanti être le plus court. Un dictionnaire `came_from` enregistre, pour chaque cellule visitée, depuis quelle cellule elle a été découverte — le chemin est reconstruit en remontant ce dictionnaire depuis la sortie jusqu'à l'entrée.

**Motif "C" personnalisé.** Remplace le motif "42" original spécifique à l'école. Un ensemble fixe de 5 coordonnées relatives est centré dans la grille ; ces cellules sont ajoutées à l'ensemble `visited` *avant* le début de la génération, si bien que le backtracker n'y entre jamais et n'ouvre jamais de mur autour d'elles — elles restent entièrement fermées et isolées, exactement comme l'exigeait le motif dans le sujet original.

**Rendu graphique (MLX).** Le labyrinthe est dessiné en une seule passe dans un buffer image en mémoire (`mlx_new_image` + écritures directes dans le buffer), puis envoyé à la fenêtre en un seul appel — nettement plus rapide que d'appeler `mlx_pixel_put` pixel par pixel, ce qui posait un vrai problème de performance dès que le déplacement du joueur nécessitait des redessins fréquents.

## Ressources

- Sujet officiel "A-Maze-ing" de l'École 42 (structure du projet, format du fichier de sortie, exigence du motif "42" — adapté ici en motif "C" personnel).
- Documentation MiniLibX (pages `man/` et header `mlx.h`, fournis avec les sources `mlx_CLXV`) et les exemples fournis `simple_test.py` / `mlxtest.py`, utilisés comme référence pour la syntaxe exacte du wrapper Python (buffers image, key hooks, format des couleurs).
- Documentation Python sur `collections.deque` (file pour le BFS) et la syntaxe des opérations bit à bit / type hints.

### Utilisation de l'IA

L'IA (Claude) a été utilisée tout au long du projet comme **assistant pédagogique**, pas comme générateur de code. Pour chaque nouveau concept (backtracking récursif, BFS, systèmes de coordonnées, buffers image MLX, key hooks), elle expliquait d'abord l'idée sous-jacente, puis guidait l'implémentation étape par étape via des questions et corrections — tout le code a été écrit à la main et débogué personnellement, donc chaque partie du projet peut être expliquée et modifiée de façon autonome. L'IA a aussi aidé à diagnostiquer des problèmes spécifiques à MLX (ordre des canaux de couleur, initialisation des buffers, superposition d'images) sans documentation publique claire, et a participé à l'optimisation des performances une fois que le rendu pixel par pixel naïf est devenu trop lent pour un déplacement du joueur en temps réel.

## Pistes d'amélioration

- Le rendu MLX redessine encore l'intégralité du buffer du labyrinthe à chaque déplacement du joueur ; une optimisation supplémentaire consisterait à mettre en cache l'arrière-plan et à ne patcher que la zone modifiée.
- Le moteur réutilisable (`mazegen`) pourrait être packagé comme module installable (`pip install`), comme l'exigeait le sujet original de 42, pour être réutilisé dans de futurs projets (par exemple un jeu façon Pac-Man construit sur le même moteur de labyrinthe).
- Le centrage du texte dans la fenêtre MLX est actuellement estimé manuellement (aucune API de métriques de police disponible dans ce wrapper MLX) — une approche plus robuste consisterait à mesurer la largeur réelle du texte rendu si la bibliothèque venait à l'exposer.