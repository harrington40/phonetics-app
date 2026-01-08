/**
 * Kids Learning Activity Graphics System
 * Provides engaging visual illustrations for phonetics learning activities
 * Optimized for child attention and comprehension
 */

class ActivityGraphics {
    constructor() {
        this.svgNS = "http://www.w3.org/2000/svg";
        this.colors = {
            primary: '#B39DDB',
            secondary: '#81C784',
            accent: '#FFAB91',
            warning: '#FFC107',
            success: '#4CAF50',
            gold: '#FFD700',
            orange: '#FF9800',
            pink: '#FF69B4',
            lightBlue: '#BBDEFB',
            lightGreen: '#C8E6C9',
            lightOrange: '#FCE8D6'
        };
    }

    /**
     * Create SVG element for "Listen & Choose" activity
     */
    createListenChooseGraphic(container, phoneme = null) {
        const svg = this.createSVG(300, 300);
        
        // Background circle
        const bgCircle = document.createElementNS(this.svgNS, 'circle');
        bgCircle.setAttribute('cx', '150');
        bgCircle.setAttribute('cy', '150');
        bgCircle.setAttribute('r', '140');
        bgCircle.setAttribute('fill', this.colors.primary);
        bgCircle.setAttribute('opacity', '0.2');
        svg.appendChild(bgCircle);
        
        // Happy character
        this.drawCharacter(svg, 150, 80, '#FFD700');
        
        // Musical notes
        const note1 = document.createElementNS(this.svgNS, 'text');
        note1.setAttribute('x', '80');
        note1.setAttribute('y', '60');
        note1.setAttribute('font-size', '35');
        note1.setAttribute('text-anchor', 'middle');
        note1.textContent = '♪';
        svg.appendChild(note1);
        
        const note2 = document.createElementNS(this.svgNS, 'text');
        note2.setAttribute('x', '220');
        note2.setAttribute('y', '70');
        note2.setAttribute('font-size', '35');
        note2.setAttribute('text-anchor', 'middle');
        note2.textContent = '♫';
        svg.appendChild(note2);
        
        // Speaker icon with click handler
        const speakerGroup = document.createElementNS(this.svgNS, 'g');
        speakerGroup.style.cursor = 'pointer';
        
        const speaker = document.createElementNS(this.svgNS, 'rect');
        speaker.setAttribute('x', '130');
        speaker.setAttribute('y', '140');
        speaker.setAttribute('width', '40');
        speaker.setAttribute('height', '50');
        speaker.setAttribute('rx', '5');
        speaker.setAttribute('fill', this.colors.primary);
        speakerGroup.appendChild(speaker);
        
        // Add click interaction
        speakerGroup.addEventListener('click', () => {
            this.speakWord(phoneme);
            speakerGroup.style.transform = 'scale(1.2)';
            setTimeout(() => {
                speakerGroup.style.transform = '';
            }, 200);
        });
        
        speakerGroup.addEventListener('mouseenter', () => {
            speaker.setAttribute('opacity', '0.8');
        });
        speakerGroup.addEventListener('mouseleave', () => {
            speaker.setAttribute('opacity', '1');
        });
        
        svg.appendChild(speakerGroup);
        
        // Sound waves
        for (let i = 1; i <= 2; i++) {
            const wave = document.createElementNS(this.svgNS, 'circle');
            wave.setAttribute('cx', '150');
            wave.setAttribute('cy', '165');
            wave.setAttribute('r', 20 + (i * 15));
            wave.setAttribute('fill', 'none');
            wave.setAttribute('stroke', this.colors.secondary);
            wave.setAttribute('stroke-width', '2');
            wave.setAttribute('opacity', 0.8 - (i * 0.2));
            wave.setAttribute('class', 'sound-wave-pulse');
            svg.appendChild(wave);
        }
        
        // Label with click handler
        const label = document.createElementNS(this.svgNS, 'text');
        label.setAttribute('x', '150');
        label.setAttribute('y', '260');
        label.setAttribute('font-size', '18');
        label.setAttribute('font-weight', 'bold');
        label.setAttribute('text-anchor', 'middle');
        label.setAttribute('fill', '#333');
        label.textContent = '🎵 Tap to Answer';
        label.style.cursor = 'pointer';
        
        label.addEventListener('click', () => {
            this.speakWord(phoneme);
            label.style.transform = 'scale(1.1)';
            setTimeout(() => {
                label.style.transform = '';
            }, 200);
        });
        
        svg.appendChild(label);
        
        container.appendChild(svg);
        return svg;
    }

