// Comment on selected text: opens a pre-filled GitHub issue form (no server needed).
(function () {
  const REPO = "NAPCORE/its-data-dictionary";
  const btn = document.createElement("button");
  btn.textContent = "Comment on selection";
  btn.style.cssText = "position:absolute;display:none;z-index:1000;padding:4px 8px;" +
    "border:1px solid #888;border-radius:4px;background:#fff;cursor:pointer;font-size:13px";
  document.body.appendChild(btn);
  let quote = "";
  document.addEventListener("mouseup", (e) => {
    if (e.target === btn) return;
    const sel = window.getSelection();
    quote = sel ? sel.toString().trim() : "";
    if (!quote) { btn.style.display = "none"; return; }
    const r = sel.getRangeAt(0).getBoundingClientRect();
    btn.style.left = window.scrollX + r.left + "px";
    btn.style.top = window.scrollY + r.bottom + 6 + "px";
    btn.style.display = "block";
  });
  btn.addEventListener("click", () => {
    const h1 = document.querySelector("h1");
    const term = h1 ? h1.textContent.trim() : document.title;
    const url = new URL(`https://github.com/${REPO}/issues/new`);
    url.searchParams.set("template", "review.yml");
    url.searchParams.set("title", `[Review] ${term}`);
    url.searchParams.set("term", term);
    url.searchParams.set("page", window.location.href);
    url.searchParams.set("quote", quote.slice(0, 1500));
    window.open(url.toString(), "_blank");
    btn.style.display = "none";
  });
})();
