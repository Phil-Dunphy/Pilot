# ClockPuzzle - Integration Anleitung

Eine JavaScript-Bibliothek für interaktive Uhren-Rätsel.

## 📦 Dateien

- `clock-puzzle.js` - Die Hauptbibliothek
- `integration-examples.html` - Ausführliche Beispiele
- `minimal-example.html` - Minimale Integration

## 🚀 Quick Start

### 1. Dateien in deine Webseite einbinden

```html
<!-- Die JavaScript-Bibliothek einbinden -->
<script src="clock-puzzle.js"></script>

<!-- Container für das Rätsel -->
<div id="puzzle"></div>

<!-- Initialisierung -->
<script>
    const puzzle = new ClockPuzzle('#puzzle', {
        clockSize: 200,
        showBorders: false,
        gap: 10
    });
</script>
```

## 📋 Optionen

```javascript
new ClockPuzzle(container, {
    mode: 'grid',           // 'grid' = 3x3, 'single' = einzelne Uhr
    clockSize: 300,         // Größe jeder Uhr in Pixeln
    showBorders: false,     // Rahmen um Uhren anzeigen
    gap: 20                 // Abstand zwischen Uhren im Grid
});
```

## 🎮 API Methoden

### 3x3 Rätsel

```javascript
// Neues Rätsel generieren
puzzle.generateNewPuzzle();

// Kritische Uhren markieren (umschalten)
puzzle.toggleCriticalHighlight();

// Kritische Uhren markieren (setzen)
puzzle.setCriticalHighlight(true);  // oder false

// Puzzle-Info abrufen (inkl. Lösung)
const info = puzzle.getPuzzleInfo();
console.log(info.kritischesElement);  // 'light', 'dark', 'rund', 'eckig'
console.log(info.startNumber);        // 1-8
console.log(info.solution);           // [1, 3, 5, 7] - Die 4 Lösungszahlen
```

### Einzelne Uhr

```javascript
puzzle.showSingleClock({
    startNumber: 1,              // 1-8
    pointerPosition: 0,          // 0-7 (0=oben, 2=rechts, 4=unten, 6=links)
    visibleNumbers: [1,2,3,4,5,6,7,8],  // Welche Zahlen sichtbar sind
    theme: 'light',              // 'light' oder 'dark'
    shape: 'rund'                // 'rund' oder 'eckig'
});
```

### Optionen ändern

```javascript
puzzle.setOptions({
    clockSize: 250,
    showBorders: true,
    gap: 15
});
```

## 💡 Anwendungsbeispiele

### Beispiel 1: Nutzer sieht nur die Uhren

```html
<div id="puzzle"></div>

<script src="clock-puzzle.js"></script>
<script>
    // Nutzer sieht nur die 9 Uhren ohne UI-Elemente
    const puzzle = new ClockPuzzle('#puzzle', {
        clockSize: 200,
        showBorders: false,
        gap: 10
    });
</script>
```

### Beispiel 2: Entwickler-Kontrolle

```javascript
// Diese Funktionen kannst du per Button, Konsole oder Code aufrufen:

// Button-Beispiel
document.getElementById('newPuzzle').addEventListener('click', () => {
    puzzle.generateNewPuzzle();
});

document.getElementById('showSolution').addEventListener('click', () => {
    const info = puzzle.getPuzzleInfo();
    alert(`Lösung: ${info.solution.join(', ')}`);
});

document.getElementById('highlight').addEventListener('click', () => {
    puzzle.toggleCriticalHighlight();
});
```

### Beispiel 3: Einzelne Uhr in deine Seite einbauen

```html
<div id="single-clock"></div>

<script src="clock-puzzle.js"></script>
<script>
    const clock = new ClockPuzzle('#single-clock');
    clock.showSingleClock({
        startNumber: 5,
        pointerPosition: 3,
        visibleNumbers: [1, 5],
        theme: 'dark',
        shape: 'eckig'
    });
</script>
```

### Beispiel 4: Versteckte Entwickler-Steuerung

```html
<!-- Nutzer sieht nur die Uhren -->
<div id="puzzle"></div>

<script src="clock-puzzle.js"></script>
<script>
    const puzzle = new ClockPuzzle('#puzzle', {
        clockSize: 200,
        showBorders: false,
        gap: 10
    });

    // Versteckte Entwickler-Steuerung per Tastatur
    document.addEventListener('keydown', (e) => {
        // STRG + N = Neues Rätsel
        if (e.ctrlKey && e.key === 'n') {
            e.preventDefault();
            puzzle.generateNewPuzzle();
        }
        
        // STRG + H = Highlight umschalten
        if (e.ctrlKey && e.key === 'h') {
            e.preventDefault();
            puzzle.toggleCriticalHighlight();
        }
        
        // STRG + L = Lösung in Konsole
        if (e.ctrlKey && e.key === 'l') {
            e.preventDefault();
            console.log(puzzle.getPuzzleInfo());
        }
    });

    // Oder per Browser-Konsole:
    // puzzle.generateNewPuzzle()
    // puzzle.toggleCriticalHighlight()
    // puzzle.getPuzzleInfo()
</script>
```

## 🎨 Styling

Die Uhren werden als Canvas-Elemente gerendert. Du kannst den Container stylen:

```css
#puzzle {
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
}
```

## 📱 Responsive

Die Uhren passen sich automatisch an die Bildschirmgröße an. Du kannst die `clockSize` je nach Viewport anpassen:

```javascript
const isMobile = window.innerWidth < 768;
const puzzle = new ClockPuzzle('#puzzle', {
    clockSize: isMobile ? 150 : 250,
    gap: isMobile ? 5 : 15
});
```

## 🔍 Browser-Kompatibilität

- Chrome/Edge: ✅
- Firefox: ✅
- Safari: ✅
- IE11: ❌ (nutzt moderne JavaScript-Features)

## 📝 Lizenz

Frei verwendbar für dein Projekt.