    /**
     * Create SVG element for "Build Word" activity
     */
    createBuildWordGraphic(container, letters = ['C', 'A', 'T']) {
        const svg = this.createSVG(300, 300);
        
        // Background
        const bgCircle = document.createElementNS(this.svgNS, 'circle');
        bgCircle.setAttribute('cx', '150');
        bgCircle.setAttribute('cy', '150');
        bgCircle.setAttribute('r', '140');
        bgCircle.setAttribute('fill', this.colors.secondary);
        bgCircle.setAttribute('opacity', '0.2');
        svg.appendChild(bgCircle);
        
        // Happy builder character
        this.drawCharacter(svg, 150, 60, '#FF9800');
        
        // Letter blocks
        const blockColors = [this.colors.accent, this.colors.secondary, this.colors.primary];
        const startX = 60;
        const blockSize = 50;
        const spacing = 65;
        
        letters.forEach((letter, index) => {
            const group = document.createElementNS(this.svgNS, 'g');
            group.setAttribute('class', 'letter-block-group');
            group.style.cursor = 'pointer';
            group.setAttribute('data-letter', letter);
            
            const rect = document.createElementNS(this.svgNS, 'rect');
            rect.setAttribute('x', startX + (index * spacing));
            rect.setAttribute('y', 130);
            rect.setAttribute('width', blockSize);
            rect.setAttribute('height', blockSize);
            rect.setAttribute('rx', '8');
            rect.setAttribute('fill', blockColors[index % blockColors.length]);
            rect.setAttribute('class', 'letter-block');
            group.appendChild(rect);
            
            const text = document.createElementNS(this.svgNS, 'text');
            text.setAttribute('x', startX + blockSize / 2 + (index * spacing));
            text.setAttribute('y', 165);
            text.setAttribute('font-size', '28');
            text.setAttribute('font-weight', 'bold');
            text.setAttribute('text-anchor', 'middle');
            text.setAttribute('fill', 'white');
            text.textContent = letter;
            text.style.pointerEvents = 'none';
            group.appendChild(text);
            
            // Add click handler to speak the letter
            group.addEventListener('click', () => {
                this.speakLetter(letter);
                // Animate on click
                group.style.transform = 'scale(1.2)';
                setTimeout(() => {
                    group.style.transform = '';
                }, 200);
            });
            
            // Add hover effect
            group.addEventListener('mouseenter', () => {
                rect.setAttribute('opacity', '0.8');
            });
            group.addEventListener('mouseleave', () => {
                rect.setAttribute('opacity', '1');
            });
            
            svg.appendChild(group);
        });
        
        // Result word display with click handler
        const resultGroup = document.createElementNS(this.svgNS, 'g');
        resultGroup.style.cursor = 'pointer';
        
        const resultBg = document.createElementNS(this.svgNS, 'rect');
        resultBg.setAttribute('x', '80');
        resultBg.setAttribute('y', '210');
        resultBg.setAttribute('width', '140');
        resultBg.setAttribute('height', '50');
        resultBg.setAttribute('rx', '8');
        resultBg.setAttribute('fill', this.colors.warning);
        resultGroup.appendChild(resultBg);
        
        const resultText = document.createElementNS(this.svgNS, 'text');
        resultText.setAttribute('x', '150');
        resultText.setAttribute('y', '245');
        resultText.setAttribute('font-size', '24');
        resultText.setAttribute('font-weight', 'bold');
        resultText.setAttribute('text-anchor', 'middle');
        resultText.setAttribute('fill', '#333');
        resultText.textContent = letters.join('');
        resultText.style.pointerEvents = 'none';
        resultGroup.appendChild(resultText);
        
        // Add click handler to speak the whole word
        const word = letters.join('');
        resultGroup.addEventListener('click', () => {
            this.speakWord(word);
            // Animate on click
            resultGroup.style.transform = 'scale(1.15)';
            setTimeout(() => {
                resultGroup.style.transform = '';
            }, 300);
        });
        
        // Add hover effect
        resultGroup.addEventListener('mouseenter', () => {
            resultBg.setAttribute('opacity', '0.8');
        });
        resultGroup.addEventListener('mouseleave', () => {
            resultBg.setAttribute('opacity', '1');
        });
        
        svg.appendChild(resultGroup);
        
        // Label
        const label = document.createElementNS(this.svgNS, 'text');
        label.setAttribute('x', '150');
        label.setAttribute('y', '285');
        label.setAttribute('font-size', '16');
        label.setAttribute('font-weight', 'bold');
        label.setAttribute('text-anchor', 'middle');
        label.setAttribute('fill', '#333');
        label.textContent = '🔤 Drag Letters';
        svg.appendChild(label);
        
        container.appendChild(svg);
        return svg;
    }

