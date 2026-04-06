const challenges = [
	{
		id: "marioo",
		title: "Marioo",
		category: "Reverse",
		folder: "reverse/Marioo",
		problemStatement: "Complete custom World 8-4 with memory analysis and Cheat Engine-assisted reverse techniques.",
		writeupSummary: "Unknown-value scans, state-variable tracking, and selective instruction patching bypassed death flow while preserving valid completion logic.",
		writeupMd: "reverse/Marioo/Mario_Hack.md",
		scripts: [],
		images: [
			"reverse/Marioo/Screenshot%202026-04-06%20184822.png",
			"reverse/Marioo/Screenshot%202026-04-06%20184900.png",
			"reverse/Marioo/Winningmoment.jpeg"
		]
	},
	{
		id: "bald-boy",
		title: "Bald Boy",
		category: "Forensics",
		folder: "forensics/Bald Boy",
		problemStatement: "Find a missing Amazon-style order ID from network traffic in a PCAP file.",
		writeupSummary: "Timeline-based packet analysis beats decoys. The correct clue appears in HTTP traffic and confirms the final formatted ID.",
		writeupMd: "forensics/Bald%20Boy/Forensics_Bald_Boy.md",
		scripts: [],
		images: [
			"forensics/Bald%20Boy/image.png",
			"forensics/Bald%20Boy/Screenshot%202026-04-06%20182816.png",
			"forensics/Bald%20Boy/Screenshot%202026-04-06%20182843.png"
		]
	},
	{
		id: "audible",
		title: "Audible",
		category: "Misc",
		folder: "misc/Audible",
		problemStatement: "Audio challenge where the hidden flag is not obvious in raw playback.",
		writeupSummary: "Spectrogram visualization in Sonic Visualiser reveals embedded text. Standard LSB and hex-level attempts were dead ends.",
		writeupMd: "misc/Audible/Misc_Audible.md",
		scripts: [],
		images: ["misc/Audible/Audible_Sonic_visualiser.jpeg"]
	},
	{
		id: "don",
		title: "Don",
		category: "Misc",
		folder: "misc/Don",
		problemStatement: "Investigate a Minecraft world where Don hid the flag in the underworld.",
		writeupSummary: "World forensics + controlled level.dat edits avoided lethal spawn loops. Clues near emerald blocks led to the chest flag path.",
		writeupMd: "misc/Don/Don_minecraft.md",
		scripts: [],
		images: [
			"misc/Don/Screenshot%202026-04-05%20234336.png",
			"misc/Don/Screenshot%202026-04-06%20184102.png",
			"misc/Don/Screenshot%202026-04-06%20184120.png"
		]
	},
	{
		id: "error-correction",
		title: "Error Correction / IdentiTy Parts of QR",
		category: "Misc",
		folder: "misc/Error Correction",
		problemStatement: "Reconstruct a deliberately corrupted QR by understanding finder patterns and QR layout constraints.",
		writeupSummary: "Brute swaps failed; the solve required structural QR knowledge and constraint-respecting reconstruction to get a scannable final QR.",
		writeupMd: "misc/Error%20Correction/Misc_Error_Correction.md",
		scripts: [
			"misc/Error%20Correction/chall.py",
			"misc/Error%20Correction/solve.py"
		],
		images: [
			"misc/Error%20Correction/chall.png",
			"misc/Error%20Correction/Final_QR.png"
		]
	},
	{
		id: "rizzler",
		title: "Are You The Rizzler?",
		category: "Social",
		folder: "social/Are You The Rizzler",
		problemStatement: "Chat with Lexi and extract the hidden secret despite conversational defenses.",
		writeupSummary: "Prompt reframing worked where direct asks failed. Creative context-switching induced secret leakage in generated narrative output.",
		writeupMd: "social/Are%20You%20The%20Rizzler/Are_You_The_Rizzler.md",
		scripts: [],
		images: []
	},
	{
		id: "what-the-book",
		title: "What The Book",
		category: "Web",
		folder: "web/What The Book",
		problemStatement: "Download the protected flag book from a vulnerable bookstore app by exploiting checkout logic.",
		writeupSummary: "Mixed number/string price types enabled type-confusion in cart sums. A crafted API request bypassed budget checks and returned flag content.",
		writeupMd: "web/What%20The%20Book/Web_What_The_Book.md",
		scripts: ["web/What%20The%20Book/exploit.py"],
		images: []
	},
	{
		id: "polyprimes",
		title: "PolyPrimes",
		category: "Crypto",
		folder: "crypto/PolyPrimes",
		problemStatement: "Custom polynomial-based prime generation with base tricks; recover factors and decrypt ciphertext.",
		writeupSummary: "The modulus leaks structure in the chosen base. Reconstructing polynomial terms allows factoring p, q, r and standard RSA decryption.",
		writeupMd: "crypto/PolyPrimes/Crypto_PolyPrimes.md",
		scripts: [
			"crypto/PolyPrimes/polyprimes.py",
			"crypto/PolyPrimes/script.py"
		],
		images: []
	}
];

