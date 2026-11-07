
# IT-Security Lab: Cross-Site Scripting (XSS)

In diesem Lab lernst du die drei wesentlichen Spielarten von Cross-Site Scripting kennen: **Stored XSS**, **Reflected XSS** und **DOM-based XSS**. 
Anschliessend untersuchst du anhand der Server-Logs, warum clientseitige Schwachstellen (DOM XSS) für klassische Web Application Firewalls (WAF) und Server-Monitoring unsichtbar bleiben.

Siehe auch https://community.owasp.org/attacks/xss/

## 1. Lab starten

Stelle sicher, dass Docker läuft. Öffne dein Terminal im Hauptverzeichnis des Repositories (`git/`) und starte das Lab:
```bash
docker compose --profile xss up --build
````

Rufe das Portal in deinem Browser auf: **[http://localhost:5002](http://localhost:5002)**

## 2. Hacking-Phase (Offensive)

### Level 1: Stored XSS im Produkt-Review

Beim Stored XSS speichert die Webapplikation ungefilterte Benutzereingaben persistent in einer Datenbank. Jeder spätere Besucher, der diese Daten abruft, führt den Schadcode automatisch in seinem eigenen Browser aus.

#### Aufgabe:

1. Öffne die Produktseite des **Faust Smart-Lötkolben 3000** (`/product`).
    
2. Verfasse eine neue Rezension und schleuse einen JavaScript-Payload in das Bewertungsfeld ein (z. B. `<script>alert('Stored XSS');</script>`) und klicke auf Bewertung veröffentlichen.
    
3. **Erkenntnis:** Das Pop-up erscheint sofort. Lade die Seite neu (`F5`) oder öffne sie in einem privaten Fenster: Der Schadcode ist dauerhaft in der SQLite-Datenbank gespeichert und wird bei jedem Seitenaufruf erneut ausgeführt.
	
4. Finde (überlege, prüfe) jetzt die Antworten zu folgenden Fragen: 
	1. Was wird auf dem Server von Faust-Electronics in der Datenbank gespeichert?
	2. Was würde in den Serverlogs stehen? 
	3. Ist der Payload in der Bewertung im Browser sichtbar?
	4. Ist der Payload im html Code des Browsers sichtbar? Suche mit den Entwicklertools im Browser.

**Wichtig für die nächsten Levels:** Klicke oben rechts auf den roten Button DB & Reviews zurücksetzen, damit die Produktseite für Level 2 wieder sauber ist.

**Bonus:**  In der Realität wollen Angreifer selten nur ein Pop-up anzeigen. Ziel ist oft das Abgreifen von Passwörtern über gefälschte Formulare (Credential Phishing) oder das Session Hijacking (Stehlen von Session Cookies). Kannst du die Payload so verändern, dass ein Loginfenster auf /products erscheint und das Passwort nach Eingabe z.B. per Mail an dich verschickt wird?

### Level 2: Reflected XSS & Phishing (Fake-Login)

Beim Reflected XSS speichert der Server den Schadcode **nicht** in einer Datenbank. Stattdessen nimmt er einen Parameter aus der URL (z. B. `?ref=...`) entgegen und fügt ihn direkt ("reflektiert") in die generierte HTML-Seite ein.
_Das Problem für Angreifer:_ Ein Angreifer kann nicht einfach die URL im Browser eines anderen Benutzers manipulieren. Er muss sein Opfer durch **Social Engineering (Phishing)** dazu bringen, einen speziell präparierten Link aktiv anzuklicken.

**Das Angriffsszenario (Phishing):**

Du möchtest dem Kundendienst der Faust Electronics GmbH ein gefälschtes Support-Ticket schicken. Der Support-Mitarbeiter soll auf einen Link klicken, der ihn auf die reguläre Produktseite führt. Dort erscheint jedoch durch den manipulierten Link ein täuschend echtes Login-Fenster. Gibt das Opfer sein Passwort ein, soll ein Dialogfenster visualisieren, dass die Daten abgefangen wurden.

#### Aufgabe 1: Die Reflektion analysieren

1. Rufe im Browser folgenden Link auf:
    
    [`http://localhost:5002/product?ref=SommerAktion`](`http://localhost:5002/product?ref=SommerAktion`)
    
2. Sieh dir an, wo der Text `SommerAktion` auf der Seite dargestellt wird. Der Server spiegelt den Wert ungeprüft in den Banner-Bereich.
#### Aufgabe 2: Proof of Concept

Wir wollen diese Schwachstelle nun missbrauchen und eine Payload einfügen. 
Hinweis: Aufgrund der HTML-Spezifikation kann nicht einfach ein `<script>alert("XY");</script>` eingefügt werden. Es gibt aber einen Umweg über einen Event-Handler:

