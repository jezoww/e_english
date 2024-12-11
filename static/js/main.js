// FORM DROPDOWN

document.querySelectorAll('.dropdown-wrapper').forEach((wrapper) => {
    wrapper.addEventListener('click', (e) => {
        e.stopPropagation();
        const dropdown = wrapper.nextElementSibling;
        const isVisible = dropdown.style.display === 'block';

        document.querySelectorAll('.dropdown-options').forEach((options) => {
            options.style.display = 'none';
        });

        dropdown.style.display = isVisible ? 'none' : 'block';
    });
});

document.querySelectorAll('.dropdown-option').forEach((option) => {
    option.addEventListener('click', (e) => {
        const input = option.closest('.form-group').querySelector('#form-input');
        input.value = option.textContent.trim();
        option.closest('.dropdown-options').style.display = 'none';


        document.querySelectorAll('.dropdown-option-icon').forEach((icon) => {
            icon.style.display = 'none';
        });


        const icon = option.querySelector('.dropdown-option-icon');
        if (icon) {
            icon.style.display = 'block';
        }
    });
});

document.body.addEventListener('click', () => {
    document.querySelectorAll('.dropdown-options').forEach((dropdown) => {
        dropdown.style.display = 'none';
    });
});

document.querySelectorAll('.dropdown-wrapper').forEach((wrapper) => {
    wrapper.addEventListener('click', (e) => {
        e.stopPropagation();
    });
});


// ADMIN PAGE books dropdown
// const dropdownWrapper = document.querySelector('.books-dropdown-wrapper');
// const dropdownInput = document.querySelector('#books-input');
// const dropdownOptions = document.querySelector('.books-dropdown-options');
// const dropdownOptionItems = document.querySelectorAll('.books-dropdown-option');
//
//
// dropdownWrapper.addEventListener('click', () => {
//     dropdownOptions.style.display = dropdownOptions.style.display === 'block' ? 'none' : 'block';
// });
//
//
// dropdownOptionItems.forEach(option => {
//     option.addEventListener('click', () => {
//         dropdownInput.value = option.textContent;
//         dropdownOptions.style.display = 'none';
//     });
// });
//
// document.addEventListener('click', (e) => {
//     if (!e.target.closest('.books-group')) {
//         dropdownOptions.style.display = 'none';
//     }
// });


// Qo'shish tugmasini modalni ochishga bog'lash
document.querySelector('.submit button').addEventListener('click', function () {
    const modal = document.querySelector('#add-book-modal'); // Faqat "Kitob qo'shish" modali
    if (modal) {
        modal.classList.remove('hidden'); // Modalni ko'rsatish
    }
});

// Barcha "Orqaga" tugmalarini yopish
document.querySelectorAll('.cancel-btn').forEach(button => {
    button.addEventListener('click', function () {
        const modal = this.closest('.modal');
        if (modal) {
            modal.classList.add('hidden'); // Modalni yashirish
        }
    });
});


document.addEventListener("DOMContentLoaded", () => {
    // Edit modalni boshqarish elementlari
    const editButtons = document.querySelectorAll(".edit-btn");
    const editModal = document.getElementById("edit-book-modal");
    const bookNameInput = document.getElementById("edit-book-name");
    const bookLevelInput = document.getElementById("edit-book-level");
    const editForm = editModal.querySelector("form");

    editButtons.forEach((button) => {
        button.addEventListener("click", (e) => {
            e.preventDefault();

            // Kitob ma'lumotlarini olish
            const listItem = button.closest(".unit-list-item");
            const bookId = listItem.dataset.bookId; // Kitob IDsi dataset orqali olindi
            const bookName = listItem.querySelector(".book-name").textContent.trim();
            const bookLevel = listItem.querySelector(".right span").textContent.match(/\d+/)[0];

            // Modalni ma'lumotlar bilan to'ldirish
            bookNameInput.value = bookName;
            bookLevelInput.value = bookLevel;

            // Form actionni dinamik yangilash
            editForm.action = `/admin2/book-update/${bookId}`; // Backendga to'g'ri ID yuboriladi

            // Modalni ko'rsatish
            editModal.classList.remove("hidden");
        });
    });

    // Modalni yopish
    const cancelEditBtn = editModal.querySelector(".cancel-btn");
    cancelEditBtn.addEventListener("click", (e) => {
        e.preventDefault();
        editModal.classList.add("hidden");
    });
});