const cardsGrid = document.getElementById("cards-grid");
const filterButtons = document.getElementById("filter-buttons");
const template = document.getElementById("challenge-card-template");
const modal = document.getElementById("details-modal");
const modalContent = document.getElementById("modal-content");
const closeModalBtn = document.getElementById("close-modal");

const state = {
	filter: "All"
};

const categories = ["All", ...new Set(challenges.map((item) => item.category))];

function fileName(path) {
	return path.split("/").pop() || path;
}

function normalize(text) {
	return text.toLowerCase().replace(/\s+/g, " ").trim();
}

function updateStats() {
	const pdfCount = challenges.length;
	const scriptCount = challenges.reduce((acc, c) => acc + c.scripts.length, 0);

	document.getElementById("challenge-count").textContent = String(challenges.length);
	document.getElementById("pdf-count").textContent = String(pdfCount);
	document.getElementById("script-count").textContent = String(scriptCount);
}

function renderFilters() {
	filterButtons.innerHTML = "";
	categories.forEach((cat) => {
		const btn = document.createElement("button");
		btn.type = "button";
		btn.textContent = cat;
		btn.classList.toggle("active", state.filter === cat);
		btn.addEventListener("click", () => {
			state.filter = cat;
			renderFilters();
			renderCards();
		});
		filterButtons.appendChild(btn);
	});
}

function filteredChallenges() {
	return challenges.filter((item) => {
		const passesFilter = state.filter === "All" || item.category === state.filter;
		return passesFilter;
	});
}

function renderCards() {
	cardsGrid.innerHTML = "";
	const visible = filteredChallenges();

	if (visible.length === 0) {
		const empty = document.createElement("div");
		empty.className = "empty-state";
		empty.textContent = "No challenges matched your search/filter. Try broader keywords.";
		cardsGrid.appendChild(empty);
		return;
	}

	visible.forEach((challenge) => {
		const clone = template.content.cloneNode(true);
		const card = clone.querySelector(".card");
		const category = clone.querySelector(".category");
		const title = clone.querySelector("h2");
		const summary = clone.querySelector(".summary");
		const detailsBtn = clone.querySelector('[data-action="details"]');

		category.textContent = challenge.category;
		title.textContent = challenge.title;
		summary.textContent = `Writeup: ${challenge.writeupSummary}`;

		detailsBtn.addEventListener("click", () => openModal(challenge));
		cardsGrid.appendChild(card);
	});
}

function imageBlock(paths) {
	const safePaths = paths.filter(Boolean);
	if (!safePaths.length) {
		return `<p class="summary">No supporting images provided for this challenge.</p>`;
	}

	const figures = safePaths
		.map((path) => {
			return `
				<figure>
					<img loading="lazy" src="${path}" alt="Challenge image">
				</figure>
			`;
		})
		.join("");

	return `
		<div class="image-grid">${figures}</div>
	`;
}

function escapeHtml(text) {
	return text
		.replace(/&/g, "&amp;")
		.replace(/</g, "&lt;")
		.replace(/>/g, "&gt;");
}