    /**
     * Create SVG element for "Read & Pick" activity
     */
    createReadPickGraphic(container) {
        const svg = this.createSVG(300, 300);
        
        // Background
        const bgCircle = document.createElementNS(this.svgNS, 'circle');
        bgCircle.setAttribute('cx', '150');
        bgCircle.setAttribute('cy', '150');
        bgCircle.setAttribute('r', '140');
        bgCircle.setAttribute('fill', this.colors.warning);
        bgCircle.setAttribute('opacity', '0.2');
        svg.appendChild(bgCircle);
        
        // Reading character
        this.drawCharacter(svg, 150, 50, '#FF69B4');
        
        // Book with click handlers
        const bookGroup = document.createElementNS(this.svgNS, 'g');
        bookGroup.style.cursor = 'pointer';
        
        const bookLeft = document.createElementNS(this.svgNS, 'rect');
        bookLeft.setAttribute('x', '100');
        bookLeft.setAttribute('y', '100');
        bookLeft.setAttribute('width', '50');
        bookLeft.setAttribute('height', '80');
        bookLeft.setAttribute('rx', '5');
        bookLeft.setAttribute('fill', this.colors.primary);
        bookGroup.appendChild(bookLeft);
        
        const bookRight = document.createElementNS(this.svgNS, 'rect');
        bookRight.setAttribute('x', '150');
        bookRight.setAttribute('y', '100');
        bookRight.setAttribute('width', '50');
        bookRight.setAttribute('height', '80');
        bookRight.setAttribute('rx', '5');
        bookRight.setAttribute('fill', this.colors.accent);
        bookGroup.appendChild(bookRight);
        
        // Make book clickable to read
        bookGroup.addEventListener('click', () => {
            this.speakWord('Read the book');
            bookGroup.style.transform = 'scale(1.1)';
            setTimeout(() => {
                bookGroup.style.transform = '';
            }, 300);
        });
        
        bookGroup.addEventListener('mouseenter', () => {
            bookLeft.setAttribute('opacity', '0.8');
            bookRight.setAttribute('opacity', '0.8');
        });
        bookGroup.addEventListener('mouseleave', () => {
            bookLeft.setAttribute('opacity', '1');
            bookRight.setAttribute('opacity', '1');
        });
        
        svg.appendChild(bookGroup);
        
        // Book spine
        const spine = document.createElementNS(this.svgNS, 'line');
        spine.setAttribute('x1', '150');
        spine.setAttribute('y1', '100');
        spine.setAttribute('x2', '150');
        spine.setAttribute('y2', '180');
        spine.setAttribute('stroke', '#999');
        spine.setAttribute('stroke-width', '2');
        svg.appendChild(spine);
        
        // Words in book with click handlers
        const word1 = document.createElementNS(this.svgNS, 'text');
        word1.setAttribute('x', '125');
        word1.setAttribute('y', '130');
        word1.setAttribute('font-size', '16');
        word1.setAttribute('text-anchor', 'middle');
        word1.setAttribute('fill', 'white');
        word1.textContent = 'dog';
        word1.style.cursor = 'pointer';
        word1.addEventListener('click', () => {
            this.speakWord('dog');
            word1.style.transform = 'scale(1.2)';
            setTimeout(() => word1.style.transform = '', 200);
        });
        word1.addEventListener('mouseenter', () => word1.setAttribute('opacity', '0.7'));
        word1.addEventListener('mouseleave', () => word1.setAttribute('opacity', '1'));
        svg.appendChild(word1);
        
        const word2 = document.createElementNS(this.svgNS, 'text');
        word2.setAttribute('x', '175');
        word2.setAttribute('y', '150');
        word2.setAttribute('font-size', '16');
        word2.setAttribute('text-anchor', 'middle');
        word2.setAttribute('fill', 'white');
        word2.textContent = 'cat';
        word2.style.cursor = 'pointer';
        word2.addEventListener('click', () => {
            this.speakWord('cat');
            word2.style.transform = 'scale(1.2)';
            setTimeout(() => word2.style.transform = '', 200);
        });
        word2.addEventListener('mouseenter', () => word2.setAttribute('opacity', '0.7'));
        word2.addEventListener('mouseleave', () => word2.setAttribute('opacity', '1'));
        svg.appendChild(word2);
        
        // Images on right
        this.drawSimpleAnimal(svg, 175, 160, 'cat');
        
        // Label with click handler
        const label = document.createElementNS(this.svgNS, 'text');
        label.setAttribute('x', '150');
        label.setAttribute('y', '285');
        label.setAttribute('font-size', '16');
        label.setAttribute('font-weight', 'bold');
        label.setAttribute('text-anchor', 'middle');
        label.setAttribute('fill', '#333');
        label.textContent = '📖 Tap Picture';
        label.style.cursor = 'pointer';
        label.addEventListener('click', () => {
            this.speakWord('Tap the picture to hear the word');
            label.style.transform = 'scale(1.1)';
            setTimeout(() => label.style.transform = '', 200);
        });
        svg.appendChild(label);
        
        container.appendChild(svg);
        return svg;
    }

