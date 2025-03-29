# 🚀 Guide de Contribution

<div align="center">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat" alt="PRs welcome">
  <img src="https://img.shields.io/badge/license-GPLv3-blue" alt="License">
</div>

## 🌟 Première Contribution ?
Vous pouvez :
- Signaler un bug 🐛 (ouvrir une *Issue*)
- Proposer une amélioration 💡 (démarrer une *Discussion*)
- Soumettre du code 👩💻 (*Pull Request*)

## 🛠 Configuration Initiale

```bash
# 1. Forker le dépôt
# 2. Cloner votre fork
git clone https://github.com/votre-user/PasswordManager-Pro.git
cd PasswordManager-Pro

# 3. Installer les dépendances
pip install -r requirements-dev.txt
```

## 🔍 Workflow Recommandé

1. **Créer une branche**  
   ```bash
   git checkout -b feat/nouvelle-fonction
   ```

2. **Faire des commits atomiques**  
   ```bash
   git commit -m "feat: ajout de la vérification de force des mots de passe"
   ```

3. **Pousser vers votre fork**  
   ```bash
   git push origin feat/nouvelle-fonction
   ```

4. **Ouvrir une Pull Request**  
   - Remplissez le template PR
   - Liez les issues concernées (ex: `Fix #123`)

## ⚠️ Règles Importantes

| Catégorie       | Règles                                                                 |
|-----------------|-----------------------------------------------------------------------|
| **Code**        | - PEP 8<br>- Docstrings Google Style<br>- Typage Python (mypy)        |
| **Sécurité**    | - Audit cryptographique obligatoire<br>- Pas de hardcoding de secrets |
| **Tests**       | - Couverture >80%<br>- Tests unitaires pour toute nouvelle crypto    |

## 📊 Structure du Projet

```
.
├── src/              # Code source principal
├── tests/           # Tests unitaires
├── docs/            # Documentation
├── installer/       # Scripts d'installation
└── requirements.txt # Dépendances
```

## 🧪 Exécuter les Tests

```bash
pytest tests/ --cov=src --cov-report=html
```

## 📝 Templates Utiles

### **Rapport de Bug**
```markdown
**Description**  
[Description claire du problème]

**Reproduire**  
1. Allez à...
2. Cliquez sur...
3. Erreur observable...

**Attendu**  
[Comportement normal]
```

### **Demande de Fonctionnalité**
```markdown
**Problème**  
[Explication du besoin]

**Solution Proposée**  
[Description de votre implémentation]

**Alternatives**  
[Options envisagées]
```

## 🤝 Code de Conduite
Nous suivons le [Contributor Covenant](https://www.contributor-covenant.org/).  
⚠️ Tout abus sera sanctionné.

## 📜 Licence
En contribuant, vous acceptez de publier sous **GPLv3**.

---

<div align="center">
  ❓ Questions ? Rejoignez les <a href="https://github.com/votre-user/PasswordManager-Pro/discussions">Discussions</a> !
</div>