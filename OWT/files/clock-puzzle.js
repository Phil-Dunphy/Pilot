/**
 * ClockPuzzle Library
 * Eine JavaScript-Bibliothek für Uhren-Rätsel
 * 
 * Verwendung:
 * const puzzle = new ClockPuzzle(containerElement, options);
 */

class ClockPuzzle {
    constructor(container, options = {}) {
        this.container = typeof container === 'string' 
            ? document.querySelector(container) 
            : container;
        
        // Optionen
        this.options = {
            mode: options.mode || 'grid', // 'grid' oder 'single'
            clockSize: options.clockSize || 300,
            showBorders: options.showBorders !== undefined ? options.showBorders : false,
            gap: options.gap || 20,
            ...options
        };

        // Interne Variablen
        this.currentPuzzle = null;
        this.showCritical = false;
        this.canvases = [];

        // Konstanten
        this.angles = [
            Math.PI / 2,          // 0: oben
            Math.PI / 4,          // 1: oben-rechts
            0.0,                  // 2: rechts
            -Math.PI / 4,         // 3: unten-rechts
            -Math.PI / 2,         // 4: unten
            -3 * Math.PI / 4,     // 5: unten-links
            Math.PI,              // 6: links
            3 * Math.PI / 4       // 7: oben-links
        ];

        this.squarePositions = [
            {x: 0, y: 0.75}, {x: 0.75, y: 0.75}, {x: 0.75, y: 0},
            {x: 0.75, y: -0.75}, {x: 0, y: -0.75}, {x: -0.75, y: -0.75},
            {x: -0.75, y: 0}, {x: -0.75, y: 0.75}
        ];

        this.squareTickPositions = [
            {start: {x: 0, y: 0.85}, end: {x: 0, y: 1}},
            {start: {x: 0.85, y: 0.85}, end: {x: 1.0, y: 1.0}},
            {start: {x: 0.85, y: 0}, end: {x: 1.0, y: 0}},
            {start: {x: 0.85, y: -0.85}, end: {x: 1.0, y: -1.0}},
            {start: {x: 0, y: -0.85}, end: {x: 0, y: -1.0}},
            {start: {x: -0.85, y: -0.85}, end: {x: -1.0, y: -1.0}},
            {start: {x: -0.85, y: 0}, end: {x: -1.0, y: 0}},
            {start: {x: -0.78, y: 0.78}, end: {x: -0.9, y: 0.9}}
        ];

        // Initial generieren
        if (this.options.mode === 'grid') {
            this.generateNewPuzzle();
        }
    }

    /**
     * Generiert ein neues Rätsel
     */
    generateNewPuzzle() {
        const farben = ["light", "dark"];
        const formen = ["rund", "eckig"];
        const kritischeElemente = [...farben, ...formen];

        const kritischesElement = kritischeElemente[Math.floor(Math.random() * kritischeElemente.length)];
        
        let elemente = [];

        if (farben.includes(kritischesElement)) {
            const kritFarbe = kritischesElement;
            const andereFarbe = farben.find(f => f !== kritFarbe);

            for (let i = 0; i < 4; i++) {
                elemente.push({
                    farbe: kritFarbe,
                    form: formen[Math.floor(Math.random() * formen.length)]
                });
            }

            for (let i = 0; i < 5; i++) {
                elemente.push({
                    farbe: andereFarbe,
                    form: formen[Math.floor(Math.random() * formen.length)]
                });
            }
        } else {
            const kritForm = kritischesElement;
            const andereForm = formen.find(f => f !== kritForm);

            for (let i = 0; i < 4; i++) {
                elemente.push({
                    farbe: farben[Math.floor(Math.random() * farben.length)],
                    form: kritForm
                });
            }

            for (let i = 0; i < 5; i++) {
                elemente.push({
                    farbe: farben[Math.floor(Math.random() * farben.length)],
                    form: andereForm
                });
            }
        }

        const startNumber = Math.floor(Math.random() * 8) + 1;
        const pointers = elemente.map(() => Math.floor(Math.random() * 8));
        const pointersBereinigt = pointers.map(p => ((p + startNumber - 1) % 8) + 1);

        const indices = Array.from({length: 9}, (_, i) => i);
        for (let i = indices.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [indices[i], indices[j]] = [indices[j], indices[i]];
        }

        const korrekteValues = [];
        for (let i = 0; i < indices.length; i++) {
            if (indices[i] <= 3) {
                korrekteValues.push(pointersBereinigt[indices[i]]);
            }
        }
        korrekteValues.sort((a, b) => a - b);

        this.currentPuzzle = {
            kritischesElement,
            elemente,
            startNumber,
            pointers,
            pointersBereinigt,
            indices,
            korrekteValues,
            visibleNumbersPerClock: [] // Wird von außen gesetzt
        };

        this.render();
        return this.currentPuzzle;
    }

