
    // Função para exibir a conversa ao selecionar um usuário
    function openTab(userId) {
        // Esconde todas as abas
        var tabs = document.querySelectorAll('.tab-content');
        tabs.forEach(function(tab) {
            tab.style.display = 'none';
        });

        // Mostra a aba do usuário selecionado
        if (userId) {
            document.getElementById('tab-' + userId).style.display = 'block';
        }
    }
