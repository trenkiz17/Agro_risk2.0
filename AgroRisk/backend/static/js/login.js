document.addEventListener("DOMContentLoaded", () => {

    document
        .getElementById("loginForm")
        .addEventListener("submit", realizarLogin);

});

async function realizarLogin(event) {

    event.preventDefault();

    const email = document.getElementById("email").value.trim();

    const senha = document.getElementById("senha").value;

    if (email === "" || senha === "") {

        alert("Preencha todos os campos.");

        return;

    }

    try {

        const resposta = await login(email, senha);

        if (!resposta) {

            alert("Erro ao conectar com a API.");

            return;

        }

        if (resposta.sucesso) {

            if (!resposta.token) {
                alert("O servidor não enviou a autenticação. Verifique a versão do backend.");
                return;
            }
            sessionStorage.setItem("agrorisk_token", resposta.token);

            localStorage.setItem("usuario", JSON.stringify(resposta.usuario));

            window.location.href = "dashboard.html";

        }

        else {

            alert(resposta.mensagem);

        }

    }

    catch (erro) {

        console.error(erro);

        alert("Erro ao conectar com a API.");

    }

}