1.  Injiziere einen minimalen Event-Handler-Payload in den Link:
     
``` <img src=x onerror="alert('Reflected XSS!')">``` 

**URL-Encoding beachten:**  Da URLs keine Leerzeichen oder spitzen Klammern enthalten dürfen, muss der Payload URL-kodiert übergeben werden:
    
```
http://localhost:5002/product?href=%3Cimg%20src%3Dx%20onerror%3D%22alert('Reflected%20XSS!')%22%3E
```

2. Rufe den Link auf . Wenn das Dialogfenster aufpoppt erscheint, ist die Reflected-XSS-Schwachstelle bestätigt.

Wir wollen ein modales Login-Fenster einblenden, das den Bildschirm sperrt und ein Passwort-Feld anzeigt:

#### Aufgabe 3: Phishing-Angriff durchführen
Reine Pop-up-Boxen richten in der Praxis keinen Schaden an. Das Ziel ist nun ein realistischer Phishing-Angriff (Credential Harvesting):

**Deine Aufgabe:**

1. Entwickle einen eigenen HTML/CSS-Payload, der ein gefälschtes Anmeldefenster darstellt:
    
    - Es soll sich wie ein modales Fenster über die Produktseite legen (`position: fixed; ...`).
        
    - Es soll einen Text wie _„Sitzung abgelaufen – Bitte erneut anmelden“_ enthalten.
        
    - Es soll mindestens ein Eingabefeld für ein Passwort und einen Button _„Anmelden“_ besitzen.
        
2. Binde an das Formular oder an den Absende-Button eine JavaScript-Aktion (z. B. `onclick`), die den Wert des Passwortfeldes ausliest und als alert() anzeigt (simuliert das Versenden des Passworts):
    
    `Passwort [XYZ] wird an bösen Server verschickt!`
    
3. Kodiere deinen fertigen HTML-Code als URL-String.
    
    _(Tipp: Du kannst dafür in der Browser-Konsole `encodeURIComponent('dein HTML Code')` verwenden).
    
1. Sende dein Supportticket mit der Payload ab und klicke dann als Support-Mitarbeiter darauf.

Teile deinen Payload mit den anderen im Forum auf Moodle.
#### Aufgabe 4: Forensik in den Server-Logs

