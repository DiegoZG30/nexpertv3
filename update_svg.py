import re

html_svg = """            <div class="consulting-diagram reveal" style="width: 100%; max-width: 1200px; margin: 0 auto; padding: 2rem 0; overflow: visible;">
                <svg viewBox="0 0 1000 400" style="width: 100%; height: auto; filter: drop-shadow(0 25px 25px rgba(0,0,0,0.15)); font-family: var(--font-primary, sans-serif);">
                    <defs>
                        <!-- Filtros de Resplandor Neón -->
                        <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
                            <feGaussianBlur stdDeviation="4" result="blur" />
                            <feMerge>
                                <feMergeNode in="blur" />
                                <feMergeNode in="blur" />
                                <feMergeNode in="SourceGraphic" />
                            </feMerge>
                        </filter>
                        <filter id="heavyGlow" x="-50%" y="-50%" width="200%" height="200%">
                            <feGaussianBlur stdDeviation="8" result="blur" />
                            <feMerge>
                                <feMergeNode in="blur" />
                                <feMergeNode in="SourceGraphic" />
                            </feMerge>
                        </filter>

                        <!-- Gradientes para los fondos de los contenedores -->
                        <linearGradient id="boxGradLeft" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stop-color="rgba(4, 18, 40, 0.8)" />
                            <stop offset="100%" stop-color="rgba(0, 160, 255, 0.15)" />
                        </linearGradient>
                        <linearGradient id="boxGradRight" x1="100%" y1="0%" x2="0%" y2="0%">
                            <stop offset="0%" stop-color="rgba(4, 18, 40, 0.8)" />
                            <stop offset="100%" stop-color="rgba(0, 160, 255, 0.15)" />
                        </linearGradient>

                        <!-- Gradiente principal del Hexágono Central -->
                        <linearGradient id="hexGrad" x1="0%" y1="0%" x2="0%" y2="100%">
                            <stop offset="0%" stop-color="#083863" />
                            <stop offset="50%" stop-color="#0a5291" />
                            <stop offset="100%" stop-color="#041830" />
                        </linearGradient>

                        <!-- Gradiente para la flecha central -->
                        <linearGradient id="arrowGrad" x1="0%" y1="100%" x2="0%" y2="0%">
                            <stop offset="0%" stop-color="#0066ff" />
                            <stop offset="100%" stop-color="#00d2ff" />
                        </linearGradient>
                    </defs>

                    <!-- FONDOS Y EFECTOS ESTELARES -->
                    <g opacity="0.4">
                        <circle cx="150" cy="80" r="1.5" fill="#00d2ff" filter="url(#glow)" />
                        <circle cx="850" cy="320" r="1.5" fill="#00d2ff" filter="url(#glow)" />
                        <circle cx="50" cy="200" r="1" fill="#fff" />
                        <circle cx="950" cy="100" r="1" fill="#fff" />
                        <circle cx="280" cy="360" r="2" fill="#00d2ff" filter="url(#glow)" opacity="0.5"/>
                        <circle cx="720" cy="60" r="2" fill="#00d2ff" filter="url(#glow)" opacity="0.5"/>
                    </g>

                    <!-- LÍNEAS DE CIRCUITO (Conectando cajas al hexágono) -->
                    <g stroke="#00d2ff" fill="none" opacity="0.75" filter="url(#glow)">
                        <!-- Izquierda -->
                        <path d="M 350 90 L 370 90 L 400 110 L 416 110" stroke-width="1.5" />
                        <circle cx="350" cy="90" r="2" fill="#00d2ff" />
                        <circle cx="416" cy="110" r="2" fill="#00d2ff" />
                        <path d="M 350 110 L 380 110 L 400 130 L 405 130" stroke-width="1.5" />
                        <circle cx="350" cy="110" r="2" fill="#00d2ff" />
                        <circle cx="405" cy="130" r="2" fill="#00d2ff" />
                        <path d="M 335 145 L 360 145 L 380 160 L 393 160" stroke-width="1.5" />
                        <circle cx="335" cy="145" r="2" fill="#00d2ff" />
                        <circle cx="393" cy="160" r="2" fill="#00d2ff" />
                        <path d="M 320 170 L 350 170 L 370 185 L 385 185" stroke-width="1.5" />
                        <circle cx="320" cy="170" r="2" fill="#00d2ff" />
                        <circle cx="385" cy="185" r="2" fill="#00d2ff" />
                        <path d="M 320 190 L 360 190 L 375 200" stroke-width="1.5" />
                        <circle cx="320" cy="190" r="2" fill="#00d2ff" />
                        <circle cx="375" cy="200" r="2" fill="#00d2ff" />
                        <path d="M 320 210 L 350 210 L 370 200" stroke-width="1.5" />
                        <circle cx="320" cy="210" r="2" fill="#00d2ff" />
                        <circle cx="370" cy="200" r="2" fill="#00d2ff" />
                        <path d="M 320 230 L 340 230 L 360 215 L 385 215" stroke-width="1.5" />
                        <circle cx="320" cy="230" r="2" fill="#00d2ff" />
                        <circle cx="385" cy="215" r="2" fill="#00d2ff" />
                        <path d="M 335 255 L 360 255 L 380 240 L 393 240" stroke-width="1.5" />
                        <circle cx="335" cy="255" r="2" fill="#00d2ff" />
                        <circle cx="393" cy="240" r="2" fill="#00d2ff" />
                        <path d="M 350 290 L 380 290 L 400 270 L 405 270" stroke-width="1.5" />
                        <circle cx="350" cy="290" r="2" fill="#00d2ff" />
                        <circle cx="405" cy="270" r="2" fill="#00d2ff" />
                        <path d="M 350 310 L 370 310 L 400 290 L 416 290" stroke-width="1.5" />
                        <circle cx="350" cy="310" r="2" fill="#00d2ff" />
                        <circle cx="416" cy="290" r="2" fill="#00d2ff" />
                        
                        <!-- Derecha -->
                        <path d="M 650 90 L 630 90 L 600 110 L 584 110" stroke-width="1.5" />
                        <circle cx="650" cy="90" r="2" fill="#00d2ff" />
                        <circle cx="584" cy="110" r="2" fill="#00d2ff" />
                        <path d="M 650 110 L 620 110 L 600 130 L 595 130" stroke-width="1.5" />
                        <circle cx="650" cy="110" r="2" fill="#00d2ff" />
                        <circle cx="595" cy="130" r="2" fill="#00d2ff" />
                        <path d="M 665 145 L 640 145 L 620 160 L 607 160" stroke-width="1.5" />
                        <circle cx="665" cy="145" r="2" fill="#00d2ff" />
                        <circle cx="607" cy="160" r="2" fill="#00d2ff" />
                        <path d="M 680 170 L 650 170 L 630 185 L 615 185" stroke-width="1.5" />
                        <circle cx="680" cy="170" r="2" fill="#00d2ff" />
                        <circle cx="615" cy="185" r="2" fill="#00d2ff" />
                        <path d="M 680 190 L 640 190 L 625 200" stroke-width="1.5" />
                        <circle cx="680" cy="190" r="2" fill="#00d2ff" />
                        <circle cx="625" cy="200" r="2" fill="#00d2ff" />
                        <path d="M 680 210 L 650 210 L 630 200" stroke-width="1.5" />
                        <circle cx="680" cy="210" r="2" fill="#00d2ff" />
                        <circle cx="630" cy="200" r="2" fill="#00d2ff" />
                        <path d="M 680 230 L 660 230 L 640 215 L 615 215" stroke-width="1.5" />
                        <circle cx="680" cy="230" r="2" fill="#00d2ff" />
                        <circle cx="615" cy="215" r="2" fill="#00d2ff" />
                        <path d="M 665 255 L 640 255 L 620 240 L 607 240" stroke-width="1.5" />
                        <circle cx="665" cy="255" r="2" fill="#00d2ff" />
                        <circle cx="607" cy="240" r="2" fill="#00d2ff" />
                        <path d="M 650 290 L 620 290 L 600 270 L 595 270" stroke-width="1.5" />
                        <circle cx="650" cy="290" r="2" fill="#00d2ff" />
                        <circle cx="595" cy="270" r="2" fill="#00d2ff" />
                        <path d="M 650 310 L 630 310 L 600 290 L 584 290" stroke-width="1.5" />
                        <circle cx="650" cy="310" r="2" fill="#00d2ff" />
                        <circle cx="584" cy="290" r="2" fill="#00d2ff" />
                    </g>

                    <!-- CONTENEDORES PRINCIPALES -->
                    
                    <!-- Caja Izquierda (Recorte exacto) -->
                    <path 
                        d="M 80 50 L 330 50 A 20 20 0 0 1 350 70 L 350 130 L 320 160 L 320 240 L 350 270 L 350 330 A 20 20 0 0 1 330 350 L 80 350 A 20 20 0 0 1 60 330 L 60 70 A 20 20 0 0 1 80 50 Z"
                        fill="url(#boxGradLeft)" stroke="#00d2ff" stroke-width="2.5" filter="url(#glow)"
                    />

                    <!-- Caja Derecha (Recorte exacto) -->
                    <path 
                        d="M 920 50 L 670 50 A 20 20 0 0 0 650 70 L 650 130 L 680 160 L 680 240 L 650 270 L 650 330 A 20 20 0 0 0 670 350 L 920 350 A 20 20 0 0 0 940 330 L 940 70 A 20 20 0 0 0 920 50 Z"
                        fill="url(#boxGradRight)" stroke="#00d2ff" stroke-width="2.5" filter="url(#glow)"
                    />

                    <!-- Hexágono Central -->
                    <polygon 
                        points="440,70 560,70 620,200 560,330 440,330 380,200"
                        fill="url(#hexGrad)" stroke="#00d2ff" stroke-width="4" filter="url(#heavyGlow)"
                    />
                    <!-- Borde interior del hexágono para mayor profundidad -->
                    <polygon 
                        points="444,75 556,75 612,200 556,325 444,325 388,200"
                        fill="none" stroke="#00e5ff" stroke-width="1" opacity="0.5"
                    />

                    <!-- === CONTENIDO: TEXTOS E ÍCONOS === -->

                    <!-- -- SECCIÓN IZQUIERDA: OUR PROCESS -- -->
                    <text x="205" y="90" fill="white" font-size="18" font-weight="bold" text-anchor="middle" letter-spacing="0.5">OUR PROCESS</text>

                    <!-- Strategy & Design -->
                    <circle cx="110" cy="150" r="26" stroke="#00d2ff" stroke-width="2" fill="#040914" filter="url(#glow)"/>
                    <g transform="translate(97, 137)">
                        <!-- Ícono de Documento y Lupa -->
                        <path d="M 4,2 L 14,2 L 20,8 L 20,24 L 4,24 Z" stroke="white" stroke-width="1.5" fill="none" />
                        <path d="M 14,2 L 14,8 L 20,8" stroke="white" stroke-width="1.5" fill="none" />
                        <circle cx="11" cy="15" r="5" stroke="#00d2ff" stroke-width="2" fill="#040914" />
                        <line x1="14.5" y1="18.5" x2="19" y2="23" stroke="#00d2ff" stroke-width="2" stroke-linecap="round" />
                        <line x1="7" y1="10" x2="10" y2="10" stroke="white" stroke-width="1.5" />
                    </g>
                    <text x="155" y="155" fill="white" font-size="13" text-anchor="start">Strategy &amp; Design</text>

                    <!-- Implementation: Roadmap to ROI -->
                    <circle cx="120" cy="255" r="26" stroke="#00d2ff" stroke-width="2" fill="#040914" filter="url(#glow)"/>
                    <g transform="translate(107, 242)">
                        <!-- Ícono de Fábrica -->
                        <path d="M 2,22 L 2,10 L 8,15 L 8,10 L 14,15 L 14,10 L 22,16 L 22,22 Z" stroke="white" stroke-width="1.5" fill="none" />
                        <rect x="3" y="5" width="3" height="5" fill="white" />
                        <rect x="7" y="18" width="4" height="4" fill="white" />
                        <!-- Flecha arriba -->
                        <path d="M 17,14 L 17,4 L 13,8 M 17,4 L 21,8" stroke="#00d2ff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" />
                    </g>
                    <text x="120" y="305" fill="white" font-size="12" text-anchor="middle">Implementation:</text>
                    <text x="120" y="322" fill="white" font-size="12" text-anchor="middle">Roadmap to ROI</text>

                    <!-- Performance & Compliance -->
                    <circle cx="280" cy="255" r="26" stroke="#00d2ff" stroke-width="2" fill="#040914" filter="url(#glow)"/>
                    <g transform="translate(267, 242)">
                        <!-- Ícono de Gráfico de barras -->
                        <rect x="4" y="14" width="4" height="8" fill="white"/>
                        <rect x="10" y="9" width="4" height="13" fill="white"/>
                        <rect x="16" y="3" width="4" height="19" fill="white"/>
                        <!-- Flecha de tendencia -->
                        <path d="M 6,10 L 12,4 L 22,4 M 22,4 L 18,8 M 22,4 L 18,0" stroke="#00d2ff" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" />
                    </g>
                    <text x="280" y="305" fill="white" font-size="12" text-anchor="middle">Performance &amp;</text>
                    <text x="280" y="322" fill="white" font-size="12" text-anchor="middle">Compliance</text>

                    <!-- -- SECCIÓN DERECHA: WHAT WE DELIVER -- -->
                    <text x="795" y="90" fill="white" font-size="18" font-weight="bold" text-anchor="middle" letter-spacing="0.5">WHAT WE DELIVER</text>

                    <!-- Intelligent Agents -->
                    <circle cx="720" cy="150" r="26" stroke="#00d2ff" stroke-width="2" fill="#040914" filter="url(#glow)"/>
                    <g transform="translate(707, 137)">
                        <!-- Ícono Cerebro y Escudo -->
                        <path d="M 12,4 C 6,4 4,8 4,12 C 4,16 6,18 8,18 C 8,22 12,22 12,22 C 12,22 16,22 16,18 C 18,18 20,16 20,12 C 20,8 18,4 12,4 Z" stroke="white" stroke-width="1.5" fill="none" />
                        <path d="M 12,4 L 12,22" stroke="white" stroke-width="1" fill="none" />
                        <!-- Escudo Superpuesto -->
                        <path d="M 16,10 L 22,12 L 22,18 C 22,22 16,25 16,25 C 16,25 10,22 10,18 L 10,12 Z" fill="#040914" stroke="#00d2ff" stroke-width="1.5" />
                        <path d="M 16,12 L 16,25" stroke="#00d2ff" stroke-width="1" fill="none" />
                    </g>
                    <text x="760" y="155" fill="white" font-size="13" text-anchor="start">Intelligent Agents</text>

                    <!-- Top Right Node Icon (Network Hex) -->
                    <circle cx="890" cy="150" r="26" stroke="#00d2ff" stroke-width="2" fill="#040914" filter="url(#glow)"/>
                    <g transform="translate(877, 137)">
                        <polygon points="13,2 22,7 22,17 13,22 4,17 4,7" stroke="white" stroke-width="1.5" fill="none"/>
                        <line x1="13" y1="2" x2="13" y2="22" stroke="white" stroke-width="1"/>
                        <line x1="4" y1="7" x2="22" y2="17" stroke="white" stroke-width="1"/>
                        <line x1="4" y1="17" x2="22" y2="7" stroke="white" stroke-width="1"/>
                        <circle cx="13" cy="12" r="3" fill="#00d2ff" />
                    </g>
                    
                    <!-- Multi-Agent Systems text -->
                    <text x="815" y="215" fill="white" font-size="12" text-anchor="middle">Multi-Agent</text>
                    <text x="815" y="232" fill="white" font-size="12" text-anchor="middle">Systems (MAS)</text>

                    <!-- Measurable Efficiency -->
                    <circle cx="720" cy="255" r="26" stroke="#00d2ff" stroke-width="2" fill="#040914" filter="url(#glow)"/>
                    <g transform="translate(707, 242)">
                        <!-- Ícono Nodos Circulares -->
                        <circle cx="13" cy="13" r="5" stroke="#00d2ff" stroke-width="1.5" fill="none" />
                        <circle cx="13" cy="3" r="2" fill="white" />
                        <circle cx="13" cy="23" r="2" fill="white" />
                        <circle cx="3" cy="13" r="2" fill="white" />
                        <circle cx="23" cy="13" r="2" fill="white" />
                        <line x1="13" y1="5" x2="13" y2="8" stroke="white" stroke-width="1.5" />
                        <line x1="13" y1="18" x2="13" y2="21" stroke="white" stroke-width="1.5" />
                        <line x1="5" y1="13" x2="8" y2="13" stroke="white" stroke-width="1.5" />
                        <line x1="18" y1="13" x2="21" y2="13" stroke="white" stroke-width="1.5" />
                        <circle cx="7" cy="7" r="1.5" fill="#00d2ff" />
                        <circle cx="19" cy="19" r="1.5" fill="#00d2ff" />
                        <line x1="8" y1="8" x2="10" y2="10" stroke="#00d2ff" stroke-width="1" />
                        <line x1="16" y1="16" x2="18" y2="18" stroke="#00d2ff" stroke-width="1" />
                    </g>
                    <text x="720" y="305" fill="white" font-size="12" text-anchor="middle">Measurable</text>
                    <text x="720" y="322" fill="white" font-size="12" text-anchor="middle">Efficiency</text>

                    <!-- Measurable Growth -->
                    <circle cx="890" cy="255" r="26" stroke="#00d2ff" stroke-width="2" fill="#040914" filter="url(#glow)"/>
                    <g transform="translate(877, 242)">
                        <!-- Ícono Objetivo / Target -->
                        <circle cx="13" cy="13" r="10" stroke="white" stroke-width="1.5" fill="none" />
                        <circle cx="13" cy="13" r="6" stroke="white" stroke-width="1.5" fill="none" />
                        <circle cx="13" cy="13" r="2" fill="#00d2ff" />
                        <path d="M 13,3 L 13,1 C 18,1 23,4 25,9 L 23,9 C 21,5 17,3 13,3 Z" fill="#00d2ff" />
                        <line x1="18" y1="8" x2="24" y2="2" stroke="#00d2ff" stroke-width="2" stroke-linecap="round" />
                        <polygon points="18,8 22,7 19,4" fill="#00d2ff" />
                    </g>
                    <text x="890" y="305" fill="white" font-size="12" text-anchor="middle">Measurable</text>
                    <text x="890" y="322" fill="white" font-size="12" text-anchor="middle">Growth</text>

                    <!-- -- HEXÁGONO CENTRAL -- -->
                    
                    <!-- Engranaje e Ícono de Flecha en el Centro -->
                    <g transform="translate(470, 110)">
                        <!-- Rueda dentada (Engranaje) -->
                        <circle cx="25" cy="30" r="14" stroke="white" stroke-width="3" fill="none" />
                        <!-- Dientes del engranaje -->
                        <path d="M 25,12 L 25,48 M 7,30 L 43,30 M 12,17 L 38,43 M 12,43 L 38,17" stroke="white" stroke-width="4" />
                        <!-- Centro del engranaje vacío -->
                        <circle cx="25" cy="30" r="8" fill="#083863" stroke="white" stroke-width="2" />
                        
                        <!-- Flecha masiva envolvente hacia arriba -->
                        <path 
                            d="M 25,30 C 45,30 55,20 50,-10 L 58,-10 L 45,-30 L 32,-10 L 40,-10 C 45,10 38,20 25,20 Z" 
                            fill="url(#arrowGrad)" 
                            filter="url(#glow)"
                        />
                    </g>

                    <!-- Textos Centrales -->
                    <text x="500" y="240" fill="white" font-size="20" font-weight="bold" text-anchor="middle" letter-spacing="0.5">Navigate.</text>
                    <text x="500" y="270" fill="white" font-size="20" font-weight="bold" text-anchor="middle" letter-spacing="0.5">Optimize.</text>
                    <text x="500" y="300" fill="white" font-size="20" font-weight="bold" text-anchor="middle" letter-spacing="0.5">Scale.</text>
                </svg>
            </div>"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to replace the content of `<div class="consulting-diagram reveal">` segment 
# It spans from `<div class="consulting-diagram reveal">` down to `</div>` before the next reveal div.
start_tag = '<div class="consulting-diagram reveal">'
end_tag = '</div>\n\n            <div class="reveal" style="text-align: left; max-width: 900px; margin: 0 auto 1.5rem;">'
start_idx = content.find(start_tag)

if start_idx != -1:
    end_idx = content.find(end_tag, start_idx)
    if end_idx != -1:
        new_content = content[:start_idx] + html_svg + '\n' + content[end_idx:]
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Replaced successfully")
    else:
        print("End tag not found")
else:
    print("Start tag not found")
