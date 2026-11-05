const chatLauncher = document.getElementById("chatLauncher");
const chatPanel = document.getElementById("chatPanel");
const closeChat = document.getElementById("closeChat");

chatLauncher.addEventListener("click", () => chatPanel.classList.add("open"));
closeChat.addEventListener("click", () => chatPanel.classList.remove("open"));

document.querySelectorAll(".filter-tab").forEach((tab) => {
    tab.addEventListener("click", () => {
        document.querySelectorAll(".filter-tab").forEach((item) => item.classList.remove("active"));
        tab.classList.add("active");
        const filter = tab.dataset.filter;
        document.querySelectorAll(".product-card").forEach((card) => {
            card.classList.toggle("is-hidden", filter !== "all" && card.dataset.category !== filter);
        });
    });
});

document.querySelectorAll(".save-button").forEach((button) => {
    button.addEventListener("click", () => {
        button.classList.toggle("saved");
        button.textContent = button.classList.contains("saved") ? "♥" : "♡";
    });
});

document.querySelectorAll(".chat-suggestions button").forEach((suggestion) => {
    suggestion.addEventListener("click", () => {
        const input = document.querySelector(".chat-input input");
        input.value = suggestion.textContent;
        input.focus();
    });
});

document.querySelector(".chat-input").addEventListener("submit", (event) => {
    event.preventDefault();
    const input = event.currentTarget.querySelector("input");
    if (!input.value.trim()) return;
    const message = document.createElement("div");
    message.className = "ai-message";
    message.style.marginTop = "9px";
    message.textContent = "Thanks — a Mavuno advisor will use this request to find the best match for you.";
    document.querySelector(".chat-body").appendChild(message);
    input.value = "";
});

document.querySelector(".menu-toggle").addEventListener("click", () => {
    const nav = document.querySelector(".main-nav");
    nav.style.display = nav.style.display === "flex" ? "none" : "flex";
    nav.style.position = "absolute";
    nav.style.top = "68px";
    nav.style.left = "0";
    nav.style.right = "0";
    nav.style.padding = "15px 6%";
    nav.style.background = "#f6f5ee";
    nav.style.zIndex = "5";
    nav.style.flexDirection = "column";
});