function inlineMarkdown(text) {
	let value = escapeHtml(text);
	const codeSpans = [];

	value = value.replace(/`([^`]+)`/g, (_, code) => {
		const token = `__CODE_SPAN_${codeSpans.length}__`;
		codeSpans.push(`<code>${code}</code>`);
		return token;
	});

	value = value.replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_m, label, url) => {
		const safeUrl = url.replace(/"/g, "%22");
		return `<a href="${safeUrl}" target="_blank" rel="noopener noreferrer">${label}</a>`;
	});

	value = value.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
	value = value.replace(/\*([^*]+)\*/g, "<em>$1</em>");
	value = value.replace(/(https?:\/\/[^\s<]+)/g, '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>');

	return value.replace(/__CODE_SPAN_(\d+)__/g, (_m, index) => codeSpans[Number(index)] || "");
}

function markdownToHtml(markdown) {
	const lines = markdown.replace(/\r\n/g, "\n").split("\n");
	const html = [];
	let inUl = false;
	let inOl = false;
	let inCode = false;
	let codeLines = [];
	let paragraphLines = [];

	const flushParagraph = () => {
		if (!paragraphLines.length) {
			return;
		}
		html.push(`<p>${inlineMarkdown(paragraphLines.join(" "))}</p>`);
		paragraphLines = [];
	};

	const closeLists = () => {
		flushParagraph();
		if (inUl) {
			html.push("</ul>");
			inUl = false;
		}
		if (inOl) {
			html.push("</ol>");
			inOl = false;
		}
	};

	for (let i = 0; i < lines.length; i += 1) {
		const raw = lines[i];
		const line = raw.trimEnd();
		const trimmed = line.trim();

		if (trimmed.startsWith("```")) {
			if (inCode) {
				html.push(`<pre><code>${escapeHtml(codeLines.join("\n"))}</code></pre>`);
				inCode = false;
				codeLines = [];
			} else {
				closeLists();
				inCode = true;
			}
			continue;
		}

		if (inCode) {
			codeLines.push(raw);
			continue;
		}

		if (!trimmed) {
			closeLists();
			continue;
		}

		if (/^(?:-{3,}|\*{3,}|_{3,})$/.test(trimmed)) {
			closeLists();
			html.push("<hr>");
			continue;
		}

		if (trimmed.startsWith("# ")) {
			closeLists();
			html.push(`<h1>${inlineMarkdown(trimmed.slice(2).trim())}</h1>`);
			continue;
		}
		if (trimmed.startsWith("## ")) {
			closeLists();
			html.push(`<h2>${inlineMarkdown(trimmed.slice(3).trim())}</h2>`);
			continue;
		}
		if (trimmed.startsWith("### ")) {
			closeLists();
			html.push(`<h3>${inlineMarkdown(trimmed.slice(4).trim())}</h3>`);
			continue;
		}

		if (trimmed.startsWith(">")) {
			closeLists();
			html.push(`<blockquote>${inlineMarkdown(trimmed.replace(/^>\s?/, ""))}</blockquote>`);
			continue;
		}

		if (/^\|.+\|$/.test(trimmed) && i + 1 < lines.length) {
			const alignmentLine = lines[i + 1].trim();
			if (/^\|?\s*:?[-]+:?(\s*\|\s*:?[-]+:?)+\s*\|?$/.test(alignmentLine)) {
				closeLists();
				const headerCells = trimmed.split("|").slice(1, -1).map((v) => v.trim());
				html.push("<table><thead><tr>");
				headerCells.forEach((cell) => html.push(`<th>${inlineMarkdown(cell)}</th>`));
				html.push("</tr></thead><tbody>");

				i += 2;
				while (i < lines.length) {
					const rowLine = lines[i].trim();
					if (!/^\|.+\|$/.test(rowLine)) {
						i -= 1;
						break;
					}
					const cells = rowLine.split("|").slice(1, -1).map((v) => v.trim());
					html.push("<tr>");
					cells.forEach((cell) => html.push(`<td>${inlineMarkdown(cell)}</td>`));
					html.push("</tr>");
					i += 1;
				}
				html.push("</tbody></table>");
				continue;
			}
		}

		if (/^\d+\.\s+/.test(trimmed)) {
			if (!inOl) {
				closeLists();
				html.push("<ol>");
				inOl = true;
			}
			html.push(`<li>${inlineMarkdown(trimmed.replace(/^\d+\.\s+/, ""))}</li>`);
			continue;
		}

		if (/^[-*]\s+/.test(trimmed)) {
			if (!inUl) {
				closeLists();
				html.push("<ul>");
				inUl = true;
			}
			html.push(`<li>${inlineMarkdown(trimmed.replace(/^[-*]\s+/, ""))}</li>`);
			continue;
		}

		if (inUl || inOl) {
			closeLists();
		}
		paragraphLines.push(trimmed);
	}

	flushParagraph();
	if (inCode) {
		html.push(`<pre><code>${escapeHtml(codeLines.join("\n"))}</code></pre>`);
	}
	if (inUl) {
		html.push("</ul>");
	}
	if (inOl) {
		html.push("</ol>");
	}

	return html.join("\n");
}