    /**
     * Zeigt eine einzelne Uhr an
     * @param {Object} config - Konfiguration der Uhr
     */
    showSingleClock(config) {
        const {
            startNumber = 1,
            pointerPosition = 0,
            visibleNumbers = [1, 2, 3, 4, 5, 6, 7, 8],
            theme = 'light',
            shape = 'rund'
        } = config;

        this.container.innerHTML = '';
        
        const canvas = document.createElement('canvas');
        canvas.width = this.options.clockSize;
        canvas.height = this.options.clockSize;
        
        const ctx = canvas.getContext('2d');
        const centerX = this.options.clockSize / 2;
        const centerY = this.options.clockSize / 2;
        const radius = this.options.clockSize * 0.4;

        ctx.fillStyle = '#FFFFFF';
        ctx.fillRect(0, 0, this.options.clockSize, this.options.clockSize);

        if (shape === 'rund') {
            this.drawRoundClock(ctx, centerX, centerY, radius, startNumber, pointerPosition, visibleNumbers, theme);
        } else {
            this.drawSquareClock(ctx, centerX, centerY, radius, startNumber, pointerPosition, visibleNumbers, theme);
        }

        this.container.appendChild(canvas);
    }

    /**
     * Rendert das aktuelle Rätsel
     */
    render() {
        if (!this.currentPuzzle) return;

        this.container.innerHTML = '';
        this.canvases = [];

        // Grid-Container erstellen
        const grid = document.createElement('div');
        grid.style.display = 'grid';
        grid.style.gridTemplateColumns = 'repeat(3, 1fr)';
        grid.style.gap = `${this.options.gap}px`;

        const centerX = this.options.clockSize / 2;
        const centerY = this.options.clockSize / 2;
        const radius = this.options.clockSize * 0.4;

        for (let i = 0; i < 9; i++) {
            const originalIndex = this.currentPuzzle.indices.indexOf(i);
            const element = this.currentPuzzle.elemente[originalIndex];
            const pointer = this.currentPuzzle.pointers[originalIndex];
            const isCritical = originalIndex < 4;

            const container = document.createElement('div');
            
            if (this.options.showBorders) {
                container.style.border = '3px solid #ddd';
                container.style.borderRadius = '10px';
                container.style.padding = '10px';
            }
            
            if (this.showCritical && isCritical) {
                container.style.border = '4px solid #28a745';
                container.style.boxShadow = '0 0 15px rgba(40, 167, 69, 0.3)';
            }

            const canvas = document.createElement('canvas');
            canvas.width = this.options.clockSize;
            canvas.height = this.options.clockSize;
            canvas.style.display = 'block';
            canvas.style.maxWidth = '100%';
            canvas.style.height = 'auto';
            
            const ctx = canvas.getContext('2d');
            
            ctx.fillStyle = '#FFFFFF';
            ctx.fillRect(0, 0, this.options.clockSize, this.options.clockSize);

            // visibleNumbers aus currentPuzzle lesen, falls vorhanden
            let visibleNumbers;
            if (this.currentPuzzle.visibleNumbersPerClock && this.currentPuzzle.visibleNumbersPerClock[originalIndex]) {
                visibleNumbers = this.currentPuzzle.visibleNumbersPerClock[originalIndex];
            } else {
                // Fallback: Standard-Verhalten
                visibleNumbers = element.form === 'rund'
                    ? [1, 2, 3, 4, 5, 6, 7, 8]
                    : [1, 5];
            }

            if (element.form === 'rund') {
                this.drawRoundClock(ctx, centerX, centerY, radius, this.currentPuzzle.startNumber, pointer, visibleNumbers, element.farbe);
            } else {
                this.drawSquareClock(ctx, centerX, centerY, radius, this.currentPuzzle.startNumber, pointer, visibleNumbers, element.farbe);
            }

            container.appendChild(canvas);
            grid.appendChild(container);
            this.canvases.push({canvas, container, isCritical});
        }

        this.container.appendChild(grid);
    }

