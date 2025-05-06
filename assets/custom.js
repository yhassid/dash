console.log("Running custom.js with MutationObserver");

const observer = new MutationObserver(function(mutations, obs) {
    const links = document.querySelectorAll('.popup-link');
    if (links.length > 0) {
        console.log("Found", links.length, "popup-link elements");

        links.forEach(function(link) {
            if (!link.dataset.popupBound) {
                console.log("Attaching handler to:", link);
                link.dataset.popupBound = true; // mark as bound

                link.addEventListener('click', function(event) {
                    event.preventDefault();
                    const url = link.getAttribute('data-url');
                    console.log("Link clicked, data-url:", url);

                    if (url) {
                        const popup = window.open(url, '_blank', 'width=800,height=600');
                        if (popup) {
                            console.log("Popup window opened successfully");
                        } else {
                            console.warn("Popup window was blocked by the browser");
                            alert("Popup was blocked! Please allow popups for this site.");
                        }
                    } else {
                        console.warn("No data-url found on clicked link");
                    }
                });
            }
        });

        // Once we find and bind, stop observing
        obs.disconnect();
    }
});

observer.observe(document.body, { childList: true, subtree: true });