    /**
     * Create celebration/reward graphic
     */
    createRewardGraphic(container, score = 100) {
        const svg = this.createSVG(300, 300);
        
        // Background with gradient effect
        const bgCircle = document.createElementNS(this.svgNS, 'circle');
        bgCircle.setAttribute('cx', '150');
        bgCircle.setAttribute('cy', '150');
        bgCircle.setAttribute('r', '140');
        bgCircle.setAttribute('fill', this.colors.gold);
        bgCircle.setAttribute('opacity', '0.2');
        svg.appendChild(bgCircle);
        
        // Celebrating character
        this.drawCharacter(svg, 150, 80, '#FF6B9D');
        
        // Trophy
        this.drawTrophy(svg, 150, 170);
        
        // Stars
        this.drawStar(svg, 80, 100, 20);
        this.drawStar(svg, 220, 110, 20);
        this.drawStar(svg, 150, 50, 25);
        
        // Sparkles with click handlers
        const sparkle1 = document.createElementNS(this.svgNS, 'text');
        sparkle1.setAttribute('x', '100');
        sparkle1.setAttribute('y', '140');
        sparkle1.setAttribute('font-size', '30');
        sparkle1.textContent = '✨';
        sparkle1.style.cursor = 'pointer';
        sparkle1.addEventListener('click', () => {
            this.speakWord('Sparkle!');
            sparkle1.style.transform = 'scale(1.5) rotate(360deg)';
            sparkle1.style.transition = 'transform 0.5s';
            setTimeout(() => {
                sparkle1.style.transform = '';
            }, 500);
        });
        svg.appendChild(sparkle1);
        
        const sparkle2 = document.createElementNS(this.svgNS, 'text');
        sparkle2.setAttribute('x', '200');
        sparkle2.setAttribute('y', '160');
        sparkle2.setAttribute('font-size', '30');
        sparkle2.textContent = '🌟';
        sparkle2.style.cursor = 'pointer';
        sparkle2.addEventListener('click', () => {
            this.speakWord('You are a star!');
            sparkle2.style.transform = 'scale(1.5) rotate(-360deg)';
            sparkle2.style.transition = 'transform 0.5s';
            setTimeout(() => {
                sparkle2.style.transform = '';
            }, 500);
        });
        svg.appendChild(sparkle2);
        
        // Score text
        const scoreText = document.createElementNS(this.svgNS, 'text');
        scoreText.setAttribute('x', '150');
        scoreText.setAttribute('y', '265');
        scoreText.setAttribute('font-size', '24');
        scoreText.setAttribute('font-weight', 'bold');
        scoreText.setAttribute('text-anchor', 'middle');
        scoreText.setAttribute('fill', '#333');
        scoreText.textContent = `${score}%`;
        svg.appendChild(scoreText);
        
        // Label with click handler
        const label = document.createElementNS(this.svgNS, 'text');
        label.setAttribute('x', '150');
        label.setAttribute('y', '290');
        label.setAttribute('font-size', '14');
        label.setAttribute('text-anchor', 'middle');
        label.setAttribute('fill', '#666');
        label.textContent = '🏆 Great Job!';
        label.style.cursor = 'pointer';
        label.addEventListener('click', () => {
            this.speakWord('Great job! You did amazing!');
            label.style.transform = 'scale(1.2)';
            setTimeout(() => label.style.transform = '', 300);
        });
        svg.appendChild(label);
        
        container.appendChild(svg);
        return svg;
    }

