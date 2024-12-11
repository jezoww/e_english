function updateModalContent(testTitle, questions) {
    const modalTestTitle = document.getElementById('modalTestTitle');
    const modalQuestionsList = document.getElementById('modalQuestionsList');

    // Modal sarlavhasini yangilash
    modalTestTitle.textContent = testTitle;

    // Savollar ro'yxatini yangilash
    modalQuestionsList.innerHTML = ''; // Avvalgi ma'lumotlarni tozalash
    questions.forEach(test => {
        const li = document.createElement('li');
        li.innerHTML = `
            <p><strong>${test.question}</strong></p>
            <ul>
                <li>A: ${test.a}</li>
                <li>B: ${test.b}</li>
                <li>C: ${test.c}</li>
                <li>D: ${test.d}</li>
            </ul>
        `;
        modalQuestionsList.appendChild(li);
    });
}

function openModal() {
    const modal = document.getElementById('testModal');
    modal.style.display = 'block'; // Modalni ko'rsatish
}

function closeModal() {
    const modal = document.getElementById('testModal');
    modal.style.display = 'none'; // Modalni yopish
}

document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll('.open-modal-button');

    buttons.forEach(button => {
        button.addEventListener('click', function () {
            const testSectionId = button.dataset.testSectionId;
            const testTitle = button.textContent;

            // Modalni ochishdan oldin ma'lumotni yuklash
            fetch(`/user/test/${testSectionId}/`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    updateModalContent(testTitle, data); // Modal ma'lumotlarini yangilash
                    openModal(); // Modalni ochish
                })
                .catch(error => console.error('Error:', error));
        });
    });

    // Modalni yopish uchun hodisa qo'shish
    const closeModalButton = document.querySelector('.close');
    closeModalButton.addEventListener('click', closeModal);

    // Modalni tashqi joyga bosganda yopish
    window.addEventListener('click', function (event) {
        const modal = document.getElementById('testModal');
        if (event.target === modal) {
            closeModal();
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const modalTestTitle = document.getElementById('modalTestTitle');
    console.log(modalTestTitle); // Bu yerni tekshirish uchun ishlatib ko'ring
});

document.addEventListener('DOMContentLoaded', function () {
    const modalTestTitle = document.getElementById('modalTestTitle');
    if (!modalTestTitle) {
        console.error('modalTestTitle element topilmadi!');
    } else {
        console.log('modalTestTitle element:', modalTestTitle);
    }
});
