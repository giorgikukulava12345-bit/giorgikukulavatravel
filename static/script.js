document.addEventListener("DOMContentLoaded", function () {
    // === 1. კატეგორიების ფილტრაცია ===
    const filterButtons = document.querySelectorAll(".filter-btn");
    const cards = document.querySelectorAll(".card");

    filterButtons.forEach(button => {
        button.addEventListener("click", function (e) {
            e.preventDefault();
            filterButtons.forEach(btn => btn.classList.remove("active"));
            this.classList.add("active");

            const targetCategory = this.getAttribute("data-target");

            cards.forEach(card => {
                const cardCategory = card.getAttribute("data-category");
                if (targetCategory === "all" || cardCategory === targetCategory) {
                    card.style.display = "flex";
                    setTimeout(() => {
                        card.style.opacity = "1";
                        card.style.transform = "scale(1)";
                    }, 50);
                } else {
                    card.style.opacity = "0";
                    card.style.transform = "scale(0.8)";
                    setTimeout(() => {
                        card.style.display = "none";
                    }, 300);
                }
            });
        });
    });

    // === 2. ვალუტის კალკულატორის ლოგიკა (ახალი) ===
    const currencySelect = document.getElementById("currency-select");
    const priceDisplays = document.querySelectorAll(".price-display");
    const ratesContainer = document.getElementById("exchange-rates");

    // ვკითხულობთ კურსებს, რომლებიც Python-მა მოგვაწოდა
    const rates = {
        GEL: parseFloat(ratesContainer.getAttribute("data-gel")),
        USD: parseFloat(ratesContainer.getAttribute("data-usd")),
        EUR: parseFloat(ratesContainer.getAttribute("data-eur")),
        CZK: 1.0
    };

    currencySelect.addEventListener("change", function () {
        const selectedCurrency = this.value;
        const rate = rates[selectedCurrency];

        priceDisplays.forEach(display => {
            const basePrice = parseFloat(display.getAttribute("data-base-price"));

            // თუ ფასი 0-ია, ვტოვებთ "უფასო"
            if (basePrice === 0) {
                display.textContent = "უფასო";
                return;
            }

            // წინააღმდეგ შემთხვევაში გადაგვყავს ახალ ვალუტაში და ვამრგვალებთ მეათედამდე
            const convertedPrice = (basePrice * rate).toFixed(1);
            
            let currencySymbol = selectedCurrency;
            if (selectedCurrency === "GEL") currencySymbol = "₾";
            else if (selectedCurrency === "USD") currencySymbol = "$";
            else if (selectedCurrency === "EUR") currencySymbol = "€";

            display.innerHTML = `<b>${convertedPrice} ${currencySymbol}</b>`;
        });
    });
});