////////////////////////////////////////////////////////////////////////////

// Qo'shish tugmasini modalni ochishga bog'lash
document.querySelector('.submit button').addEventListener('click', function () {
    const modal = document.querySelector('#add-unit-modal'); // Faqat "Kitob qo'shish" modali
    if (modal) {
        modal.classList.remove('hidden'); // Modalni ko'rsatish
    }
});

// Barcha "Orqaga" tugmalarini yopish
document.querySelectorAll('.cancel-btn').forEach(button => {
    button.addEventListener('click', function () {
        const modal = this.closest('.modal');
        if (modal) {
            modal.classList.add('hidden'); // Modalni yashirish
        }
    });
});


document.addEventListener("DOMContentLoaded", () => {
    const editUnitModal = document.getElementById("edit-unit-modal");
    const unitNameInput = editUnitModal.querySelector("input[name='name']");
    const unitNumInput = editUnitModal.querySelector("input[name='unit_num']");
    const bookSelect = editUnitModal.querySelector("select[name='book_id']");
    const form = editUnitModal.querySelector("form");

    document.querySelectorAll(".edit-unit-btn").forEach((button) => {
        button.addEventListener("click", (event) => {
            const unitItem = event.target.closest(".unit-list-item");

            // "Unit 1: Unit Name" dan ma'lumotni olish
            const unitFullText = unitItem.childNodes[0].nodeValue.trim(); // "Unit 1: Unit Name"
            const [_, unitNum, unitName] = unitFullText.match(/Unit (\d+): (.+)/); // Unit raqami va nomini ajratish

            const bookId = unitItem.getAttribute("data-book-id");
            const unitId = unitItem.getAttribute("data-unit-id");

            // Ma'lumotlarni formaga qo'yish
            unitNameInput.value = unitName;
            unitNumInput.value = unitNum;
            bookSelect.value = bookId;

            // Form action-ni yangilash
            form.action = `/admin2/unit-update/${unitId}`;

            // Modalni ochish
            editUnitModal.classList.remove("hidden");
        });
    });

    // Modalni yopish
    editUnitModal.querySelector(".cancel-btn").addEventListener("click", () => {
        editUnitModal.classList.add("hidden");
    });
});


///////////////////////////////////////////////////////////////////////////////////////////////
document.querySelector('.submit button').addEventListener('click', function () {
    const modal = document.querySelector('#add-vocab-modal');
    if (modal) {
        modal.classList.remove('hidden');
    }
});

document.querySelectorAll('.cancel-btn').forEach(button => {
    button.addEventListener('click', function () {
        const modal = this.closest('.modal');
        if (modal) {
            modal.classList.add('hidden');
        }
    });
});

document.querySelectorAll('.edit-btn').forEach(button => {
    button.addEventListener('click', () => {
        const vocabId = button.dataset.id;
        const uzbek = button.dataset.uzbek;
        const english = button.dataset.english;
        const unitId = button.dataset.unitId;

        // Formani to'ldirish
        document.querySelector('#vocab-update-modal input[name="uzbek"]').value = uzbek;
        document.querySelector('#vocab-update-modal input[name="english"]').value = english;
        document.querySelector('#vocab-update-modal select[name="unit_id"]').value = unitId;
        document.querySelector('#vocab-update-modal form').action = `/admin2/vocab-update/${vocabId}/`;

        // Modalni ochish
        document.querySelector('#vocab-update-modal').classList.remove('hidden');
    });
});


document.querySelector('.submit-excel button').addEventListener('click', function () {
    const modal = document.querySelector('#add-vocab-excel-modal');
    if (modal) {
        modal.classList.remove('hidden');
    }
});



