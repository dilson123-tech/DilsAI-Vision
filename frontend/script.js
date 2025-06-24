// frontend/script.js

async function gerarImagem() {
  const prompt = document.getElementById("prompt").value.trim();
  if (!prompt) {
    alert("Digite um prompt antes de gerar a imagem!");
    return;
  }

  // Limpa resultado anterior
  document.getElementById("resultado").innerHTML = "⌛ Gerando imagem...";

  try {
    const resposta = await fetch("https://dilsai-backend.onrender.com/gerar-imagem", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
    });

    const dados = await resposta.json();

    if (dados.imagem) {
      document.getElementById("resultado").innerHTML = `
        <p><strong>Prompt:</strong> ${prompt}</p>
        <img src="${dados.imagem}" alt="Imagem gerada" style="max-width:100%;border:1px solid #ccc;padding:5px;" />
      `;
      carregarHistorico(); // Atualiza histórico após gerar
    } else {
      document.getElementById("resultado").innerHTML = "Erro ao gerar imagem.";
    }
  } catch (erro) {
    console.error("Erro:", erro);
    document.getElementById("resultado").innerHTML = "Erro ao conectar com a API.";
  }
}

async function carregarHistorico() {
  try {
    const resposta = await fetch("https://dilsai-backend.onrender.com/data/output/historico.json");
    const historico = await resposta.json();

    const divHistorico = document.getElementById("historico");
    divHistorico.innerHTML = "";

    [...historico].reverse().forEach(item => {
      const img = document.createElement("img");
      img.src = item.url_local;
      img.title = item.prompt;
      img.style = "width: 120px; border: 1px solid #ccc; margin: 5px;";
      divHistorico.appendChild(img);
    });
  } catch (erro) {
    console.warn("Histórico não encontrado ainda.");
  }
}

// Carrega histórico ao abrir a página
window.onload = carregarHistorico;

function limparHistorico() {
  const historico = document.getElementById('historico');
  historico.innerHTML = '';
  localStorage.removeItem('historico');
}