async function fetchText(path) {
	const response = await fetch(path);
	if (!response.ok) {
		throw new Error(`Failed to load ${path}`);
	}
	return response.text();
}

async function scriptsBlock(paths) {
	if (!paths.length) {
		return "";
	}

	const parts = [];
	for (const path of paths) {
		try {
			const code = await fetchText(path);
			parts.push(`
				<div class="script-file">
					<h5>${fileName(path)}</h5>
					<pre><code>${escapeHtml(code)}</code></pre>
				</div>
			`);
		} catch {
			parts.push(`
				<div class="script-file">
					<h5>${fileName(path)}</h5>
					<p class="summary">Unable to load this script.</p>
				</div>
			`);
		}
	}

	return `
		<section class="scripts-section">
			<h4>Python Scripts</h4>
			${parts.join("\n")}
		</section>
	`;
}

async function openModal(challenge) {
	const scriptsPlaceholder = challenge.scripts.length
		? `
		<section class="scripts-section">
			<h4>Python Scripts</h4>
			<p class="summary">Loading script content...</p>
		</section>
	`
		: "";

	modalContent.innerHTML = `
		<section class="modal-text">
			<span class="chip">${challenge.category}</span>
			<h3>${challenge.title}</h3>
			<p><strong>Folder:</strong> ${challenge.folder}</p>
			<p><strong>Writeup Summary:</strong> ${challenge.writeupSummary}</p>
		</section>
		<section class="writeup-section">
			<h4>Solution Writeup</h4>
			<div class="writeup-content"><p class="summary">Loading writeup content...</p></div>
		</section>
		<section class="asset-block">
			<h4>Context Images</h4>
			${imageBlock(challenge.images)}
		</section>
		${scriptsPlaceholder}
	`;

	if (!modal.open) {
		modal.showModal();
	}

	try {
		const mdText = await fetchText(challenge.writeupMd);
		const html = markdownToHtml(mdText);
		const writeupContainer = modalContent.querySelector(".writeup-content");
		if (writeupContainer) {
			writeupContainer.innerHTML = html;
		}
	} catch {
		const writeupContainer = modalContent.querySelector(".writeup-content");
		if (writeupContainer) {
			writeupContainer.innerHTML = "<p class=\"summary\">Unable to load solution markdown content.</p>";
		}
	}

	if (challenge.scripts.length) {
		const scriptsHtml = await scriptsBlock(challenge.scripts);
		const scriptSection = modalContent.querySelector(".scripts-section");
		if (scriptSection && scriptsHtml) {
			scriptSection.outerHTML = scriptsHtml;
		}
	}
}

closeModalBtn.addEventListener("click", () => {
	modal.close();
});

modal.addEventListener("click", (event) => {
	const rect = modal.getBoundingClientRect();
	const clickedInside =
		rect.top <= event.clientY &&
		event.clientY <= rect.top + rect.height &&
		rect.left <= event.clientX &&
		event.clientX <= rect.left + rect.width;

	if (!clickedInside) {
		modal.close();
	}
});

updateStats();
renderFilters();
renderCards();
