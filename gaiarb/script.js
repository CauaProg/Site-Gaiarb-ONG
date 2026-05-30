/* ═══════════════════════════════════════════════
   GAIARB – script.js
   ═══════════════════════════════════════════════ */

// ── VARIÁVEIS GLOBAIS ────────────────────────────
let valorSelecionado = 50;
let currentPixPayload = "";
let qrInstance = null;
const apiBase = window.location.protocol === 'file:' ? 'http://127.0.0.1:8000' : '';

/* ═══════════════════════════════════════════════
   INICIALIZAÇÃO
   ═══════════════════════════════════════════════ */
document.addEventListener("DOMContentLoaded", () => {

    // Animações de entrada ao scroll
    iniciarScrollAnimations();

    // Highlight link ativo no header
    marcarLinkAtivo();

    // Contador animado nos stats (home)
    iniciarContadores();

    // Partículas flutuantes no hero (home)
    criarParticulasHero();

    // Efeito parallax leve no banner
    iniciarParallax();

    // Fade-in nas seções
    iniciarFadeInSections();

    // Carregamento dinâmico do Banco de Dados
    carregarEquipeDinamica();

    // Inicialização da página de doações
    inicializarPaginaDoacao();

    // Injetar estética global de pintura e desenho
    injectGlobalAesthetics();
});


/* ═══════════════════════════════════════════════
   ANIMAÇÕES DE SCROLL
   ═══════════════════════════════════════════════ */
function iniciarScrollAnimations() {
    const seletores = [
        ".membro-linha",
        ".card-ajuda",
        ".mvv-card",
        ".porque-item",
        ".impacto-item",
        ".forma-card",
        ".galeria-item",
        ".stat-item",
        ".valor-tag",
        ".areas-lista li",
        ".quem-foto",
        ".secao"
    ];

    const elementos = document.querySelectorAll(seletores.join(", "));

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add("visivel-scroll");
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: "0px 0px -40px 0px" });

    elementos.forEach((el, i) => {
        el.style.opacity = "0";
        el.style.transform = "translateY(30px)";
        el.style.transition = `opacity 0.55s ease ${i * 0.04}s, transform 0.55s ease ${i * 0.04}s`;
        observer.observe(el);
    });
}

// Classe adicionada pelo observer
document.addEventListener("DOMContentLoaded", () => {
    const style = document.createElement("style");
    style.textContent = ".visivel-scroll { opacity: 1 !important; transform: translateY(0) !important; }";
    document.head.appendChild(style);
});


/* ═══════════════════════════════════════════════
   LINK ATIVO NO HEADER
   ═══════════════════════════════════════════════ */
function marcarLinkAtivo() {
    const pagina = window.location.pathname.split("/").pop() || "index.html";
    document.querySelectorAll(".alllinks a").forEach(link => {
        const href = link.getAttribute("href");
        const div  = link.querySelector(".linkshead");
        if (!div || div.classList.contains("btn-doe")) return;
        if (href === pagina || (pagina === "" && href === "index.html")) {
            div.classList.add("active-link");
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const style = document.createElement("style");
    style.textContent = `
        .linkshead.active-link::after { width: 80% !important; }
        .linkshead.active-link { color: var(--primary) !important; }
    `;
    document.head.appendChild(style);
});


/* ═══════════════════════════════════════════════
   CONTADORES ANIMADOS (HOME)
   ═══════════════════════════════════════════════ */
function iniciarContadores() {
    const statsBar = document.querySelector(".stats-bar");
    if (!statsBar) return;
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.querySelectorAll(".stat-numero").forEach(el => {
                    const raw = el.textContent.trim();
                    const valor = parseInt(raw.replace(/\D/g, ""));
                    const sufixo = raw.includes("+") ? "+" : "";
                    if (!isNaN(valor)) animarContador(el, valor, sufixo);
                });
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.4 });

    observer.observe(statsBar);
}

function animarContador(el, alvo, sufixo) {
    let atual = 0;
    const duracao = 1200;
    const incremento = Math.ceil(alvo / (duracao / 16));
    const timer = setInterval(() => {
        atual = Math.min(atual + incremento, alvo);
        el.textContent = atual.toLocaleString("pt-BR") + sufixo;
        if (atual >= alvo) clearInterval(timer);
    }, 16);
}


/* ═══════════════════════════════════════════════
   PARTÍCULAS HERO (HOME)
   ═══════════════════════════════════════════════ */