1. Rufe die Server-Logs auf: **[http://localhost:5002/logs](http://localhost:5002/logs)**.
    
2. Suche den HTTP-Request, der durch den Klick auf den Ticket-Link erzeugt wurde.
    
3. **Beobachtung:** Der gesamte Schadcode ist in der Spalte _Pfad / URL_ sichtbar. Da Query-Parameter (`?ref=...`) Teil der HTTP-Anfrage sind, wandern sie über das Netzwerk direkt in das Logfile des Webservers.

### Level 3: DOM-based XSS (Der auf dem Server unsichtbare Angriff)

Bei DOM-based XSS ist serverseitig kein Schadcode aufzufinden: Der Schadcode wird nach dem Klick auf den Link im Browser direkt ausgeführt und nicht an den Server geschickt. Dadurch kann serverseitig ein DOM-based XSS Angriff kaum erkannt werden! 
#### Aufgabe 1: Die Schwachstelle analysieren

Öffne den Quelltext von `/product` (Rechtsklick -> _Seitenquelltext anzeigen_) und prüfe das Skript am Ende der Seite oder schau dir product.html an:

```
const hash = window.location.hash;
if (hash.startsWith('#ref=')) {
    const payload = decodeURIComponent(hash.substring(5));
    const domContainer = document.getElementById('dom-banner');
    if (domContainer) {
        domContainer.innerHTML = '<div>Partner-Aktion (DOM): ' + payload + '</div>';
    }
}
```

**Was macht dieser Code?**

1. `window.location.hash` liest den Text aus der Adresszeile aus, der hinter dem `#` steht (den sogenannten Anker oder Fragment-Identifier).
	
2. `domContainer.innerHTML` fügt diesen Text direkt als HTML-Code in die Seite ein. Wenn der Text HTML-Elemente oder JavaScript-Befehle enthält, führt der Browser sie sofort aus.

#### Aufgabe 2: Proof-of-Concept mit Fragment (`#`)

1. Rufe die Produktseite mit einem URL-Fragment auf. Anstatt `?ref=` benutzen wir `#ref=`:
      
```
http://localhost:5002/product#ref=%3Cimg%20src%3Dx%20onerror%3D%22alert('DOM%20XSS!')%22%3E
```
    
2. Das Dialogfenster poppt auf – diesmal getrieben durch das Client-JavaScript im Browser.
    

#### Aufgabe 3: Phishing-Angriff über DOM ausführen

1. Nimm deinen Phishing-Payload aus Level 2.
    
2. Ersetze in der URL lediglich das Fragezeichen `?ref=` durch das Hashtag `#ref=`:
    
    `http://localhost:5002/product#ref=<DEIN_KODIERTER_PAYLOAD>`
    
3. Reiche den Link unter `/support` in einem neuen Ticket ein.
    
4. Klicke unter `/tickets` auf den neuen Link. Das Fake-Login-Modal verhält sich exakt wie in Level 2.
    
#### Aufgabe 4 Forensik: Der entscheidende Unterschied im Logfile

1. Öffne erneut die Server-Logs unter **[http://localhost:5002/logs](http://localhost:5002/logs)**.
    
2. Vergleiche die Einträge:
    
    - **Level 2 (Reflected):** `GET /product?ref=%3C...`
        
    - **Level 3 (DOM-based):** `GET /product`
        
3. **Erkenntnis:**
    Fragment-Identifier (`#...`) werden vom Browser **niemals an den Webserver übertragen**. Für den Webserver war dies ein gewöhnlicher, harmloser Aufruf der Produktseite. Eine serverseitige WAF (Web Application Firewall) hat keine Chance, diesen Angriff im Netzwerkverkehr zu erkennen.

## 3. Fixing-Phase (Defensive)

Die in diesem Lab gezeigten Angriffe beruhen auf verschiedenen Schwachstellen im Code und können nicht einfach so durchgeführt werden. Wechsle nun in die Rolle des Sicherheitsbeauftragten und Entwicklers. Deine Aufgabe ist es, alle drei Schwachstellen in der Datei `xss/templates/product.html` zu beheben.

Nutze als Referenz das **OWASP Cross Site Scripting Prevention Cheat Sheet**:
[https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)

#### 1. Fix für Stored & Reflected XSS (Framework Security)
Laut OWASP bieten moderne Web-Frameworks (wie das hier verwendete Flask mit Jinja2) integrierte Schutzmechanismen wie *Auto-Escaping*, um XSS zu verhindern. Entwickler müssen jedoch aufpassen, dass sie diese Schutzmechanismen nicht versehentlich umgehen (siehe Abschnitt *Framework Security* im OWASP Cheat Sheet).

1. Öffne die Datei `xss/templates/product.html` in deinem Editor.
2. Finde die Stellen, an denen die Reviews (Level 1) und der Partner-Parameter (Level 2) im HTML ausgegeben werden.
3. Finde heraus, durch welchen expliziten Jinja2-Befehl (Filter) das automatische Escaping des Frameworks deaktiviert wurde.
4. Entferne diesen Befehl, damit das Framework die Benutzereingaben wieder sicher als reinen Text maskiert (HTML Entity Encoding).
5. Prüfe, ob Stored und Reflected XSS noch funktioniert.

**Tipp:** In Jinja2 (der Template-Engine) werden Filter mit einem senkrechten Strich (`|`) an Variablen angehängt.

#### 2. Fix für DOM-based XSS (Safe Sinks)
Bei DOM-basiertem XSS entsteht die Schwachstelle im JavaScript des Browsers, wenn Daten an sogenannte unsichere Senken (*Sinks*) übergeben werden. Laut dem OWASP Cheat Sheet sollten Entwickler Referenzen auf unsichere Senken wie `.innerHTML` vermeiden und stattdessen sichere Senken (*Safe Sinks*) nutzen, die Eingaben als reinen Text behandeln.

1. Untersuche den `<script>`-Block am Ende von `xss/templates/product.html`.
2. Identifiziere die unsichere Eigenschaft, mit der die Daten in den DOM-Container geschrieben werden.
3. Konsultiere den Abschnitt *Safe Sinks* im OWASP Cheat Sheet.
4. Ersetze die unsichere Eigenschaft in deinem Code durch eine der von OWASP empfohlenen Eigenschaften (Tipp: Suche nach einer Methode oder Eigenschaft, die den Inhalt als simplen Textknoten behandelt und kein HTML parst).

#### 3. Verifikation
1. Setze das Lab über den roten Reset-Button zurück.
2. Erstelle erneut ein Support-Ticket und klicke unter `/tickets` auf deine manipulierten Links aus Level 2 und Level 3.
3. **Erfolgskontrolle:** Weder das Alert-Fenster noch das Fake-Login dürfen jetzt ausgeführt werden. Der injizierte Code muss als harmloser Klartext sicher auf der Webseite angezeigt werden.

#### 4. Bonus
Angenommen, du könntest den Code auf dem Server nicht beeinflussen, bist aber trotzdem für die Sicherheit zuständig. Was könntest du tun, um XSS-Angriffe zu erkennen und abzuwehren?
