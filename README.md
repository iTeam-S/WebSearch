# WebSearch

> Module python permettant de faire différent recherche sur le Web.

### Initialiser la recherche

```python
from websearch import WebSearch

web = WebSearch('Gaetan Jonathan BAKARY')
```

##### Resultats pour les pages web

```python
webpages = web.pages
for wp in webpages[:5]:
   print(wp)
```
<details>
 <summary> Resultats pages web </summary>
   
```
   https://mg.linkedin.com/in/gaetanj
   https://portfolio.iteam-s.mg/%3Fu%3Dgaetan
   https://github.com/gaetan1903
   https://medium.com/%40gaetan1903
   https://gitlab.com/gaetan1903
```
   
</details>


#### Resultats pour les images

```python
webpages = web.images
for wp in webpages[:5]:
   print(wp)
```

<details>
 <summary> Resultats images </summary>
```
   https://tse3.mm.bing.net/th?id=OIP.-K25y8TqkOi9UG_40Ti8bgAAAA
   https://tse1.mm.bing.net/th?id=OIP.yJPVcDx6znFSOewLdQBbHgHaJA
   https://tse3.mm.bing.net/th?id=OIP.7rO2T_nDAS0bXm4tQ4LKQAHaJA
   https://tse2.mm.bing.net/th?id=OIP.IUIEkGQVzYRKaDA7WeeV7QHaEF
   https://tse3.explicit.bing.net/th?id=OIP.OmvVnMIVu2ZdNZHZzJK_hgAAAA
```
</details>