function criarParticulasHero() {
    const hero = document.querySelector(".hero");
    if (!hero) return;

    const emojis = ["💜", "🌈", "💛", "💚", "💙", "🌟", "✨", "💕"];
    for (let i = 0; i < 8; i++) {
        const p = document.createElement("span");
        p.textContent = emojis[i % emojis.length];
        p.style.cssText = `
            position: absolute;
            font-size: ${12 + Math.random() * 16}px;
            top: ${Math.random() * 100}%;
            left: ${Math.random() * 100}%;
            opacity: ${0.05 + Math.random() * 0.08};
            pointer-events: none;
            animation: floatParticle ${5 + Math.random() * 6}s ease-in-out infinite;
            animation-delay: ${Math.random() * 4}s;
            z-index: 0;
        `;
        hero.appendChild(p);
    }

    const style = document.createElement("style");
    style.textContent = `
        @keyframes floatParticle {
            0%, 100% { transform: translateY(0) rotate(0deg); }
            33%       { transform: translateY(-20px) rotate(10deg); }
            66%       { transform: translateY(10px) rotate(-5deg); }
        }
    `;
    document.head.appendChild(style);
}


/* ═══════════════════════════════════════════════
   PARALLAX LEVE NO BANNER
   ═══════════════════════════════════════════════ */
function iniciarParallax() {
    const banner = document.querySelector(".banner");
    if (!banner) return;
    window.addEventListener("scroll", () => {
        const scrollY = window.scrollY;
        banner.style.backgroundPositionY = `calc(50% + ${scrollY * 0.3}px)`;
    }, { passive: true });
}


/* ═══════════════════════════════════════════════
   FADE-IN DAS SEÇÕES GRANDES
   ═══════════════════════════════════════════════ */
function iniciarFadeInSections() {
    const secoes = document.querySelectorAll(".secao, .quem-somos, .como-ajudar, .mvv-section, .valores-section");
    const obs = new IntersectionObserver((entries) => {
        entries.forEach(e => {
            if (e.isIntersecting) {
                e.target.style.opacity = "1";
                e.target.style.transform = "none";
                obs.unobserve(e.target);
            }
        });
    }, { threshold: 0.08 });

    secoes.forEach(s => {
        s.style.opacity    = "0";
        s.style.transform  = "translateY(20px)";
        s.style.transition = "opacity 0.7s ease, transform 0.7s ease";
        obs.observe(s);
    });
}


/* ═══════════════════════════════════════════════
   DOAÇÃO – SISTEMA SIMPLIFICADO PIX
   ═══════════════════════════════════════════════ */
let activeDoeTab = 'pix';

function switchDoeTab(tab) {
    // compatibility placeholder
}

function inicializarPaginaDoacao() {
    const qrEl = document.getElementById("staticPixQrCode");
    if (!qrEl) return;
    
    // Generate static payload with no amount to let the donor choose
    const pixPayload = generatePixPayload("67c3117b-28f1-4ac2-94a6-c4bc3121807f", 0, "GAIARB", "RIO DE JANEIRO");
    currentPixPayload = pixPayload;
    
    const qrUrl = "https://api.qrserver.com/v1/create-qr-code/?size=188x188&data=" + encodeURIComponent(pixPayload);
    qrEl.innerHTML = `<img src="${qrUrl}" alt="QR Code PIX" style="width:188px;height:188px;display:block;margin:0 auto;box-shadow:0 4px 12px rgba(0,0,0,0.05);">`;
    
    const ccText = document.getElementById("pixCopiaColaText");
    if (ccText) ccText.textContent = pixPayload;
}

