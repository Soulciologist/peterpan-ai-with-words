function ai() {
    const button = document.getElementById("submit");

    if (
        document.getElementById("last-eat").value === "" ||
        document.getElementById("eat").value === "" ||
        document.getElementById("plans").value === ""
    ) {
        alert("Please fill in all the fields.");
        return;
    }

    button.disabled = true;

    let last_eat = document.getElementById("last-eat").value;
    let eat = document.getElementById("eat").value;
    let plans = document.getElementById("plans").value;
    fetch("/ai", {
        method: "POST",
        body: JSON.stringify({
            last_eat: last_eat,
            eat: eat,
            plans: plans,
        }),
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((response) => {
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let result = "";
            let elem = document.getElementById("output");

            document
                .getElementById("output-wrapper-1")
                .removeAttribute("hidden");

            // Process the stream
            return new Promise((resolve) => {
                function read() {
                    reader.read().then(({ done, value }) => {
                        if (done) {
                            // Resolve the promise when done
                            let characters = [
                                "\n",
                                "\n",
                                "\\- ",
                                "P",
                                "e",
                                "t",
                                "e",
                                "r",
                                " ",
                                "P",
                                "a",
                                "n",
                            ];
                            function addCharWithDelay(index) {
                                if (index < characters.length) {
                                    setTimeout(() => {
                                        result += characters[index];
                                        elem.innerHTML = marked.parse(result);
                                        addCharWithDelay(index + 1);
                                    }, 100); // 100 milliseconds = 0.1 seconds
                                } else {
                                    resolve(result);
                                }
                            }
                            addCharWithDelay(0);
                            return;
                        }
                        // Decode the chunk and add to result
                        const chunk = decoder.decode(value, {
                            stream: true,
                        });
                        result += chunk;
                        // Update the DOM with the new chunk
                        elem.innerHTML = marked.parse(result);
                        // Read the next chunk
                        read();
                    });
                }
                read(); // Start reading the stream
            });
        })
        .then((finalResult) => {
            console.log("Streaming completed:", finalResult);
            setTimeout(() => {
                button.disabled = false;
            }, 1000);
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}

function ai2() {
    const button = document.getElementById("submit-2");

    if (
        document.getElementById("last-eat").value === "" ||
        document.getElementById("eat").value === "" ||
        document.getElementById("plans").value === ""
    ) {
        alert("Please fill in all the fields.");
        return;
    }

    button.disabled = true;

    let photo = document.getElementById("fridge").files[0];
    let restrictions = document.getElementById("diet").value;
    let last_eat = document.getElementById("last-eat-2").value;
    let eat = document.getElementById("eat-2").value;
    let plans = document.getElementById("plans-2").value;

    // Create a new FormData object
    const formData = new FormData();

    // Append the image file (make sure to get the first file from the input)
    formData.append("image", photo, photo.name);

    // Append your data to the FormData object
    formData.append("restrictions", restrictions);
    formData.append("last_eat", last_eat);
    formData.append("eat", eat);
    formData.append("plans", plans);

    fetch("/ai2", {
        method: "POST",
        body: formData,
    })
        .then((response) => {
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let result = "";
            let elem = document.getElementById("output-2");

            document
                .getElementById("output-wrapper-2")
                .removeAttribute("hidden");

            // Process the stream
            return new Promise((resolve) => {
                function read() {
                    reader.read().then(({ done, value }) => {
                        if (done) {
                            // Resolve the promise when done
                            let characters = [
                                "\n",
                                "\n",
                                "\\- ",
                                "P",
                                "e",
                                "t",
                                "e",
                                "r",
                                " ",
                                "P",
                                "a",
                                "n",
                            ];
                            function addCharWithDelay(index) {
                                if (index < characters.length) {
                                    setTimeout(() => {
                                        result += characters[index];
                                        elem.innerHTML = marked.parse(result);
                                        addCharWithDelay(index + 1);
                                    }, 100); // 100 milliseconds = 0.1 seconds
                                } else {
                                    resolve(result);
                                }
                            }
                            addCharWithDelay(0);
                            return;
                        }
                        // Decode the chunk and add to result
                        const chunk = decoder.decode(value, {
                            stream: true,
                        });
                        result += chunk;
                        // Update the DOM with the new chunk
                        elem.innerHTML = marked.parse(result);
                        // Read the next chunk
                        read();
                    });
                }
                read(); // Start reading the stream
            });
        })
        .then((finalResult) => {
            console.log("Streaming completed:", finalResult);
            setTimeout(() => {
                button.disabled = false;
            }, 1000);
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}

document.getElementById("submit").addEventListener("click", ai);
document.getElementById("submit-2").addEventListener("click", ai2);

document.getElementById("last-eat").addEventListener("change", function () {
    document.getElementById("last-eat-2").value = this.value;
});
document.getElementById("eat").addEventListener("change", function () {
    document.getElementById("eat-2").value = this.value;
});
document.getElementById("plans").addEventListener("change", function () {
    document.getElementById("plans-2").value = this.value;
});
