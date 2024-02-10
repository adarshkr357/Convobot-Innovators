var time = gsap.timeline();

time.from(".robot", {
	x: -700,
	duration: 1.8,
	delay: 0.2,
	opacity: 0,
})
time.to(".robot", {
	x: -50,
	yoyo: true,
	duration: 0.5,
})
time.from(".cloud", {
	opacity: 0,
	scale: 0,
	duration: 1,
})
time.from(".nav-bar,.topic", {
	y: -100,
	duration: 0.5,
	stagger: 0.2,

})
time.from(".text-section", {
	y: 100,
})
time.from(".input-area,.send-btn ", {
	y: 100,
	duration: 0.8,
	stagger: 0.5

})
time.from(".mic", {
	scale: 0,
	opacity: 0,
	duration: 0.9

});

document.addEventListener('DOMContentLoaded', function () {
	var messageDiv = document.querySelector('.message');
	var sendButton = document.getElementById('sendButton');
	var micButton = document.getElementById('micButton');

	function toggleButtonVisibility() {
		var text = messageDiv.innerText.trim();
		sendButton.style.display = text.length > 0 ? 'inline' : 'none';
		micButton.style.display = text.length > 0 ? 'none' : 'inline';
	}

	messageDiv.addEventListener('input', toggleButtonVisibility);

	toggleButtonVisibility();
});


document.getElementById('micButton').addEventListener('click', function () {
	navigator.mediaDevices.getUserMedia({
			audio: true
		})
		.then(stream => {
			const recognition = new(window.SpeechRecognition || window.webkitSpeechRecognition)();
			recognition.lang = 'en-US';
			recognition.interimResults = true;

			let queryDiv = document.getElementById('query');

			recognition.onstart = function () {
				queryDiv.setAttribute("placeholder", "Listening...");
			};

			recognition.onresult = function (event) {
				const current = event.resultIndex;
				const transcript = event.results[current][0].transcript;
				queryDiv.textContent += transcript;
			};

			recognition.onspeechend = function () {
				recognition.stop();
				document.getElementById('sendButton').click();
			};

			recognition.onerror = function (event) {
				console.error('Recognition error', event.error);
				queryDiv.setAttribute("placeholder", "Error: " + event.error);
				recognition.stop();
			};

			recognition.start();
		})
		.catch(err => {
			console.error('Microphone access was denied', err);
		});
});

document.getElementById('sendButton').addEventListener('click', function () {
	let query = document.getElementById('query').innerHTML;

	fetch('/process-data', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				query
			})
		})
		.then(response => response.json())
		.then(data => {
			if (data.success) {
				document.getElementById('robot-section').style.display = 'none';
				document.getElementById('results-section').style.display = 'block';

				const tableBody = document.querySelector('#results-section table tbody');

				tableBody.innerHTML = '';

				data.data.forEach(result => {
					const row = document.createElement('tr');

					const siteNameCell = document.createElement('td');
					siteNameCell.textContent = result[0];
					row.appendChild(siteNameCell);

					const imageCell = document.createElement('td');
					const image = document.createElement('img');
					image.src = result[1];
					image.alt = 'Product Image';
					imageCell.appendChild(image);
					row.appendChild(imageCell);

					const titleCell = document.createElement('td');
					titleCell.textContent = result[2];
					row.appendChild(titleCell);

					const ratingCell = document.createElement('td');
					ratingCell.textContent = result[3];
					row.appendChild(ratingCell);

					const priceCell = document.createElement('td');
					priceCell.textContent = `INR ${result[4]}`;
					row.appendChild(priceCell);

					tableBody.appendChild(row);
				});
			} else {
				alert(data.error);
			};
		})
		.catch(error => {
			console.error('Error:', error);
		});
});