function gerarDoacaoMercadoPago() {
    const valorInput = document.getElementById("doeValorInput");
    if (!valorInput) return;
    
    const val = parseFloat(valorInput.value);
    if (!val || val <= 0) {
        valorInput.style.borderColor = "#e53e3e";
        setTimeout(() => { valorInput.style.borderColor = ""; }, 1500);
        alert("Por favor, insira um valor válido.");
        return;
    }
    
    const btn = document.getElementById("btnGerarPix");
    const originalText = btn ? btn.textContent : "Gerar QR Code PIX";
    if (btn) {
        btn.disabled = true;
        btn.textContent = "Gerando...";
    }
    
    const successMsg = document.getElementById("doe-success-msg");
    if (successMsg) {
        successMsg.style.display = "none";
    }
    
    fetch(apiBase + '/api/doacoes/mercadopago', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ valor: val })
    })
    .then(res => {
        if (!res.ok) throw new Error("Erro na requisição ao servidor");
        return res.json();
    })
    .then(data => {
        if (data.success) {
            // Update current payload
            currentPixPayload = data.qr_code;
            
            // Update Copia e Cola text
            const ccText = document.getElementById("pixCopiaColaText");
            if (ccText) {
                ccText.textContent = data.qr_code;
            }
            
            // Update QR Code image
            const qrEl = document.getElementById("staticPixQrCode");
            if (qrEl) {
                if (data.qr_code_base64) {
                    qrEl.innerHTML = `<img src="data:image/png;base64,${data.qr_code_base64}" alt="QR Code PIX" style="width:188px;height:188px;display:block;margin:0 auto;box-shadow:0 4px 12px rgba(0,0,0,0.05);">`;
                } else {
                    const qrUrl = "https://api.qrserver.com/v1/create-qr-code/?size=188x188&data=" + encodeURIComponent(data.qr_code);
                    qrEl.innerHTML = `<img src="${qrUrl}" alt="QR Code PIX" style="width:188px;height:188px;display:block;margin:0 auto;box-shadow:0 4px 12px rgba(0,0,0,0.05);">`;
                }
            }
            
            // Update status badge
            const badge = document.getElementById("mp-status-badge");
            if (badge) {
                badge.textContent = data.provider === "mercadopago" ? "Mercado Pago Ativo" : "Mercado Pago (Simulado)";
                badge.style.display = "inline-block";
            }
            
            if (successMsg) {
                successMsg.textContent = `QR Code PIX no valor de R$ ${val.toFixed(2)} gerado com sucesso!`;
                successMsg.style.display = "block";
            }
        } else {
            alert("Erro ao gerar doação: " + (data.error || "Tente novamente mais tarde."));
        }
    })
    .catch(err => {
        console.warn("Backend offline or request failed, generating local simulation.", err);
        // Fallback to local simulation
        const simulatedPayload = generatePixPayload("67c3117b-28f1-4ac2-94a6-c4bc3121807f", val, "GAIARB", "RIO DE JANEIRO");
        currentPixPayload = simulatedPayload;
        
        const ccText = document.getElementById("pixCopiaColaText");
        if (ccText) {
            ccText.textContent = simulatedPayload;
        }
        
        const qrEl = document.getElementById("staticPixQrCode");
        if (qrEl) {
            const qrUrl = "https://api.qrserver.com/v1/create-qr-code/?size=188x188&data=" + encodeURIComponent(simulatedPayload);
            qrEl.innerHTML = `<img src="${qrUrl}" alt="QR Code PIX" style="width:188px;height:188px;display:block;margin:0 auto;box-shadow:0 4px 12px rgba(0,0,0,0.05);">`;
        }
        
        const badge = document.getElementById("mp-status-badge");
        if (badge) {
            badge.textContent = "Mercado Pago (Simulado Offline)";
            badge.style.display = "inline-block";
        }
        
        if (successMsg) {
            successMsg.textContent = `Doação de R$ ${val.toFixed(2)} simulada offline com sucesso!`;
            successMsg.style.display = "block";
        }
    })
    .finally(() => {
        if (btn) {
            btn.disabled = false;
            btn.textContent = originalText;
        }
    });
}

function registrarDoacaoNoBanco() {
    const valorInput = document.getElementById("doeValorInput");
    if (!valorInput) return;
    
    const val = parseFloat(valorInput.value);
    if (!val || val <= 0) {
        valorInput.style.borderColor = "#e53e3e";
        setTimeout(() => { valorInput.style.borderColor = ""; }, 1500);
        alert("Por favor, insira um valor válido.");
        return;
    }
    
    const successMsg = document.getElementById("doe-success-msg");
    if (successMsg) {
        successMsg.style.display = "none";
    }
    
    fetch(apiBase + '/api/doacoes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ valor: val, tipo: 'PIX', status: 'Confirmado' })
    })
    .then(res => res.json())
    .then(data => {
        if (successMsg) {
            successMsg.textContent = `Doação de R$ ${val.toFixed(2)} registrada com sucesso! Muito obrigado pelo seu apoio.`;
            successMsg.style.display = "block";
        } else {
            alert(`Doação de R$ ${val.toFixed(2)} registrada com sucesso!`);
        }
        valorInput.value = "50";
        const nameInput = document.getElementById("doeNomeInput");
        if (nameInput) nameInput.value = "";
    })
    .catch(err => {
        console.warn("Backend offline, simulating local log.");
        if (successMsg) {
            successMsg.textContent = `Doação de R$ ${val.toFixed(2)} registrada com sucesso (Modo offline). Obrigado!`;
            successMsg.style.display = "block";
        } else {
            alert(`Doação de R$ ${val.toFixed(2)} registrada com sucesso (Modo offline).`);
        }
        valorInput.value = "50";
        const nameInput = document.getElementById("doeNomeInput");
        if (nameInput) nameInput.value = "";
    });
}

