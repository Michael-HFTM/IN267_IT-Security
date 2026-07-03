# IT-Security Lab: Passwort Brute-Forcing

In diesem Lab lernst du, wie Angreifer ungeschützte Anmeldeschnittstellen automatisiert attackieren und wie man sich als Entwickler dagegen schützt.

---

## 1. Lab starten

Öffne deinen Terminal im Hauptverzeichnis des Repositories (im Ordner `git/`) und führe folgenden Befehl aus:

```bash
docker compose --profile brute-force up --build
```

Rufe danach die Webseite in deinem Browser auf: **[http://localhost:5000](http://localhost:5000)**

---

## 2. Angreifen (Offensive)

Der Login erlaubt unendlich viele Versuche ohne zeitliche Verzögerung oder Kontosperrung.

* **Deine Aufgabe:** Schreibe ein Python-Skript (z. B. mit der Bibliothek `requests`), das eine Liste gängiger Passwörter automatisiert durchprobiert, bis du erfolgreich eingeloggt wirst und die **FLAG** siehst.
* **Präsentation:** Halte dein Hacking-Skript und die gefundene Flag für die Präsentation in der nächsten Unterrichtseinheit bereit.

---

## 3. Absichern (Defensive)

Wechsle nun in die Rolle des Entwicklers.

* **Deine Aufgabe:** Behebe die Schwachstelle in der Datei `brute-force/main.py` auf deinem Rechner.
* **Ziel:** Implementiere einen Schutzmechanismus (z. B. eine künstliche Verzögerung bei einem Fehlversuch mit `time.sleep()` oder eine Sperre nach $X$ Versuchen), sodass automatisierte Angriffe extrem verlangsamt oder komplett blockiert werden.
* **Test:** Überprüfe, ob dein zuvor geschriebenes Hacking-Skript nach deinem Fix fehlschlägt oder blockiert wird.

```
