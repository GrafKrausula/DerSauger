# DerSauger Versioning Scheme

## Format

```
{Major}.{Minor}.{Patch} {Greek Letter}
```

**Beispiel:** `1.0.0 Zeta`

---

## Griechisches Alphabet (24 Buchstaben)

| #  | Buchstabe | #  | Buchstabe |
|----|-----------|----|-----------| 
| 1  | Alpha     | 13 | Nu        |
| 2  | Beta      | 14 | Xi        |
| 3  | Gamma     | 15 | Omicron   |
| 4  | Delta     | 16 | Pi        |
| 5  | Epsilon   | 17 | Rho       |
| 6  | Zeta      | 18 | Sigma     |
| 7  | Eta       | 19 | Tau       |
| 8  | Theta     | 20 | Upsilon   |
| 9  | Iota      | 21 | Phi       |
| 10 | Kappa     | 22 | Chi       |
| 11 | Lambda    | 23 | Psi       |
| 12 | Mu        | 24 | Omega     |

---

## Release-Zyklus

### Normaler Release (Standard)
Jeder Release inkrementiert den griechischen Buchstaben:

```
1.0.0 Alpha  →  1.0.0 Beta  →  1.0.0 Gamma  →  ...  →  1.0.0 Omega
```

### Nach Omega (automatischer Patch-Inkrement)
Nach dem letzten griechischen Buchstaben (Omega) wird automatisch:
- **Patch** um 1 erhöht
- **Buchstabe** auf Alpha zurückgesetzt

```
1.0.0 Omega  →  1.0.1 Alpha
```

### Minor/Major Release
Bei manuellem Minor oder Major Inkrement wird immer auf Alpha zurückgesetzt:

```
1.0.5 Theta  --minor-->  1.1.0 Alpha
1.2.3 Psi    --major-->  2.0.0 Alpha
```

---

## Beispiel-Sequenz

```
1.0.0 Alpha
1.0.0 Beta
1.0.0 Gamma
...
1.0.0 Psi
1.0.0 Omega
1.0.1 Alpha    ← Automatischer Patch-Inkrement
1.0.1 Beta
...
1.0.1 Omega
1.0.2 Alpha    ← Automatischer Patch-Inkrement
...
```

---

## Warum dieses Schema?

- **24 Releases pro Patch-Level** ermöglichen feingranulare Updates
- **Griechische Buchstaben** sind leicht merkbar und geben jeder Version einen Namen
- **Automatischer Overflow** macht das Versionieren frictionless
- **Konsistenz** durch automatisiertes Release-Script