function copiarChave(chave) {
    navigator.clipboard.writeText(chave).then(() => {
        alert("Chave copiada: " + chave);
    }).catch(() => {
        alert("Chave PIX: " + chave);
    });
}

function copiarChaveCopiaCola() {
    if (currentPixPayload) {
        navigator.clipboard.writeText(currentPixPayload).then(() => {
            alert("Código PIX Copia e Cola copiado com sucesso!");
        }).catch(() => {
            alert("Falha ao copiar código PIX.");
        });
    }
}

function calculateCRC16(str) {
    let crc = 0xFFFF;
    for (let c = 0; c < str.length; c++) {
        crc ^= str.charCodeAt(c) << 8;
        for (let i = 0; i < 8; i++) {
            if (crc & 0x8000) {
                crc = (crc << 1) ^ 0x1021;
            } else {
                crc = crc << 1;
            }
            crc &= 0xFFFF;
        }
    }
    let hex = crc.toString(16).toUpperCase();
    while (hex.length < 4) {
        hex = "0" + hex;
    }
    return hex;
}

function generatePixPayload(key, amount, name, city) {
    let payload = "000201";
    
    let gui = "0014br.gov.bcb.pix";
    
    let keyLenStr = String(key.length);
    if (keyLenStr.length < 2) keyLenStr = "0" + keyLenStr;
    let keyTag = "01" + keyLenStr + key;
    
    let merchantInfo = gui + keyTag;
    let merchantInfoLenStr = String(merchantInfo.length);
    if (merchantInfoLenStr.length < 2) merchantInfoLenStr = "0" + merchantInfoLenStr;
    payload += "26" + merchantInfoLenStr + merchantInfo;
    
    payload += "52040000";
    payload += "5303986";
    
    if (amount && Number(amount) > 0) {
        let numAmount = Number(amount);
        let amtStr = numAmount.toFixed(2);
        let amtLenStr = String(amtStr.length);
        if (amtLenStr.length < 2) amtLenStr = "0" + amtLenStr;
        payload += "54" + amtLenStr + amtStr;
    }
    
    payload += "5802BR";
    
    let sanitizedName = name.toUpperCase();
    let nameLenStr = String(sanitizedName.length);
    if (nameLenStr.length < 2) nameLenStr = "0" + nameLenStr;
    payload += "59" + nameLenStr + sanitizedName;
    
    let sanitizedCity = city.toUpperCase();
    let cityLenStr = String(sanitizedCity.length);
    if (cityLenStr.length < 2) cityLenStr = "0" + cityLenStr;
    payload += "60" + cityLenStr + sanitizedCity;
    
    let txid = "62100506GAIARB";
    payload += txid;
    
    payload += "6304";
    let crc = calculateCRC16(payload);
    payload += crc;
    
    return payload;
}


/* ═══════════════════════════════════════════════
   GALERIA – FILTROS
   ═══════════════════════════════════════════════ */
function filtrar(btn, categoria) {
    document.querySelectorAll(".filtro-btn").forEach(b => b.classList.remove("ativo"));
    btn.classList.add("ativo");

    const itens = document.querySelectorAll(".galeria-item");
    const grid = document.querySelector(".galeria-grid");

    let visiveis = 0;

    itens.forEach((item, i) => {
        const cat = item.dataset.cat;

        if (categoria === "todos" || cat === categoria) {
            item.style.display = "";
            visiveis++;

            // animação suave
            item.style.opacity = "0";
            item.style.transform = "scale(0.88)";

            setTimeout(() => {
                item.style.transition = "opacity 0.35s ease, transform 0.35s ease";
                item.style.opacity = "1";
                item.style.transform = "scale(1)";
            }, i * 45);

        } else {
            item.style.display = "none";
        }
    });

    // 🔥 AQUI ESTÁ O SEGREDO (crescer quando filtrar)
    if (visiveis <= 4) {
        grid.classList.add("expandido");
    } else {
        grid.classList.remove("expandido");
    }
}