    /**
     * Create progress/mastery visualization
     */
    createProgressPlant(container, masteryPercent = 50) {
        const svg = this.createSVG(300, 300);
        
        // Background
        const bgCircle = document.createElementNS(this.svgNS, 'circle');
        bgCircle.setAttribute('cx', '150');
        bgCircle.setAttribute('cy', '150');
        bgCircle.setAttribute('r', '140');
        bgCircle.setAttribute('fill', this.colors.secondary);
        bgCircle.setAttribute('opacity', '0.2');
        svg.appendChild(bgCircle);
        
        // Soil
        const soil = document.createElementNS(this.svgNS, 'ellipse');
        soil.setAttribute('cx', '150');
        soil.setAttribute('cy', '240');
        soil.setAttribute('rx', '30');
        soil.setAttribute('ry', '15');
        soil.setAttribute('fill', '#8B4513');
        svg.appendChild(soil);
        
        // Growing plant based on mastery
        const stage = Math.min(3, Math.floor(masteryPercent / 33));
        
        // Stem with click handler
        const stem = document.createElementNS(this.svgNS, 'line');
        stem.setAttribute('x1', '150');
        stem.setAttribute('y1', stage === 0 ? 220 : 200);
        stem.setAttribute('x2', '150');
        stem.setAttribute('y2', 100 - (stage * 20));
        stem.setAttribute('stroke', '#558B2F');
        stem.setAttribute('stroke-width', 4 + stage);
        stem.style.cursor = 'pointer';
        stem.addEventListener('click', () => {
            this.speakWord(`Your plant is growing! ${masteryPercent} percent complete`);
        });
        svg.appendChild(stem);
        
        // Leaves based on stage
        if (stage >= 1) {
            this.drawLeaf(svg, 130, 180, this.colors.secondary);
            this.drawLeaf(svg, 170, 185, this.colors.secondary);
        }
        
        if (stage >= 2) {
            this.drawLeaf(svg, 125, 140, '#7CB342');
            this.drawLeaf(svg, 175, 145, '#7CB342');
        }
        
        if (stage >= 3) {
            // Flower
            this.drawFlower(svg, 150, 80);
        }
        
        // Progress bar
        const progressBg = document.createElementNS(this.svgNS, 'rect');
        progressBg.setAttribute('x', '50');
        progressBg.setAttribute('y', '260');
        progressBg.setAttribute('width', '200');
        progressBg.setAttribute('height', '20');
        progressBg.setAttribute('rx', '10');
        progressBg.setAttribute('fill', '#f0f0f0');
        svg.appendChild(progressBg);
        
        const progressFill = document.createElementNS(this.svgNS, 'rect');
        progressFill.setAttribute('x', '50');
        progressFill.setAttribute('y', '260');
        progressFill.setAttribute('width', 200 * (masteryPercent / 100));
        progressFill.setAttribute('height', '20');
        progressFill.setAttribute('rx', '10');
        progressFill.setAttribute('fill', this.colors.secondary);
        svg.appendChild(progressFill);
        
        // Percentage text
        const percentText = document.createElementNS(this.svgNS, 'text');
        percentText.setAttribute('x', '150');
        percentText.setAttribute('y', '274');
        percentText.setAttribute('font-size', '12');
        percentText.setAttribute('font-weight', 'bold');
        percentText.setAttribute('text-anchor', 'middle');
        percentText.setAttribute('fill', '#333');
        percentText.textContent = `${masteryPercent}%`;
        svg.appendChild(percentText);
        
        container.appendChild(svg);
        return svg;
    }

