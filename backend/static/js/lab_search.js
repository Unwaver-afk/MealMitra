// Asynchronous AJAX search demonstration for College Syllabus Module 6
document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("ajax-plan-search");
    const resultsContainer = document.getElementById("ajax-search-results");
    const countBadge = document.getElementById("search-results-count");

    if (!searchInput || !resultsContainer) return;

    let debounceTimer;

    searchInput.addEventListener("input", function (e) {
        clearTimeout(debounceTimer);
        const query = e.target.value.trim();

        debounceTimer = setTimeout(() => {
            fetch(`/api/plans/search?q=${encodeURIComponent(query)}`)
                .then((res) => res.json())
                .then((data) => {
                    if (countBadge) countBadge.textContent = `${data.count} found`;

                    if (data.results.length === 0) {
                        resultsContainer.innerHTML = `
                            <tr>
                                <td colspan="5" style="text-align:center; padding: 24px; color: #64748b;">
                                    No meal plans matched your search "${query}".
                                </td>
                            </tr>
                        `;
                        return;
                    }

                    resultsContainer.innerHTML = data.results
                        .map(
                            (p) => `
                        <tr>
                            <td><strong>${p.title}</strong></td>
                            <td><span class="badge badge-info">${p.mealType}</span></td>
                            <td>${p.duration}</td>
                            <td>₹${p.price}</td>
                            <td>${p.description}</td>
                        </tr>
                    `
                        )
                        .join("");
                })
                .catch((err) => {
                    console.error("AJAX Search Error:", err);
                });
        }, 250);
    });
});