    /**
     * Zeichnet eine runde Uhr
     */
    drawRoundClock(ctx, centerX, centerY, radius, startNumber, pointerPosition, visibleNumbers, theme) {
        const bgColor = theme === 'dark' ? '#000000' : '#FFFFFF';
        const fgColor = theme === 'dark' ? '#FFFFFF' : '#000000';

        const numbers = [];
        for (let i = 0; i < 8; i++) {
            numbers.push((startNumber + i - 1) % 8 + 1);
        }

        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
        ctx.fillStyle = bgColor;
        ctx.fill();
        ctx.strokeStyle = fgColor;
        ctx.lineWidth = 4;
        ctx.stroke();

        const rText = 0.7 * radius;
        const rTickInner = 0.9 * radius;
        const rTickOuter = 1.02 * radius;

        for (let i = 0; i < 8; i++) {
            const num = numbers[i];
            const angle = this.angles[i];

            if (visibleNumbers.includes(num)) {
                const x = centerX + rText * Math.cos(angle);
                const y = centerY - rText * Math.sin(angle);

                ctx.fillStyle = fgColor;
                ctx.font = 'bold 28px Arial';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(num, x, y);
            } else {
                const x1 = centerX + rTickInner * Math.cos(angle);
                const y1 = centerY - rTickInner * Math.sin(angle);
                const x2 = centerX + rTickOuter * Math.cos(angle);
                const y2 = centerY - rTickOuter * Math.sin(angle);

                ctx.beginPath();
                ctx.moveTo(x1, y1);
                ctx.lineTo(x2, y2);
                ctx.strokeStyle = fgColor;
                ctx.lineWidth = 3;
                ctx.stroke();
            }
        }

        const pointerAngle = this.angles[pointerPosition];
        const pointerLength = 0.5 * radius;
        const px = centerX + pointerLength * Math.cos(pointerAngle);
        const py = centerY - pointerLength * Math.sin(pointerAngle);

        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(px, py);
        ctx.strokeStyle = fgColor;
        ctx.lineWidth = 4;
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(centerX, centerY, 10, 0, 2 * Math.PI);
        ctx.fillStyle = fgColor;
        ctx.fill();
    }

    /**
     * Zeichnet eine quadratische Uhr
     */
    drawSquareClock(ctx, centerX, centerY, radius, startNumber, pointerPosition, visibleNumbers, theme) {
        const bgColor = theme === 'dark' ? '#000000' : '#FFFFFF';
        const fgColor = theme === 'dark' ? '#FFFFFF' : '#000000';

        const numbers = [];
        for (let i = 0; i < 8; i++) {
            numbers.push((startNumber + i - 1) % 8 + 1);
        }

        const squareSize = 2 * radius;
        const squareX = centerX - squareSize / 2;
        const squareY = centerY - squareSize / 2;

        ctx.fillStyle = bgColor;
        ctx.fillRect(squareX, squareY, squareSize, squareSize);
        ctx.strokeStyle = fgColor;
        ctx.lineWidth = 4;
        ctx.strokeRect(squareX, squareY, squareSize, squareSize);

        for (let i = 0; i < 8; i++) {
            const num = numbers[i];
            const pos = this.squarePositions[i];

            if (visibleNumbers.includes(num)) {
                const x = centerX + pos.x * radius;
                const y = centerY - pos.y * radius;

                ctx.fillStyle = fgColor;
                ctx.font = 'bold 28px Arial';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText(num, x, y);
            } else {
                const tickPos = this.squareTickPositions[i];
                const x1 = centerX + tickPos.start.x * radius;
                const y1 = centerY - tickPos.start.y * radius;
                const x2 = centerX + tickPos.end.x * radius;
                const y2 = centerY - tickPos.end.y * radius;

                ctx.beginPath();
                ctx.moveTo(x1, y1);
                ctx.lineTo(x2, y2);
                ctx.strokeStyle = fgColor;
                ctx.lineWidth = 4;
                ctx.stroke();
            }
        }

        const pointerAngle = this.angles[pointerPosition];
        const pointerLength = 0.4 * radius;
        const px = centerX + pointerLength * Math.cos(pointerAngle);
        const py = centerY - pointerLength * Math.sin(pointerAngle);

        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(px, py);
        ctx.strokeStyle = fgColor;
        ctx.lineWidth = 3;
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(centerX, centerY, 10, 0, 2 * Math.PI);
        ctx.fillStyle = fgColor;
        ctx.fill();
    }

    /**
     * Schaltet die Markierung der kritischen Uhren um
     */
    toggleCriticalHighlight() {
        this.showCritical = !this.showCritical;
        this.render();
        return this.showCritical;
    }

    /**
     * Setzt die Markierung der kritischen Uhren
     */
    setCriticalHighlight(show) {
        this.showCritical = show;
        this.render();
    }

    /**
     * Gibt Informationen über das aktuelle Rätsel zurück
     */
    getPuzzleInfo() {
        if (!this.currentPuzzle) return null;
        
        return {
            kritischesElement: this.currentPuzzle.kritischesElement,
            startNumber: this.currentPuzzle.startNumber,
            solution: this.currentPuzzle.korrekteValues
        };
    }

    /**
     * Setzt die Optionen neu
     */
    setOptions(newOptions) {
        this.options = { ...this.options, ...newOptions };
        if (this.currentPuzzle) {
            this.render();
        }
    }
}

// Für Browser-Umgebung als globale Variable
if (typeof window !== 'undefined') {
    window.ClockPuzzle = ClockPuzzle;
}

// Für Node.js / Module
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ClockPuzzle;
}
