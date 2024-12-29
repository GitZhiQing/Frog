const dirTree = JSON.parse(dirTreeJson.replace(/&#34;/g, '"'));
function renderTree(tree, parentElement) {
  const ul = document.createElement("ul");
  ul.classList.add("category-list");
  for (const key in tree) {
    const li = document.createElement("li");
    li.classList.add("category-item");
    if (key.endsWith(".md")) {
      const title = key.replace(/\.md$/, "");
      const a = document.createElement("a");
      a.href = `./articles/${title}`;
      a.textContent = title;
      a.classList.add("article-title");
      li.appendChild(a);
      li.classList.add("article-title-item");
    } else {
      const div = document.createElement("div");
      div.textContent = key;
      div.classList.add("category-title");
      li.appendChild(div);
      if (tree[key] !== null) {
        renderTree(tree[key], li);
      }
    }
    ul.appendChild(li);
  }
  parentElement.appendChild(ul);
}
const articlesDiv = document.getElementById("articles");
renderTree(dirTree, articlesDiv);
