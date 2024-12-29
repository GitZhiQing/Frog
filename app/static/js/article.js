document.addEventListener("DOMContentLoaded", (event) => {
  // 初始化代码高亮
  document.querySelectorAll("pre code").forEach((block) => {
    hljs.highlightElement(block);
    // 添加语言标签和复制功能
    const language = block.result
      ? block.result.language
      : block.className.split("-")[1];
    if (language) {
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
        const code = block.innerText;
        navigator.clipboard.writeText(code).then(() => {
          label.textContent = "已复制";
          setTimeout(() => {
            label.textContent = language;
          }, 2000);
        });
      });
      block.parentNode.classList.add("code-block");
      block.parentNode.appendChild(label);
    }
  });
  // 初始化 KaTeX
  renderMathInElement(document.body, {
    delimiters: [
      { left: "$$", right: "$$", display: true },
      { left: "$", right: "$", display: false },
    ],
  });
});

// 更新 URL hash
function updateURLHash() {
  const headings = document.querySelectorAll(
    ".article-content h1, .article-content h2, .article-content h3, .article-content h4, .article-content h5, .article-content h6"
  );
  let lastVisibleHeading = null;

  for (const heading of headings) {
    const rect = heading.getBoundingClientRect();
    if (rect.top >= 0 && rect.top <= window.innerHeight / 2) {
      lastVisibleHeading = heading;
    }
  }

  if (lastVisibleHeading && lastVisibleHeading.id) {
    history.replaceState(null, null, `#${lastVisibleHeading.id}`);
  }
}

document.addEventListener("scroll", updateURLHash);
document.addEventListener("DOMContentLoaded", updateURLHash);
