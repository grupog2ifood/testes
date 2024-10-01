document.addEventListener('DOMContentLoaded', function () {
    const btnsAtualizar = document.querySelectorAll('.btn-atualizar');
    btnsAtualizar.forEach(btn => {
        btn.addEventListener('click', function (event) {
            event.preventDefault();
            const id = this.getAttribute('data-id');
            const row = this.parentNode.parentNode;
            const nome = row.cells[1].innerText;
            const cpf = row.cells[2].innerText;
            const email = row.cells[3].innerText;
            const celular = row.cells[4].innerText;
            const telefone = row.cells[5].innerText;

            document.getElementById('update-id').value = id;
            document.getElementById('update-nome').value = nome;
            document.getElementById('update-cpf').value = cpf;
            document.getElementById('update-email').value = email;
            document.getElementById('update-celular').value = celular;
            document.getElementById('update-telefone').value = telefone;

            document.getElementById('atualizar-form').style.display = 'block';
        });
    });
});
