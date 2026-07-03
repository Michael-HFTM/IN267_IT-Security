# IT-Security Lab: Passwort Brute-Forcing

In diesem Lab lernst du, wie Angreifer ungeschützte Anmeldeschnittstellen automatisiert attackieren und wie man sich als Entwickler dagegen schützt.



## 1. Lab starten

Öffne deinen Terminal im Hauptverzeichnis des Repositories (im Ordner `git/`) und führe folgenden Befehl aus:

```bash
docker compose --profile brute-force up --build
```

Rufe danach die Webseite in deinem Browser auf: **[http://localhost:5000](http://localhost:5000)**



## 2. Angreifen (Offensive)

Der Server erlaubt unendlich viele Versuche ohne zeitliche Verzögerung oder Kontosperrung bei den Logins. Es könnte aber passieren, dass der Flask-Server bei zu vielen Versuchen in kurzer Zeit temporär in die Knie geht, bis der Arbeitsspeicher wieder geleert ist. Hab geduld :)

### a. Brute-Force

Für den Account **admin1** wurde ein **fünfstelliges Passwort aus Zahlen gesetzt**. Überlege dir, wie viele Mögliche Passwörter es geben kann und wie lange du wohl manuell durchprobieren müsstest. 

**Aufgabe:** Schreibe nun ein Script (z. B. mit der Bibliothek `requests` in Python), welches automatisch alle fünfstelligen Zahlen durchprobiert und im Erfolgsfall das korrekte Passwort anzeigt. 
Hast du das Passwort herausgefunden, poste dein Script im Forum auf Moodle. 

Hinweis: Der Server gibt bei falschen Passwörtern den HTML-Status-Code 401 - Access DENIED  zurück. Bei einem korrekten Passwort aber 200 OK.


### b. Brute-Force mit Word-List

Für den Account **admin2** wurde ein **Passwort aus Zahlen und Kleinbuchstaben gesetzt**, diesmal ohne Begrenzung der Passwortlänge. Wie viele mögliche Passwörter gibt es jetzt? Wie lange hätte wohl dein Brute-Force Script von vorher, um z.B. das Passwort "password123" (nicht das Passwort zu admin2) zu finden?
Um sich das Leben einfacher zu machen, verwenden Angreifer und Penntester häufig Passwortlisten, welche bekannte oder häufig verwendete Passwörter enthalten. Eine bekannte Liste unter Penntestern ist die [rockyou.txt (GitHub)](https://github.com/RykerWilder/rockyou.txt) von RykerWilder.

**Aufgabe:** Schreibe wieder ein Skript, das die Passwörter der rockyou.txt durchprobiert und das gefundene Passwort zurückgibt. Hast du das Passwort herausgefunden, poste dein Script im Forum auf Moodle. 

Hinweis: Dein Script wird wahrscheinlich mehrere Minuten benötigen.




**Lösungen für das Brute-Force Lab**
<details>

<summary>Lösung: Klicken, um die Passwörter anzuzeigen</summary>
 
| Benutzer | Passwort |
| :--- | :--- |
| **admin1** | `48151` |
| **admin2** | `butt3rfly` |
 
</details>



## 3. Verteidigen (Defensive)

Wechsle nun in die Rolle des Entwicklers.

**Aufgabe:** Überlege dir Sicherheitsmassnahmen, wie du solche Brute-Force angriffe erkennen und abwehren kannst. Wäge Nutzen/Kosten der verschiedenen Massnahmen und den Einfluss auf die User-Experience ab. Implementiere nun mindestens eine Massnahme in der Datei `brute-force/main.py` auf deinem Rechner, um den Angriff zu verhindern oder detektieren.

**Test:** Überprüfe, ob dein zuvor geschriebenes Hacking-Skript nach deinem Fix fehlschlägt oder blockiert wird.

Teile deine implementierte Massnahme auf dem Forum in Moodle.

Hinweis: Der [OWASP-Artikel zu Brute-Force Blocking](https://owasp.org/www-community/controls/Blocking_Brute_Force_Attacks) könnte dir Ideen verschaffen.



## 4. Bonus (nicht prüfungsrelevant, für Begeisterte)

Hydra oder dirb sind professionelle Passwort-Cracking Tools. [TryHackMe](https://tryhackme.com) hat einen Room, welcher als exzellentes Tutorial für Hydra dient.

1. Erstelle einen Account bei [TryHackMe](https://tryhackme.com) (gratis)
2. Löse den [Room Hydra](https://tryhackme.com/room/hydra)

Nun wende dein gewonnenes Wissen an:

3. Installiere Hydra auf deinem System.
4. Wende Hydra mit rockyou.txt auf unser Lab an und vergleiche die Geschwindigkeit.
5. Poste den hydra-command im Forum

!! Die Verwendung von Hydra für Angriffe auf unberechtigte Systeme ist strafbar!!