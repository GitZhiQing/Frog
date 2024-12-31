document.addEventListener("DOMContentLoaded", () => {
  initHighlighting();
  initKaTeX();
  initTocbot();
  updateURLHash();
});

function initHighlighting() {
  document.querySelectorAll("pre code").forEach((block) => {
    hljs.highlightElement(block);
    addLanguageLabel(block);
  });
}

function addLanguageLabel(block) {
  const language = block.result
    ? block.result.language
    : block.className.split("-")[1];
  if (language) {
    const label = createLanguageLabel(language);
    block.parentNode.classList.add("code-block");
    block.parentNode.appendChild(label);
  }
}

function createLanguageLabel(language) {
  const label = document.createElement("div");
  label.className = "language-label";
  label.textContent = language;

  label.addEventListener("mouseover", () => {
    label.dataset.originalText = label.textContent;
    label.textContent = "复制";
  });

  label.addEventListener("mouseout", () => {
    label.textContent = label.dataset.originalText;
  });

  label.addEventListener("click", () => {
    copyToClipboard(label, language);
  });

  return label;
}

function copyToClipboard(label, language) {
  const code = label.previousSibling.innerText;
  navigator.clipboard.writeText(code).then(() => {
    label.textContent = "已复制";
    setTimeout(() => {
      label.textContent = language;
    }, 2000);
  });
}

function initKaTeX() {
  renderMathInElement(document.body, {
    delimiters: [
      { left: "$$", right: "$$", display: true },
      { left: "\\(", right: "\\)", display: false },
    ],
  });
}

function initTocbot() {
  tocbot.init({
    tocSelector: "#toc-content",
    contentSelector: ".article-content",
    headingSelector: "h1, h2, h3",
    scrollSmooth: true,
    headingsOffset: 180,
    collapseDepth: 3,
    fixedSidebar: true,
    orderedList: false,
    scrollEndCallback: (e) => {
      const id = e.target.id;
      if (id) {
        history.replaceState(null, null, "#" + id);
      }
    },
  });
}

function updateURLHash() {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          history.replaceState(null, null, "#" + entry.target.id);
        }
      });
    },
    { rootMargin: "-80px 0px -80% 0px" }
  );

  document
    .querySelectorAll(
      ".article-content h1, .article-content h2, .article-content h3"
    )
    .forEach((heading) => {
      observer.observe(heading);
    });
}