    // Helper methods

    createSVG(width, height) {
        const svg = document.createElementNS(this.svgNS, 'svg');
        svg.setAttribute('viewBox', `0 0 ${width} ${height}`);
        svg.setAttribute('width', '100%');
        svg.setAttribute('height', 'auto');
        return svg;
    }

    drawCharacter(svg, x, y, faceColor) {
        // Face
        const face = document.createElementNS(this.svgNS, 'circle');
        face.setAttribute('cx', x);
        face.setAttribute('cy', y);
        face.setAttribute('r', '35');
        face.setAttribute('fill', faceColor);
        svg.appendChild(face);
        
        // Eyes
        const eye1 = document.createElementNS(this.svgNS, 'circle');
        eye1.setAttribute('cx', x - 15);
        eye1.setAttribute('cy', y - 10);
        eye1.setAttribute('r', '5');
        eye1.setAttribute('fill', '#333');
        svg.appendChild(eye1);
        
        const eye2 = document.createElementNS(this.svgNS, 'circle');
        eye2.setAttribute('cx', x + 15);
        eye2.setAttribute('cy', y - 10);
        eye2.setAttribute('r', '5');
        eye2.setAttribute('fill', '#333');
        svg.appendChild(eye2);
        
        // Smile
        const smile = document.createElementNS(this.svgNS, 'path');
        smile.setAttribute('d', `M ${x - 20} ${y + 10} Q ${x} ${y + 25} ${x + 20} ${y + 10}`);
        smile.setAttribute('stroke', '#333');
        smile.setAttribute('stroke-width', '3');
        smile.setAttribute('fill', 'none');
        smile.setAttribute('stroke-linecap', 'round');
        svg.appendChild(smile);
    }

    drawSimpleAnimal(svg, x, y, type) {
        if (type === 'cat') {
            // Cat head
            const head = document.createElementNS(this.svgNS, 'circle');
            head.setAttribute('cx', x);
            head.setAttribute('cy', y);
            head.setAttribute('r', '12');
            head.setAttribute('fill', '#FF9800');
            svg.appendChild(head);
            
            // Ears
            const ear1 = document.createElementNS(this.svgNS, 'polygon');
            ear1.setAttribute('points', `${x-5},${y-15} ${x-10},${y-5} ${x},${y-10}`);
            ear1.setAttribute('fill', '#FF9800');
            svg.appendChild(ear1);
            
            const ear2 = document.createElementNS(this.svgNS, 'polygon');
            ear2.setAttribute('points', `${x+5},${y-15} ${x+10},${y-5} ${x},${y-10}`);
            ear2.setAttribute('fill', '#FF9800');
            svg.appendChild(ear2);
        }
    }

