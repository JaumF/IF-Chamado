document.addEventListener("DOMContentLoaded", function() {
    var departamentoInput = document.querySelector('input[name="departamento"]');
    var salaSelect = document.getElementById('sala');

    function updateSalaOptions(departamento) {
        let options = [];

        if (departamento === 'Laboratório') {
            options = [
                { value: 'sem-opcao', text: '' },
                { value: 'Laboratório 1', text: 'Laboratório 1' },
                { value: 'Laboratório 2', text: 'Laboratório 2' }
            ];
        } else if (departamento === 'Pavilhão Novo') {
            options = [
                { value: 'sem-opcao', text: '' },
                { value: 'Sala 1', text: 'Sala 1' },
                { value: 'Sala 2', text: 'Sala 2' }
            ];
        } else {
            options = [
                { value: 'sem-opcao', text: '' }
            ];
        }

        salaSelect.innerHTML = '';
        options.forEach(function(option) {
            var opt = document.createElement('option');
            opt.value = option.value;
            opt.textContent = option.text;
            salaSelect.appendChild(opt);
        });
    }

    updateSalaOptions(departamentoInput.value);

    departamentoInput.addEventListener('change', function() {
        updateSalaOptions(this.value);
    });
});