/* ═══════════════════════════════════════════════
   GALERIA – LIGHTBOX
   ═══════════════════════════════════════════════ */
function abrirLightbox(item) {
    const lb       = document.getElementById("lightbox");
    const conteudo = document.getElementById("lightboxConteudo");
    if (!lb || !conteudo) return;
    conteudo.style.backgroundImage = item.style.backgroundImage;
    lb.classList.add("aberto");
    document.body.style.overflow = "hidden";
}

function fecharLightbox(event) {
    const lb = document.getElementById("lightbox");
    if (!lb) return;
    if (!event || event.target === lb || event.target.classList.contains("lightbox-fechar")) {
        lb.classList.remove("aberto");
        document.body.style.overflow = "";
    }
}


/* ═══════════════════════════════════════════════
   FORMULÁRIO DE VOLUNTÁRIO
   ═══════════════════════════════════════════════ */
function enviarFormVoluntario() {
    const nome  = document.getElementById("vol-nome")?.value.trim();
    const email = document.getElementById("vol-email")?.value.trim();
    const whats = document.getElementById("vol-whats")?.value.trim();
    const area  = document.getElementById("vol-area")?.value;
    const disp  = document.getElementById("vol-disp")?.value;
    const msg   = document.getElementById("vol-msg")?.value.trim();

    if (!nome || !email || !whats || !area) {
        // Destaca campos vazios
        ["vol-nome","vol-email","vol-whats","vol-area"].forEach(id => {
            const el = document.getElementById(id);
            if (el && !el.value.trim()) {
                el.style.borderColor = "#e53e3e";
                el.style.boxShadow = "0 0 0 4px rgba(229,62,62,0.15)";
                setTimeout(() => {
                    el.style.borderColor = "";
                    el.style.boxShadow = "";
                }, 2000);
            }
        });
        return;
    }

    const payload = { nome, email, whatsapp: whats, area, disponibilidade: disp, mensagem: msg };
    const btn = document.querySelector(".vol-form-col .btn-primary");
    const originalText = btn ? btn.textContent : "Enviar Candidatura";
    if (btn) {
        btn.disabled = true;
        btn.textContent = "Enviando...";
    }

    const statusMsg = document.getElementById("vol-status-msg");
    if (statusMsg) {
        statusMsg.style.display = "none";
        statusMsg.textContent = "";
    }

    fetch(apiBase + '/api/voluntarios', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(data => {
        if (statusMsg) {
            statusMsg.style.color = "var(--secondary)";
            statusMsg.textContent = `Obrigado, ${nome}! Recebemos sua candidatura com sucesso.`;
            statusMsg.style.display = "block";
        } else {
            alert(`Obrigado, ${nome}! Recebemos sua candidatura com sucesso.`);
        }
        ["vol-nome","vol-email","vol-whats","vol-area","vol-disp","vol-msg"].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.value = "";
        });
    })
    .catch(err => {
        console.warn("Backend offline, saving application client-side simulation.");
        if (statusMsg) {
            statusMsg.style.color = "var(--secondary)";
            statusMsg.textContent = `Obrigado, ${nome}! Cadastro recebido (Modo offline).`;
            statusMsg.style.display = "block";
        } else {
            alert(`Obrigado, ${nome}! Cadastro recebido (Modo offline).`);
        }
        ["vol-nome","vol-email","vol-whats","vol-area","vol-disp","vol-msg"].forEach(id => {
            const el = document.getElementById(id);
            if (el) el.value = "";
        });
    })
    .finally(() => {
        if (btn) {
            btn.disabled = false;
            btn.textContent = originalText;
        }
    });
}

/* ═══════════════════════════════════════════════
   INTEGRAÇÃO DINÂMICA DO BANCO DE DADOS (APIs)
   ═══════════════════════════════════════════════ */

function carregarEquipeDinamica() {
    const lista = document.querySelector('.equipe-lista');
    if (!lista) return;
    
    fetch(apiBase + '/api/equipe')
    .then(res => {
        if (!res.ok) throw new Error("API Indisponível");
        return res.json();
    })
    .then(data => {
        if (!data || data.length === 0) return;
        lista.innerHTML = ''; // Limpa conteúdo estático se carregou do banco
        data.forEach((m, i) => {
            lista.innerHTML += `
                <div class="membro-linha">
                    <div class="membro-numero">${m.numero}</div>
                    <div class="membro-info">
                        <div class="membro-nome">${m.nome}</div>
                        <span class="membro-cargo-tag">${m.cargo}</span>
                        <p class="membro-bio">${m.bio}</p>
                    </div>
                    <div class="membro-deco dc${(i % 6) + 1}"></div>
                </div>
            `;
        });
    })
    .catch(err => {
        console.log("Servidor offline: Usando dados estáticos para equipe", err);
    });
}