    drawTrophy(svg, x, y) {
        // Cup
        const cup = document.createElementNS(this.svgNS, 'rect');
        cup.setAttribute('x', x - 25);
        cup.setAttribute('y', y);
        cup.setAttribute('width', '50');
        cup.setAttribute('height', '40');
        cup.setAttribute('rx', '3');
        cup.setAttribute('fill', this.colors.gold);
        svg.appendChild(cup);
        
        // Base
        const base = document.createElementNS(this.svgNS, 'rect');
        base.setAttribute('x', x - 15);
        base.setAttribute('y', y + 40);
        base.setAttribute('width', '30');
        base.setAttribute('height', '8');
        base.setAttribute('fill', this.colors.gold);
        svg.appendChild(base);
    }

    drawStar(svg, x, y, size) {
        const points = [];
        for (let i = 0; i < 5; i++) {
            const angle = (i * 4 * Math.PI) / 5 - Math.PI / 2;
            points.push([
                x + size * Math.cos(angle),
                y + size * Math.sin(angle)
            ]);
        }
        
        const star = document.createElementNS(this.svgNS, 'polygon');
        star.setAttribute('points', points.map(p => p.join(',')).join(' '));
        star.setAttribute('fill', this.colors.gold);
        svg.appendChild(star);
    }

    drawFlower(svg, x, y) {
        // Petals
        const petals = 5;
        const petalRadius = 15;
        
        for (let i = 0; i < petals; i++) {
            const angle = (i * 2 * Math.PI) / petals;
            const px = x + petalRadius * Math.cos(angle);
            const py = y + petalRadius * Math.sin(angle);
            
            const petal = document.createElementNS(this.svgNS, 'circle');
            petal.setAttribute('cx', px);
            petal.setAttribute('cy', py);
            petal.setAttribute('r', '10');
            petal.setAttribute('fill', '#FF1493');
            svg.appendChild(petal);
        }
        
        // Center
        const center = document.createElementNS(this.svgNS, 'circle');
        center.setAttribute('cx', x);
        center.setAttribute('cy', y);
        center.setAttribute('r', '8');
        center.setAttribute('fill', this.colors.gold);
        svg.appendChild(center);
    }

    drawLeaf(svg, x, y, color) {
        const leaf = document.createElementNS(this.svgNS, 'ellipse');
        leaf.setAttribute('cx', x);
        leaf.setAttribute('cy', y);
        leaf.setAttribute('rx', '10');
        leaf.setAttribute('ry', '18');
        leaf.setAttribute('fill', color);
        svg.appendChild(leaf);
    }
    
    /**
     * Speak a single letter using Web Speech API
     */
    speakLetter(letter) {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(letter);
            utterance.rate = 0.8; // Slower for clarity
            utterance.pitch = 1.2; // Slightly higher pitch for kids
            utterance.volume = 1;
            speechSynthesis.cancel(); // Cancel any ongoing speech
            speechSynthesis.speak(utterance);
        } else {
            console.log('Speech: ' + letter);
        }
    }
    
    /**
     * Speak a whole word using Web Speech API
     */
    speakWord(word) {
        if ('speechSynthesis' in window) {
            const utterance = new SpeechSynthesisUtterance(word);
            utterance.rate = 0.7; // Even slower for whole words
            utterance.pitch = 1.1;
            utterance.volume = 1;
            speechSynthesis.cancel(); // Cancel any ongoing speech
            speechSynthesis.speak(utterance);
        } else {
            console.log('Speech: ' + word);
        }
    }
}

// Export for use in web pages
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ActivityGraphics;
}
