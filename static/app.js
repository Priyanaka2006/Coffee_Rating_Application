const grid = document.querySelector("#coffee-grid");
const statusMessage = document.querySelector("#status-message");

function renderCoffees(coffees) {
  grid.innerHTML = coffees
    .map(
      (coffee, index) => `
    <article class="coffee-card" style="animation-delay: ${index * 70}ms">
      <div class="coffee-photo">
        <img src="${coffee.image}" alt="${coffee.alt}" loading="lazy">
        <span class="roast-label">${coffee.roast}</span>
      </div>
      <div class="coffee-details">
        <p class="coffee-origin">${coffee.origin}</p>
        <h3>${coffee.name}</h3>
        <p class="coffee-notes">${coffee.notes}</p>
        <div class="coffee-actions">
          <button class="vote-button" type="button" data-coffee-id="${coffee.id}">I'd brew this</button>
          <span class="vote-count"><strong>${coffee.votes}</strong> ${coffee.votes === 1 ? "vote" : "votes"}</span>
        </div>
      </div>
    </article>
  `,
    )
    .join("");
  grid.setAttribute("aria-busy", "false");
}

async function loadCoffees() {
  try {
    const response = await fetch("/api/coffees");
    if (!response.ok) throw new Error("Could not load coffees");
    renderCoffees(await response.json());
  } catch (_error) {
    grid.innerHTML =
      '<p class="loading-message">Could not load the tasting list. Refresh to try again.</p>';
    grid.setAttribute("aria-busy", "false");
  }
}

grid.addEventListener("click", async (event) => {
  const button = event.target.closest(".vote-button");
  if (!button) return;

  button.disabled = true;
  statusMessage.textContent = "Saving your vote...";
  try {
    const response = await fetch(
      `/api/coffees/${button.dataset.coffeeId}/vote`,
      { method: "POST" },
    );
    if (!response.ok) throw new Error("Vote could not be saved");
    const updatedCoffee = await response.json();
    const count = button.nextElementSibling.querySelector("strong");
    count.textContent = updatedCoffee.votes;
    button.nextElementSibling.lastChild.textContent =
      updatedCoffee.votes === 1 ? " vote" : " votes";
    statusMessage.textContent = "Your vote is in. Nice choice!";
  } catch (_error) {
    statusMessage.textContent = "That vote did not save. Please try again.";
  } finally {
    button.disabled = false;
  }
});

loadCoffees();