// FAQ Accordion Toggle
document.addEventListener("DOMContentLoaded", () => {
    const faqQuestions = document.querySelectorAll(".faq-question");
    faqQuestions.forEach(btn => {
        btn.addEventListener("click", () => {
            const item = btn.parentNode;
            const answer = item.querySelector(".faq-answer");
            const isActive = item.classList.contains("active");
            
            // Close all other faq items first
            document.querySelectorAll(".faq-item").forEach(otherItem => {
                otherItem.classList.remove("active");
                otherItem.querySelector(".faq-answer").style.maxHeight = null;
            });
            
            if (!isActive) {
                item.classList.add("active");
                answer.style.maxHeight = answer.scrollHeight + "px";
            }
        });
    });
});

/* Auxiliar para gerar o SVG do Girassol Geométrico detalhado */
function getSunflowerSVG() {
    const numPetals = 14;
    const angleStep = 360 / numPetals;
    let sfSvg = `
        <svg viewBox="0 0 120 120" fill="none" stroke="currentColor">
            <!-- Grid de Sementes no Miolo (Centro) -->
            <g stroke-width="0.8" opacity="0.8">
                <circle cx="60" cy="60" r="18" fill="currentColor" fill-opacity="0.15" stroke-width="1.8"/>
                <circle cx="60" cy="60" r="14" stroke-dasharray="2,2"/>
                <circle cx="60" cy="60" r="10" stroke-dasharray="1.5,1.5"/>
                <circle cx="60" cy="60" r="6" stroke-dasharray="1,1"/>
                <circle cx="60" cy="60" r="2.5" fill="currentColor"/>
                <path d="M52,52 L68,68 M68,52 L52,68 M60,42 L60,78 M42,60 L78,60" stroke-width="0.5" stroke-dasharray="1,2" opacity="0.5"/>
            </g>
            <g>
    `;
    // 1. Pétalas de Trás
    for (let i = 0; i < numPetals; i++) {
        const rotAngle = i * angleStep + (angleStep / 2);
        sfSvg += `
            <g transform="rotate(${rotAngle} 60 60)" opacity="0.65">
                <path d="M 60,42 C 53,34 53,22 60,12 Z" fill="currentColor" fill-opacity="0.5" stroke="currentColor" stroke-width="0.8"/>
                <path d="M 60,42 C 67,34 67,22 60,12 Z" fill="currentColor" fill-opacity="0.35" stroke="currentColor" stroke-width="0.8"/>
            </g>
        `;
    }
    // 2. Pétalas da Frente
    for (let i = 0; i < numPetals; i++) {
        const rotAngle = i * angleStep;
        sfSvg += `
            <g transform="rotate(${rotAngle} 60 60)">
                <path d="M 60,42 C 52,32 52,20 60,10 Z" fill="currentColor" fill-opacity="0.85" stroke="currentColor" stroke-width="1"/>
                <path d="M 60,42 C 68,32 68,20 60,10 Z" fill="currentColor" fill-opacity="0.6" stroke="currentColor" stroke-width="1"/>
            </g>
        `;
    }
    sfSvg += `
            </g>
        </svg>
    `;
    return sfSvg;
}

/* ═══════════════════════════════════════════════
   ESTÉTICA GLOBAL: INJEÇÃO DE ARTE, TINTA E DESENHO
   ═══════════════════════════════════════════════ */
function injectGlobalAesthetics() {
    // 1. SVGs dos respingos de tinta
    const splattersSvg = [
        `<svg viewBox="0 0 100 100"><path d="M30,30 C50,10 80,20 80,45 C80,70 60,85 40,85 C20,85 10,60 10,45 C10,30 10,50 30,30 Z" fill="currentColor"/><circle cx="85" cy="30" r="3.5" fill="currentColor"/><circle cx="15" cy="75" r="2.5" fill="currentColor"/><circle cx="50" cy="5" r="2" fill="currentColor"/></svg>`,
        `<svg viewBox="0 0 100 100"><path d="M40,25 C65,15 85,40 75,70 C65,100 35,90 25,75 C15,60 15,35 40,25 Z" fill="currentColor"/><circle cx="80" cy="85" r="2.5" fill="currentColor"/><circle cx="20" cy="15" r="3.5" fill="currentColor"/><circle cx="55" cy="8" r="2" fill="currentColor"/></svg>`,
        `<svg viewBox="0 0 100 100"><path d="M35,20 C60,10 80,30 80,55 C80,80 50,90 35,75 C20,60 10,30 35,20 Z" fill="currentColor"/><circle cx="85" cy="65" r="2.5" fill="currentColor"/><circle cx="15" cy="20" r="2" fill="currentColor"/><circle cx="70" cy="85" r="1.5" fill="currentColor"/></svg>`
    ];

    // 2. Injetar respingos estruturados nos fundos das seções
    const sections = document.querySelectorAll(".secao, .hero-section, .about-brief-section, .how-to-help-section, .testimonials-section, .faq-section, .about-section, .team-section, .voluntario-editorial-section, .login-wrapper, .video-section");
    sections.forEach((sec, idx) => {
        // Garantir que a seção tenha position relative para posicionar os splatters
        const secStyle = window.getComputedStyle(sec);
        if (secStyle.position === 'static') {
            sec.style.position = 'relative';
        }

        // Criar splatter 1 (esquerda)
        const s1 = document.createElement("div");
        const shapeIdx1 = idx % 3;
        s1.className = `paint-splatter-bg splatter-${shapeIdx1 + 1}`;
        s1.innerHTML = splattersSvg[shapeIdx1];
        
        // Cores alternadas da paleta
        const colors = ["var(--primary)", "var(--secondary)", "var(--accent)"];
        s1.style.color = colors[idx % colors.length];
        
        // Posicionamento alternado
        s1.style.left = `${5 + (idx * 7) % 15}%`;
        s1.style.top = `${10 + (idx * 13) % 40}%`;
        s1.style.transform = `rotate(${(idx * 45) % 360}deg) scale(${0.8 + (idx * 0.1) % 0.5})`;
        sec.appendChild(s1);

        // Criar splatter 2 (direita) em seções maiores
        if (sec.offsetHeight > 300) {
            const s2 = document.createElement("div");
            const shapeIdx2 = (idx + 1) % 3;
            s2.className = `paint-splatter-bg splatter-${shapeIdx2 + 1}`;
            s2.innerHTML = splattersSvg[shapeIdx2];
            s2.style.color = colors[(idx + 1) % colors.length];
            s2.style.right = `${5 + (idx * 9) % 15}%`;
            s2.style.bottom = `${10 + (idx * 17) % 35}%`;
            s2.style.transform = `rotate(${(idx * 75) % 360}deg) scale(${0.7 + (idx * 0.15) % 0.4})`;
            sec.appendChild(s2);
        }

        // Injetar DOIS girassóis decorativos de fundo por seção (diagonais opostas)
        const sunflower1 = document.createElement("div");
        const sfColor1 = idx % 2 === 0 ? 'sunflower-gray' : 'sunflower-green';
        const sfSize1 = idx % 3 === 0 ? 'sunflower-size-1' : 'sunflower-size-2';
        sunflower1.className = `sunflower-bg ${sfColor1} ${sfSize1}`;
        sunflower1.innerHTML = getSunflowerSVG();
        
        const sunflower2 = document.createElement("div");
        const sfColor2 = idx % 2 === 0 ? 'sunflower-green' : 'sunflower-gray';
        const sfSize2 = idx % 3 === 0 ? 'sunflower-size-2' : 'sunflower-size-1';
        sunflower2.className = `sunflower-bg ${sfColor2} ${sfSize2}`;
        sunflower2.innerHTML = getSunflowerSVG();

        // Posicionar alternando entre diagonais opostas
        if (idx % 2 === 0) {
            sunflower1.style.right = `${8 + (idx * 7) % 18}%`;
            sunflower1.style.top = `${8 + (idx * 13) % 25}%`;
            
            sunflower2.style.left = `${10 + (idx * 9) % 18}%`;
            sunflower2.style.bottom = `${12 + (idx * 11) % 25}%`;
        } else {
            sunflower1.style.left = `${8 + (idx * 8) % 18}%`;
            sunflower1.style.top = `${12 + (idx * 12) % 25}%`;
            
            sunflower2.style.right = `${10 + (idx * 11) % 18}%`;
            sunflower2.style.bottom = `${8 + (idx * 14) % 25}%`;
        }
        
        sunflower1.style.transform = `rotate(${(idx * 40 + 15) % 360}deg)`;
        sunflower2.style.transform = `rotate(${(idx * 40 + 195) % 360}deg)`;
        
        sec.appendChild(sunflower1);
        sec.appendChild(sunflower2);
    });

    // 3. Efeito de Quadro (Molduras) e Rotação Randômica Realista
    const frames = document.querySelectorAll('.secao-img, .grid-img-large, .grid-img-small, .about-img, .about-image-wrapper .about-img, .about-img');
    frames.forEach((el, index) => {
        // Rotação entre -1.2deg e +1.2deg para simular quadros reais pendurados
        const angle = (Math.random() * 2.4 - 1.2).toFixed(2);
        el.style.transform = `rotate(${angle}deg)`;
        
        el.addEventListener('mouseenter', () => {
            el.style.transform = 'scale(1.015) rotate(0deg)';
        });
        el.addEventListener('mouseleave', () => {
            el.style.transform = `rotate(${angle}deg)`;
        });
    });

    // 4. Inserir desenhos (sketches) decorativos à mão livre
    
    // Setas apontando para ações importantes
    const buttonsToArrow = document.querySelectorAll(".hero-actions .btn-primary, .vol-form-col .btn-primary, .newsletter-form .btn-primary, .btn-doe");
    buttonsToArrow.forEach((btn, idx) => {
        // Evita duplicar setas no header
        if (btn.classList.contains("btn-doe") && idx > 0) return;
        
        const parent = btn.parentNode;
        const parentStyle = window.getComputedStyle(parent);
        if (parentStyle.position === 'static') {
            parent.style.position = 'relative';
        }

        const arrow = document.createElement("div");
        arrow.className = "sketch-element sketch-arrow";
        // SVG seta rabiscada
        arrow.innerHTML = `
            <svg viewBox="0 0 50 30">
                <path d="M5,20 Q20,5 42,10 M42,10 L32,3 M42,10 L34,19" stroke="currentColor" fill="none" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        `;
        arrow.style.color = "var(--secondary)";
        
        // Posicionar ligeiramente acima e à esquerda do botão
        arrow.style.position = "absolute";
        arrow.style.top = "-24px";
        arrow.style.left = "-38px";
        arrow.style.transform = "rotate(-10deg)";
        
        parent.appendChild(arrow);
    });

    // Estrelas brilhantes ao lado de cabeçalhos ou destaques
    const titles = document.querySelectorAll(".section-title, .help-title, .vol-title, .member-name, .form-title");
    titles.forEach((title, idx) => {
        const titleStyle = window.getComputedStyle(title);
        if (titleStyle.position === 'static') {
            title.style.position = 'relative';
        }

        const star = document.createElement("div");
        star.className = "sketch-element sketch-star";
        // SVG estrela rabiscada
        star.innerHTML = `
            <svg viewBox="0 0 24 24">
                <path d="M12,2 L14.5,9 L22,9 L16,13.5 L18.5,21 L12,16.5 L5.5,21 L8,13.5 L2,9 L9.5,9 Z" stroke="currentColor" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        `;
        star.style.color = "var(--accent)";
        star.style.top = "-12px";
        star.style.right = "-20px";
        
        title.appendChild(star);
    });

    // Espirais rabiscadas nos cantos dos cards maiores
    const largeCards = document.querySelectorAll(".team-card, .vol-form-col, .login-card, .registro-doacao-box");
    largeCards.forEach((card, idx) => {
        const cardStyle = window.getComputedStyle(card);
        if (cardStyle.position === 'static') {
            card.style.position = 'relative';
        }

        const swirl = document.createElement("div");
        swirl.className = "sketch-element sketch-swirl";
        // SVG espiral
        swirl.innerHTML = `
            <svg viewBox="0 0 40 40">
                <path d="M20,20 C25,15 25,25 20,25 C15,25 15,15 20,10 C27,10 27,27 20,30 C10,30 8,12 20,5 C35,0 38,32 20,37" stroke="currentColor" fill="none" stroke-width="2" stroke-linecap="round"/>
            </svg>
        `;
        swirl.style.color = "var(--primary)";
        swirl.style.bottom = "8px";
        swirl.style.right = "8px";
        
        card.appendChild(swirl);
    });
}
